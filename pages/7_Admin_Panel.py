"""pages/7_Admin_Panel.py"""
import streamlit as st
import pandas as pd
import pdfplumber, io

st.set_page_config(page_title="Admin Panel — EduSathi", page_icon="🛠️", layout="wide")

from modules.ui_components import inject_css, page_header, metric_card, render_sidebar
from modules.auth import (get_all_users, update_user_role, delete_user,
                           get_all_quiz_attempts, save_document_record)
from modules.rag_pipeline import ingest_pdf
from modules.llm_client import analyze_question_paper

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "admin":
    st.error("Access denied. Admin role required.")
    st.stop()

page_header("◆ Admin Panel", f"Role: {user['role'].capitalize()}")

tab1, tab2, tab3, tab4 = st.tabs([
    "User Management",
    "Analytics",
    "Question Papers",
    "Paper Analysis"
])

with tab1:
    if user["role"] != "admin":
        st.info("User management is admin-only.")
    else:
        users = get_all_users()
        c1, c2, c3 = st.columns(3)
        metric_card("Total Users", str(len(users)), c1)
        metric_card("Students", str(sum(1 for u in users if u["role"]=="student")), c2)
        metric_card("Faculty", str(sum(1 for u in users if u["role"]=="faculty")), c3)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("👤 User List")
        search = st.text_input("Search by name or email", placeholder="Type to filter...")
        filtered_users = [u for u in users if search.lower() in u["name"].lower() or search.lower() in u["email"].lower()] if search else users

        for u in filtered_users:
            if u["id"] == user["id"]:
                continue
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"""
                <div style="padding:0.5rem 0;">
                    <div style="color:#E0E0F0;font-weight:500;">{u['name']}</div>
                    <div style="color:#9E9EC0;font-size:0.8rem;">{u['email']}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='color:#9E9EC0;padding-top:0.7rem;'>{u['created_at'][:10] if u['created_at'] else ''}</div>", unsafe_allow_html=True)
            with col3:
                new_role = st.selectbox("Role", ["student", "faculty", "admin"],
                                        index=["student","faculty","admin"].index(u["role"]),
                                        key=f"role_{u['id']}", label_visibility="collapsed")
                if new_role != u["role"]:
                    update_user_role(u["id"], new_role)
                    st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_{u['id']}",
                             help=f"Delete {u['name']}"):
                    delete_user(u["id"])
                    st.rerun()
            st.markdown("<hr style='border-color:rgba(108,99,255,0.1);'>", unsafe_allow_html=True)

with tab2:
    attempts = get_all_quiz_attempts()
    c1, c2, c3 = st.columns(3)
    metric_card("Total Attempts", str(len(attempts)), c1)
    if attempts:
        avg = sum(a["score"]/a["total_questions"]*100 for a in attempts) / len(attempts)
        metric_card("Platform Avg", f"{round(avg,1)}%", c2)
    else:
        metric_card("Platform Avg", "—", c2)
    unique_students = len(set(a["user_id"] for a in attempts))
    metric_card("Active Students", str(unique_students), c3)

    st.markdown("<br>", unsafe_allow_html=True)
    if attempts:
        df = pd.DataFrame(attempts)
        df["score_pct"] = (df["score"] / df["total_questions"] * 100).round(1)
        subj_filter = st.selectbox("Filter by Subject", ["All"] + sorted(df["subject"].unique().tolist()))
        if subj_filter != "All":
            df = df[df["subject"] == subj_filter]
        display_df = df[["name","email","subject","topic","score","total_questions","score_pct","difficulty_level","attempted_at"]].rename(columns={
            "name":"Student","email":"Email","subject":"Subject","topic":"Topic",
            "score":"Score","total_questions":"Total","score_pct":"Score %",
            "difficulty_level":"Difficulty","attempted_at":"Date"
        })
        st.dataframe(display_df, width="stretch", hide_index=True)
    else:
        st.info("No quiz attempts yet.")

with tab3:
    if user["role"] != "admin":
        st.info("Paper upload is admin-only.")
    else:
        st.subheader("📤 Upload VSKUB Question Papers")
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        paper_subject = st.text_input("Paper Subject Tag", placeholder="e.g. BCA Semester 4 OS")
        paper_file = st.file_uploader("Upload Question Paper PDF", type=["pdf"], key="paper_upload")
        if paper_file and st.button("Process Question Paper"):
            with st.spinner("Processing..."):
                result = ingest_pdf(paper_file.read(), paper_file.name, user["id"], paper_subject or "question_paper")
            if result["success"]:
                save_document_record(user["id"], paper_file.name, paper_subject or "question_paper", result["store_path"])
                st.success(f"✅ Question paper processed! {result['chunk_count']} chunks indexed.")
            else:
                st.error(result["error"])
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.subheader("🔍 Analyze Question Paper Topics")
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    analysis_file = st.file_uploader("Upload Question Paper for Analysis", type=["pdf"], key="analysis_upload")
    n_topics = st.slider("Number of Top Topics", 5, 20, 10)
    if analysis_file and st.button("🔍 Analyze Topics"):
        with st.spinner("Extracting and analyzing topics — reading full paper..."):
            with pdfplumber.open(io.BytesIO(analysis_file.read())) as pdf:
                text = "".join([p.extract_text() or "" for p in pdf.pages])
            if text.strip():
                topics = analyze_question_paper(text, n=n_topics)
            else:
                topics = []
        if topics:
            st.subheader("📊 Frequently Asked Topics")
            # Find max frequency for progress bar scaling
            max_freq = max(t.get("frequency", 1) for t in topics) if topics else 1
            for i, t in enumerate(topics):
                imp = t.get("importance","medium").lower()
                color = "#4ECDC4" if imp=="high" else "#FFB700" if imp=="medium" else "#9E9EC0"
                freq = t.get("frequency", 1)
                bar_pct = min(int(freq / max_freq * 100), 100)
                
                subtopics_html = ""
                subtopics = t.get("subtopics", [])
                if subtopics:
                    tags = " ".join(
                        f'<span style="display:inline-block;padding:0.15rem 0.5rem;background:rgba(78,205,196,0.15);'
                        f'border-radius:8px;font-size:0.72rem;color:#4ECDC4;margin:0.15rem 0.2rem 0 0;">{s}</span>'
                        for s in subtopics[:5]
                    )
                    subtopics_html = f'<div style="margin-top:0.4rem;">{tags}</div>'
                
                qtypes_html = ""
                qtypes = t.get("question_types", [])
                if qtypes:
                    qt_tags = ", ".join(qtypes[:4])
                    qtypes_html = f'<span style="color:#9E9EC0;font-size:0.72rem;margin-left:0.5rem;">({qt_tags})</span>'
                
                st.markdown(f"""
                <div style="padding:0.9rem 1.2rem;background:rgba(255,255,255,0.04);border-radius:14px;
                    margin:0.5rem 0;border-left:4px solid {color};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#E0E0F0;font-weight:600;font-size:0.95rem;">#{i+1} {t.get("topic","")}</span>
                            {qtypes_html}
                        </div>
                        <div style="text-align:right;">
                            <span style="color:{color};font-weight:700;font-size:0.85rem;
                                text-transform:uppercase;">{t.get("importance","medium")}</span>
                            <span style="color:#9E9EC0;font-size:0.78rem;margin-left:0.5rem;">
                                ×{freq}
                            </span>
                        </div>
                    </div>
                    <div style="margin-top:0.5rem;background:rgba(255,255,255,0.06);border-radius:6px;height:6px;overflow:hidden;">
                        <div style="width:{bar_pct}%;height:100%;background:linear-gradient(90deg,{color},rgba(108,99,255,0.8));
                            border-radius:6px;transition:width 0.4s ease;"></div>
                    </div>
                    {subtopics_html}
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("Could not extract topics. Ensure the PDF has readable text and your API key is configured.")
    st.markdown('</div>', unsafe_allow_html=True)

