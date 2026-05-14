"""modules/llm_client.py — Groq API wrapper with robust error handling."""
import os
import json
import re
import logging
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
logger = logging.getLogger(__name__)


def _client():
    """Get Groq client with API key validation."""
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY not configured. Please set it in .env file.")
    return Groq(api_key=api_key)


def _parse_json_response(raw: str) -> list:
    """Robust JSON parsing with multiple fallback strategies."""
    if not raw:
        return []
    
    # Clean markdown fences
    cleaned = raw.strip()
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()
    
    # Try direct parse
    try:
        result = json.loads(cleaned)
        if isinstance(result, list):
            return result
        return []
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array in the response
    match = re.search(r'\[[\s\S]*\]', cleaned)
    if match:
        try:
            result = json.loads(match.group())
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass
    
    # Try line by line for objects
    try:
        objects = []
        for match in re.finditer(r'\{[^{}]*\}', cleaned):
            try:
                obj = json.loads(match.group())
                objects.append(obj)
            except json.JSONDecodeError:
                continue
        if objects:
            return objects
    except Exception:
        pass
    
    return []


def chat(context: str, question: str, history: list = None) -> str:
    """Context-grounded chat answer with error handling."""
    try:
        system = (
            "You are EduSathi, a helpful and patient AI study tutor for students of "
            "Vijayanagara Sri Krishnadevaraya University (VSKUB). "
            "Answer questions clearly and concisely using ONLY the provided study material context. "
            "If the answer is not in the context, respond exactly with: "
            "'I don't have information on that in your uploaded material.' "
            "Do not hallucinate facts or use outside knowledge.\n\n"
            f"Context:\n{context}"
        )
        messages = [{"role": "system", "content": system}]
        if history:
            for h in history[-6:]:
                messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": question})
        
        resp = _client().chat.completions.create(
            model=MODEL, messages=messages, temperature=0.3, max_tokens=1024
        )
        
        if resp and resp.choices and resp.choices[0].message:
            content = resp.choices[0].message.content
            if content:
                return content.strip()
        
        return "I apologize, but I couldn't process that question. Please try again."
        
    except ValueError as e:
        return f"⚠️ Configuration Error: {str(e)}"
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return "I'm having trouble connecting right now. Please check your internet connection and try again."


def generate_mcqs(context: str, topic: str, n: int = 5, difficulty: str = "medium") -> list:
    """Generate MCQs with robust error handling. Returns list of dicts."""
    try:
        prompt = (
            f"Generate exactly {n} {difficulty}-difficulty multiple choice questions "
            f"about the topic '{topic}' based strictly on the following study material. "
            "Return ONLY a valid JSON array with no extra text, no markdown fences. "
            "Each element must have exactly these keys: "
            "question (string), options (array of 4 strings like ['A. ...', 'B. ...', 'C. ...', 'D. ...']), "
            "answer (string, one of A/B/C/D), explanation (string). "
            f"Study material:\n{context}"
        )
        
        resp = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5, max_tokens=3000
        )
        
        if not resp or not resp.choices or not resp.choices[0].message:
            return []
        
        raw = resp.choices[0].message.content
        if not raw:
            return []
        
        questions = _parse_json_response(raw)
        
        # Validate question structure
        valid_questions = []
        for q in questions:
            if isinstance(q, dict) and "question" in q and "options" in q and "answer" in q:
                # Ensure options is a list of 4 items
                if isinstance(q.get("options"), list) and len(q["options"]) >= 4:
                    q["options"] = q["options"][:4]
                    q["explanation"] = q.get("explanation", "")
                    valid_questions.append(q)
        
        return valid_questions
        
    except ValueError as e:
        logger.error(f"MCQ generation config error: {e}")
        return []
    except Exception as e:
        logger.error(f"MCQ generation error: {e}")
        return []


