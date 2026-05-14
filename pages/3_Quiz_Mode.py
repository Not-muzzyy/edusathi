"""pages/3_Quiz_Mode.py — Adaptive quiz with premium UI."""
import streamlit as st
import json

st.set_page_config(page_title="Quiz Mode — EduSathi", page_icon="🧠", layout="wide")

from modules.ui_components import inject_css, page_header, empty_state, success_feedback, error_feedback, render_sidebar
from modules.quiz_engine import QuizSession
from modules.llm_client import generate_mcqs
from modules.rag_pipeline import retrieve_context_from_multiple
from modules.auth import get_user_documents, save_quiz_attempt
from modules.progress_tracker import update_progress_from_result
from modules.modern_ui import sanitize_input, validate_input, toast_success, toast_error

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()

if "quiz_session" not in st.session_state:
    st.session_state.quiz_session = None
if "quiz_answer_shown" not in st.session_state:
    st.session_state.quiz_answer_shown = False

page_header("◎ Quiz Mode", "Test your knowledge with adaptive AI-generated questions")

if st.session_state.quiz_session is None or st.session_state.quiz_session.finished:
    if st.session_state.quiz_session and st.session_state.quiz_session.finished:
        res = st.session_state.quiz_session.get_result()

        # Results card with enhanced styling
        result_icon = "🏆" if res["percentage"] >= 70 else "📖" if res["percentage"] >= 50 else "💪"
        result_color = "#4ECDC4" if res["percentage"] >= 70 else "#FFB700" if res["percentage"] >= 50 else "#FF5252"
        result_msg = "Excellent work!" if res["percentage"] >= 70 else "Good effort!" if res["percentage"] >= 50 else "Keep practicing!"

        st.markdown(f"""
        <div class="glass-container" style="text-align:center;padding:3.5rem 2rem;">
            <div style="font-size:5rem;margin-bottom:1.25rem;animation:bounce 0.6s ease;">{result_icon}</div>
            <h2 style="color:#E0E0F0;font-weight:700;margin:0;font-size:1.8rem;">Quiz Complete!</h2>
            <p style="color:{result_color};font-size:1.1rem;margin:0.5rem 0 0 0;font-weight:500;">{result_msg}</p>
            <div style="font-size:4rem;font-weight:800;background:linear-gradient(135deg,#6C63FF,#4ECDC4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                margin:1.5rem 0;">
                {res["score"]}/{res["total"]}
            </div>
            <div style="display:inline-block;padding:0.5rem 1.5rem;background:rgba(108,99,255,0.15);
                border-radius:20px;border:1px solid rgba(108,99,255,0.3);">
                <span style="font-size:2rem;color:{result_color};font-weight:700;">{res["percentage"]}%</span>
            </div>
            <p style="color:#9E9EC0;margin:1.25rem 0 0 0;font-size:0.95rem;">
                Difficulty reached: <span style="color:#FFB700;font-weight:600;">{res["difficulty"].capitalize()}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        qs = st.session_state.quiz_session
        try:
            save_quiz_attempt(user["id"], qs.subject, qs.topic, res["score"], res["total"],
                              res["difficulty"], json.dumps(res["history"]))
            update_progress_from_result(user["id"], qs.subject, qs.topic, res["score"], res["total"])
        except Exception as e:
            st.warning(f"Could not save quiz results: {e}")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 Review Your Answers", expanded=False):
            for i, h in enumerate(res["history"]):
                is_correct = h["correct"]
                color = "#4ECDC4" if is_correct else "#FF5252"
                icon = "✓" if is_correct else "✗"
                bg_color = "rgba(78,205,196,0.1)" if is_correct else "rgba(255,82,82,0.1)"
                st.markdown(f"""
                <div style="background:{bg_color};border-radius:18px;padding:1.4rem 1.75rem;margin:0.85rem 0;
                    border-left:5px solid {color};">
                    <div style="display:flex;align-items:flex-start;gap:0.85rem;">
                        <span style="font-size:1.4rem;color:{color};font-weight:700;min-width:24px;">{icon}</span>
                        <div style="flex:1;">
                            <div style="font-weight:600;color:#E0E0F0;font-size:1.02rem;margin-bottom:0.6rem;line-height:1.5;">
                                Q{i+1}: {h["question"]}</div>
                            <div style="font-size:0.9rem;color:#9E9EC0;margin-bottom:0.6rem;">
                                Your answer: <span style="color:{color};font-weight:500;">{h["selected"]}</span>
                                &nbsp;|&nbsp; Correct: <span style="color:#4ECDC4;font-weight:500;">{h["correct_answer"]}</span>
                            </div>
                            <div style="font-size:0.9rem;color:#A0D9CC;padding:0.85rem;
                                background:rgba(0,0,0,0.22);border-radius:10px;margin-top:0.5rem;line-height:1.6;">
                                💡 {h["explanation"]}
                            </div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Quiz", width="stretch"):
                st.session_state.quiz_session = None
                st.session_state.quiz_answer_shown = False
                st.rerun()
        with col2:
            if st.button("📊 View Dashboard", width="stretch"):
                st.switch_page("pages/1_Dashboard.py")

    else:
        # Quiz setup form
        docs = get_user_documents(user["id"])
        col_form, col_info = st.columns([2, 1])

        with col_form:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1.5rem 0;font-weight:600;'>⚙️ Configure Your Quiz</h4>", unsafe_allow_html=True)

            subject = st.text_input("📚 Subject", placeholder="e.g. Data Structures", key="q_sub")
            topic = st.text_input("🎯 Topic", placeholder="e.g. Binary Trees", key="q_topic")

            col_q, col_d = st.columns(2)
            with col_q:
                n_q = st.slider("📝 Questions", 3, 15, 5)
            with col_d:
                difficulty = st.selectbox("⚡ Difficulty", ["easy", "medium", "hard"], index=1)

            if docs:
                doc_choices = {d["filename"]: d for d in docs}
                selected_docs = st.multiselect(
                    "📄 Study Materials",
                    list(doc_choices.keys()),
                    default=list(doc_choices.keys())[:1],
                    help="Select which uploaded documents to use for generating questions"
                )
            else:
                selected_docs = []
                st.markdown("""
                <div style="padding:0.85rem 1rem;background:rgba(108,99,255,0.12);border-radius:12px;margin:0.75rem 0;
                    border:1px solid rgba(108,99,255,0.25);">
                    <span style="color:#9E9EC0;font-size:0.9rem;">
                        💡 Upload PDFs in Chat Tutor for context-based questions.
                    </span>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Validate inputs
            is_valid_topic, topic_msg = validate_input(topic.strip(), min_len=2, max_len=100)
            
            if topic and not is_valid_topic:
                st.error(f"⚠️ {topic_msg}")
            
            btn_disabled = not is_valid_topic or not topic.strip()
            if st.button("🚀 Start Quiz", width="stretch", disabled=btn_disabled):
                # Sanitize inputs to prevent prompt injection
                sanitized_topic = sanitize_input(topic)
                sanitized_subject = sanitize_input(subject)
                
                with st.spinner("🧠 Generating questions..."):
                    try:
                        if selected_docs:
                            paths = [doc_choices[n]["vector_store_path"] for n in selected_docs]
                            context = retrieve_context_from_multiple(sanitized_topic, paths, top_k=6)
                        else:
                            context = f"Topic: {sanitized_topic}. Subject: {sanitized_subject}. Generate general university-level questions."
                        questions = generate_mcqs(context, sanitized_topic, n=n_q, difficulty=difficulty)
                    except Exception as e:
                        questions = []
                        toast_error(f"Error generating questions: {str(e)}")
                
                if questions:
                    qs = QuizSession(questions, topic=sanitized_topic, subject=sanitized_subject)
                    qs.difficulty = difficulty
                    st.session_state.quiz_session = qs
                    st.session_state.quiz_answer_shown = False
                    toast_success("Quiz created! Starting now...")
                    st.rerun()
                else:
                    toast_error("Could not generate questions. Check your API key or try a different topic.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;'>💡 How It Works</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div style="color:#9E9EC0;font-size:0.92rem;line-height:2;">
                <div style="margin-bottom:1.1rem;display:flex;align-items:flex-start;gap:10px;">
                    <span style="color:#6C63FF;font-weight:600;font-size:1.1rem;">◎</span>
                    <span>Questions are AI-generated from your study materials</span>
                </div>
                <div style="margin-bottom:1.1rem;display:flex;align-items:flex-start;gap:10px;">
                    <span style="color:#4ECDC4;font-weight:600;font-size:1.1rem;">◎</span>
                    <div>Difficulty adapts to your performance:<br>
                    <span style="margin-left:0.25rem;color:#78788C;">80%+ → Hard | Below 40% → Easy</span></div>
                </div>
                <div style="display:flex;align-items:flex-start;gap:10px;">
                    <span style="color:#FFB700;font-weight:600;font-size:1.1rem;">◎</span>
                    <span>Progress is saved automatically to your dashboard</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Active quiz session
    qs = st.session_state.quiz_session
    q = qs.current_question()

    # Progress bar and info
    progress_pct = qs.progress_pct()
    st.progress(progress_pct)

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
        padding:0.85rem 1.25rem;background:rgba(108,99,255,0.1);border-radius:14px;margin:1.25rem 0 1.75rem 0;
        border:1px solid rgba(108,99,255,0.2);">
        <span style="color:#E0E0F0;font-weight:600;font-size:1rem;">📝 Question {qs.index + 1} of {len(qs.questions)}</span>
        <div>
            <span style="color:#4ECDC4;font-weight:700;font-size:1.05rem;">Score: {qs.score}</span>
            <span style="color:#9E9EC0;margin:0 0.6rem;">|</span>
            <span style="color:#FFB700;font-weight:600;">{qs.difficulty.capitalize()}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    if q:
        # Question card
        st.markdown(f'<div class="quiz-question-card">❓ {q["question"]}</div>', unsafe_allow_html=True)

        if not st.session_state.quiz_answer_shown:
            # Show options as clickable buttons
            st.markdown("<br>", unsafe_allow_html=True)
            for i, opt in enumerate(q.get("options", [])):
                if st.button(opt, key=f"opt_{i}", width="stretch"):
                    result = qs.submit_answer(opt[0])
                    st.session_state.last_result = result
                    st.session_state.quiz_answer_shown = True
                    st.rerun()
        else:
            # Show answer feedback
            result = st.session_state.get("last_result", {})
            st.markdown("<br>", unsafe_allow_html=True)

            for i, opt in enumerate(q.get("options", [])):
                letter = opt[0].upper() if opt else ""
                correct_letter = result.get("correct_answer", "").upper()
                selected_letter = result.get("selected", " ")[0].upper() if result.get("selected") else ""

                if letter == correct_letter:
                    css_class = "option-correct"
                    icon = "✓ "
                elif letter == selected_letter:
                    css_class = "option-wrong"
                    icon = "✗ "
                else:
                    css_class = ""
                    icon = ""

                st.markdown(f'<div class="option-btn {css_class}">{icon}{opt}</div>', unsafe_allow_html=True)

            # Feedback message
            st.markdown("<br>", unsafe_allow_html=True)
            if result.get("correct"):
                success_feedback("Correct! Well done!")
            else:
                st.markdown(f"""
                <div class="feedback-error">
                    <span class="icon">✗</span>
                    <div>
                        <span class="text">Incorrect</span>
                        <span style="color:#9E9EC0;margin-left:0.75rem;font-size:0.95rem;">
                            Correct answer: <span style="color:#4ECDC4;font-weight:600;">{result.get('correct_answer')}</span>
                        </span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Explanation expander
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("💡 View Explanation", expanded=True):
                st.markdown(f"""
                <div style="color:#E0E0F0;line-height:1.75;padding:0.6rem 0;font-size:0.98rem;">
                    {result.get("explanation", "No explanation available.")}
                </div>""", unsafe_allow_html=True)

            # Next button
            st.markdown("<br>", unsafe_allow_html=True)
            if qs.finished:
                if st.button("🏁 View Results", width="stretch"):
                    st.session_state.quiz_answer_shown = False
                    st.rerun()
            else:
                if st.button("➡️ Next Question", width="stretch"):
                    st.session_state.quiz_answer_shown = False
                    st.rerun()
