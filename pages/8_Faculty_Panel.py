"""pages/8_Faculty_Panel.py"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Faculty Panel — EduSathi", page_icon="👨‍🏫", layout="wide")

from modules.ui_components import inject_css, page_header, metric_card, render_sidebar
from modules.auth import get_all_quiz_attempts

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "faculty":
    st.error("Access denied. Faculty role required.")
    st.stop()

page_header("◆ Faculty Panel", f"Welcome back, Prof. {user['name']}!")

tab1, tab2 = st.tabs(["Student Progress", "Course Management"])

with tab1:
    st.subheader("📈 Student Analytics")
    attempts = get_all_quiz_attempts()
    c1, c2 = st.columns(2)
    metric_card("Total Quizzes Attempted", str(len(attempts)), c1)
    unique_students = len(set(a["user_id"] for a in attempts))
    metric_card("Active Students", str(unique_students), c2)

    st.markdown("<br>", unsafe_allow_html=True)
    if attempts:
        df = pd.DataFrame(attempts)
        df["score_pct"] = (df["score"] / df["total_questions"] * 100).round(1)
        subj_filter = st.selectbox("Filter by Subject", ["All"] + sorted(df["subject"].unique().tolist()))
        if subj_filter != "All":
            df = df[df["subject"] == subj_filter]
        
        display_df = df[["name", "email", "subject", "topic", "score_pct", "attempted_at"]].rename(columns={
            "name": "Student", "email": "Email", "subject": "Subject", "topic": "Topic",
            "score_pct": "Score %", "attempted_at": "Date"
        })
        st.dataframe(display_df, width="stretch", hide_index=True)
    else:
        st.info("No quiz attempts yet from students.")

with tab2:
    st.subheader("📚 Course Materials")
    st.info("Feature coming soon: Upload course materials directly to student dashboards.")
