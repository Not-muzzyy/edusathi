"""pages/4_Exam_Simulation.py"""
import streamlit as st
import time, json

st.set_page_config(page_title="Exam Simulation — EduSathi", page_icon="⏱️", layout="wide")

from modules.ui_components import inject_css, page_header, render_sidebar
from modules.quiz_engine import QuizSession
from modules.llm_client import generate_mcqs
from modules.rag_pipeline import retrieve_context_from_multiple
from modules.auth import get_user_documents, save_quiz_attempt
from modules.progress_tracker import update_progress_from_result
from modules.modern_ui import sanitize_input, validate_input, toast_success, toast_error, toast_warning

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()

if "exam_session" not in st.session_state:
    st.session_state.exam_session = None
if "exam_start_time" not in st.session_state:
    st.session_state.exam_start_time = None
if "exam_answers" not in st.session_state:
    st.session_state.exam_answers = {}
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

user = st.session_state.user
page_header("◇ Exam Simulation", "Timed mock exam modelled on VSKUB patterns")

if st.session_state.exam_session is None or st.session_state.exam_submitted:
    if st.session_state.exam_submitted and st.session_state.exam_session:
        qs = st.session_state.exam_session
        questions = qs.questions
        answers = st.session_state.exam_answers
        score = sum(1 for i, q in enumerate(questions)
                    if answers.get(i, "")[:1].upper() == q.get("answer","A").upper())
        total = len(questions)
        pct = round(score / total * 100, 1) if total else 0
        elapsed = int(time.time() - (st.session_state.exam_start_time or time.time()))
        mins, secs = divmod(elapsed, 60)

        save_quiz_attempt(user["id"], qs.subject, qs.topic, score, total, "exam",
                          json.dumps([{"question": q["question"], "selected": answers.get(i,""),
                                       "correct": answers.get(i,"")[:1].upper()==q.get("answer","A").upper(),
                                       "explanation": q.get("explanation","")}
                                      for i, q in enumerate(questions)]))
        update_progress_from_result(user["id"], qs.subject, qs.topic, score, total)

        st.markdown(f"""
        <div class="glass-container" style="text-align:center;padding:2.5rem;">
            <div style="font-size:3.5rem;margin-bottom:0.5rem;">{"🏆" if pct>=60 else "📖"}</div>
            <h2 style="color:#6C63FF;font-weight:700;">Exam Complete!</h2>
            <div style="font-size:3rem;font-weight:800;background:linear-gradient(135deg,#6C63FF,#4ECDC4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                {score}/{total} ({pct}%)
            </div>
            <p style="color:#9E9EC0;margin-top:0.5rem;">
                Time taken: <strong style="color:#FFB700;">{mins}m {secs}s</strong>
            </p>
        </div>""", unsafe_allow_html=True)

        with st.expander("📋 Detailed Review"):
            for i, q in enumerate(questions):
                sel = answers.get(i, "Not answered")
                correct = q.get("answer", "A")
                is_correct = sel[:1].upper() == correct.upper() if sel else False
                color = "#4ECDC4" if is_correct else "#FF5252"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:1rem;margin:0.5rem 0;
                    border-left:3px solid {color};">
                    <div style="font-weight:600;color:#E0E0F0;">{"✅" if is_correct else "❌"} Q{i+1}: {q["question"]}</div>
                    <div style="font-size:0.88rem;color:#9E9EC0;margin-top:0.3rem;">
                        Your answer: {sel} | Correct: {correct}</div>
                    <div style="font-size:0.88rem;color:#A0D9CC;margin-top:0.3rem;">{q.get("explanation","")}</div>
                </div>""", unsafe_allow_html=True)

        if st.button("🔁 New Exam", width="stretch"):
            st.session_state.exam_session = None
            st.session_state.exam_submitted = False
            st.session_state.exam_answers = {}
            st.session_state.exam_start_time = None
            st.rerun()
    else:
        docs = get_user_documents(user["id"])
        col_form, col_info = st.columns([2,1])
        with col_form:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("⚙️ Configure Exam")
            subject = st.text_input("Subject", placeholder="e.g. Computer Networks")
            topic = st.text_input("Topic(s)", placeholder="e.g. OSI Model, TCP/IP")
            n_q = st.slider("Questions", 5, 30, 10)
            time_limit = st.slider("Time Limit (minutes)", 5, 120, 30)
            if docs:
                doc_choices = {d["filename"]: d for d in docs}
                sel_docs = st.multiselect("Use Documents", list(doc_choices.keys()),
                                          default=list(doc_choices.keys())[:1])
            else:
                sel_docs = []

            # Validate inputs
            is_valid_topic, topic_msg = validate_input(topic.strip(), min_len=2, max_len=150)
            
            if topic and not is_valid_topic:
                st.error(f"⚠️ {topic_msg}")
            
            btn_disabled = not is_valid_topic or not topic.strip()
            if st.button("🚀 Start Exam", width="stretch", disabled=btn_disabled):
                # Sanitize inputs to prevent prompt injection
                sanitized_topic = sanitize_input(topic)
                sanitized_subject = sanitize_input(subject)
                
                with st.spinner("Generating exam questions..."):
                    try:
                        if sel_docs:
                            paths = [doc_choices[n]["vector_store_path"] for n in sel_docs]
                            context = retrieve_context_from_multiple(sanitized_topic, paths, top_k=8)
                        else:
                            context = f"Topic: {sanitized_topic}. Subject: {sanitized_subject}."
                        questions = generate_mcqs(context, sanitized_topic, n=n_q, difficulty="medium")
                    except Exception as e:
                        questions = []
                        toast_error(f"Failed to generate questions: {str(e)}")
                
                if questions:
                    qs = QuizSession(questions, topic=sanitized_topic, subject=sanitized_subject)
                    st.session_state.exam_session = qs
                    st.session_state.exam_start_time = time.time()
                    st.session_state.exam_time_limit = time_limit * 60
                    st.session_state.exam_answers = {}
                    st.session_state.exam_submitted = False
                    st.session_state.exam_locked = False  # Prevent double submission
                    toast_success("Exam started! Good luck!")
                    st.rerun()
                else:
                    toast_error("Could not generate questions.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.subheader("📋 Exam Rules")
            st.markdown("""
            <div style="color:#9E9EC0;font-size:0.9rem;line-height:1.8;">
            ⏱️ Timer starts when exam begins<br>
            📝 Answer all questions before submitting<br>
            🔒 Can't change answers after submit<br>
            📊 Results saved to progress tracker<br>
            💡 Review explanations after exam
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    qs = st.session_state.exam_session
    elapsed = int(time.time() - st.session_state.exam_start_time)
    time_limit = st.session_state.get("exam_time_limit", 1800)
    remaining = max(0, time_limit - elapsed)
    mins, secs = divmod(remaining, 60)
    
    # Enhanced timer with alerts
    timer_color = "#FF5252" if remaining < 120 else "#FFB700" if remaining < 300 else "#4ECDC4"
    timer_pulse = "pulse" if remaining < 120 else ""
    
    st.markdown(f"""
    <div class="timer-sticky" style="color:{timer_color};animation:{timer_pulse};font-weight:700;">
        ⏱️ Time Remaining: {mins:02d}:{secs:02d}
        &nbsp;&nbsp;|&nbsp;&nbsp; {len(qs.questions)} Questions
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    </style>""", unsafe_allow_html=True)

    # Show warning toast when time < 5 min
    if remaining < 300 and remaining > 295 and not st.session_state.get("time_warning_shown", False):
        toast_warning("⏰ Less than 5 minutes remaining!")
        st.session_state.time_warning_shown = True

    # Auto-submit when time expires (with race condition protection)
    if remaining <= 0 and not st.session_state.get("exam_locked", False):
        st.session_state.exam_locked = True
        st.session_state.exam_submitted = True
        toast_error("⏰ Time's up! Exam auto-submitted.")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    for i, q in enumerate(qs.questions):
        st.markdown(f"""
        <div class="quiz-question-card">
            <strong>Q{i+1}.</strong> {q["question"]}
        </div>""", unsafe_allow_html=True)

        current_answer = st.session_state.exam_answers.get(i, None)
        options = q.get("options", ["A", "B", "C", "D"])
        option_labels = {opt: opt for opt in options}

        selected = st.radio(
            f"Select answer for Q{i+1}",
            options=options,
            index=options.index(current_answer) if current_answer in options else 0,
            key=f"exam_q_{i}",
            label_visibility="collapsed"
        )
        st.session_state.exam_answers[i] = selected
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,3])
    with col1:
        answered = sum(1 for i in range(len(qs.questions)) if st.session_state.exam_answers.get(i))
        st.info(f"Answered: {answered}/{len(qs.questions)}")
    with col2:
        # Prevent double-submit and allow only when time remains
        submit_disabled = st.session_state.get("exam_locked", False) or remaining <= 0
        if st.button("✅ Submit Exam", width="stretch", type="primary", disabled=submit_disabled):
            st.session_state.exam_locked = True
            st.session_state.exam_submitted = True
            toast_success("Exam submitted successfully!")
            st.rerun()