def generate_flashcards(context: str, n: int = 10) -> list:
    """Generate flashcards with robust error handling. Returns list of {front, back}."""
    try:
        prompt = (
            f"Generate exactly {n} flashcards from the following study material. "
            "Return ONLY a valid JSON array with no markdown fences. "
            "Each element: {\"front\": \"term or question\", \"back\": \"definition or answer\"}. "
            f"Material:\n{context}"
        )
        
        resp = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=2000
        )
        
        if not resp or not resp.choices or not resp.choices[0].message:
            return []
        
        raw = resp.choices[0].message.content
        if not raw:
            return []
        
        cards = _parse_json_response(raw)
        
        # Validate flashcard structure
        valid_cards = []
        for card in cards:
            if isinstance(card, dict) and "front" in card and "back" in card:
                valid_cards.append({
                    "front": str(card["front"]),
                    "back": str(card["back"])
                })
        
        return valid_cards
        
    except ValueError as e:
        logger.error(f"Flashcard generation config error: {e}")
        return []
    except Exception as e:
        logger.error(f"Flashcard generation error: {e}")
        return []


def explain_wrong_answer(question: str, selected: str, correct: str) -> str:
    """Explain why an answer is wrong with error handling."""
    try:
        prompt = (
            f"The student answered '{selected}' to: '{question}'. "
            f"The correct answer is '{correct}'. "
            "Explain in 2-3 encouraging sentences why the correct answer is right "
            "and what concept the student should review."
        )
        
        resp = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=300
        )
        
        if resp and resp.choices and resp.choices[0].message:
            content = resp.choices[0].message.content
            if content:
                return content.strip()
        
        return "Review this concept in your study material for better understanding."
        
    except Exception as e:
        logger.error(f"Explanation error: {e}")
        return "Review this concept in your study material for better understanding."


def analyze_question_paper(text: str, n: int = 10) -> list:
    """Analyze question paper to identify frequently asked topics with comprehensive analysis."""
    try:
        # Use more of the text — Groq supports up to 128k context on llama-3.3-70b
        max_chars = 12000
        paper_text = text[:max_chars] if len(text) > max_chars else text
        
        prompt = (
            f"You are an expert academic examiner. Carefully analyze ALL of the following "
            f"past exam questions and identify the top {n} most frequently appearing topics.\n\n"
            "Instructions:\n"
            "1. Read EVERY question in the paper thoroughly.\n"
            "2. Identify recurring themes, concepts, and subject areas.\n"
            "3. Count how many times each topic appears across ALL questions.\n"
            "4. Rate importance as 'high' (appears in 3+ questions or is a major topic), "
            "'medium' (appears in 2 questions), or 'low' (appears once).\n"
            "5. Include sub-topics when a broad topic has multiple specific questions.\n\n"
            "Return ONLY a valid JSON array, no markdown fences, no extra text:\n"
            '[{"topic": "Topic Name", "frequency": 3, "importance": "high", '
            '"subtopics": ["Subtopic A", "Subtopic B"], '
            '"question_types": ["short answer", "essay", "MCQ"]}]\n\n'
            f"Question Paper Content:\n{paper_text}"
        )
        
        resp = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, max_tokens=2500
        )
        
        if not resp or not resp.choices or not resp.choices[0].message:
            return []
        
        raw = resp.choices[0].message.content
        if not raw:
            return []
        
        topics = _parse_json_response(raw)
        
        # Validate and normalize topic structure
        valid_topics = []
        for t in topics:
            if isinstance(t, dict) and "topic" in t:
                valid_topics.append({
                    "topic": str(t.get("topic", "")),
                    "frequency": int(t.get("frequency", 1)),
                    "importance": str(t.get("importance", "medium")),
                    "subtopics": t.get("subtopics", []),
                    "question_types": t.get("question_types", [])
                })
        
        # Sort by frequency descending
        valid_topics.sort(key=lambda x: x["frequency"], reverse=True)
        
        return valid_topics[:n]
        
    except Exception as e:
        logger.error(f"Paper analysis error: {e}")
        return []

