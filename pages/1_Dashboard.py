"""pages/1_Dashboard.py — Premium Dashboard with enhanced visualizations."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dashboard — EduSathi", page_icon="📊", layout="wide")

from modules.ui_components import inject_css, page_header, metric_card, empty_state, render_sidebar
from modules.progress_tracker import get_dashboard_stats
from modules.auth import get_user_documents
from modules import icons

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()
page_header("Dashboard", f"Welcome back, {user['name']}! Here's your study overview.")

stats = get_dashboard_stats(user["id"])
docs  = get_user_documents(user["id"])

# Metric cards row with SVG icons
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
metric_card("Total Quizzes", str(stats["total_quizzes"]), c1, icon=icons.clipboard_check(28, "#6C63FF"))
metric_card("Avg Score", f"{stats['avg_score_pct']}%", c2, icon=icons.target(28, "#4ECDC4"))
metric_card("Overall Mastery", f"{stats['overall_mastery']}%", c3, icon=icons.trophy(28, "#FFB700"))
metric_card("Docs Uploaded", str(len(docs)), c4, icon=icons.book_open(28, "#FF5252"))

st.markdown("<br><br>", unsafe_allow_html=True)
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>{icons.bar_chart(22, '#6C63FF')} Topic Mastery Overview</h4>", unsafe_allow_html=True)
    progress = stats.get("progress", [])
    if progress:
        df = pd.DataFrame(progress)
        df["mastery_pct"] = (df["mastery_score"] * 100).round(1)
        df["label"] = df["subject"] + " — " + df["topic"]
        fig = px.bar(
            df, x="mastery_pct", y="label", orientation="h",
            color="mastery_pct",
            color_continuous_scale=["#FF5252", "#FFB700", "#4ECDC4"],
            range_color=[0, 100],
            labels={"mastery_pct": "Mastery %", "label": ""},
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=max(300, len(df) * 55),
            font=dict(color="#9E9EC0", size=12)
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
    else:
        empty_state(icons.bar_chart(48, "#6C63FF"), "No Progress Data Yet", "Complete quizzes to see your topic mastery breakdown here.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>{icons.trending_up(22, '#4ECDC4')} Score Trend</h4>", unsafe_allow_html=True)
    history = stats.get("history", [])
    if history:
        df_h = pd.DataFrame(history)
        df_h["score_pct"] = (df_h["score"] / df_h["total_questions"] * 100).round(1)
        df_h["quiz_num"] = range(1, len(df_h) + 1)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_h["quiz_num"][::-1], y=df_h["score_pct"][::-1],
            mode="lines+markers",
            line=dict(color="#6C63FF", width=3, shape="spline"),
            marker=dict(color="#4ECDC4", size=10, line=dict(width=2, color="#0F0F1A")),
            fill="tozeroy",
            fillcolor="rgba(108,99,255,0.18)"
        ))
        fig2.add_hline(y=70, line_dash="dash", line_color="rgba(255,183,0,0.5)",
                       annotation_text="Target: 70%", annotation_position="right",
                       annotation_font_color="#FFB700")
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Quiz #", color="#9E9EC0", gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(title="Score %", color="#9E9EC0", range=[0,105], gridcolor="rgba(255,255,255,0.06)"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            font=dict(color="#9E9EC0", size=11)
        )
        st.plotly_chart(fig2, width="stretch")
    else:
        empty_state(icons.trending_up(48, "#4ECDC4"), "No Quiz History", "Complete quizzes to track your score progression!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col_w, col_s = st.columns(2)

with col_w:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>{icons.alert_triangle(22, '#FF5252')} Weak Topics (Mastery &lt; 50%)</h4>", unsafe_allow_html=True)
    weak = stats.get("weak_topics", [])
    if weak:
        for w in weak:
            pct = int(w["mastery_score"] * 100)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                padding:0.9rem 1.4rem;background:rgba(255,82,82,0.08);border-radius:14px;margin:8px 0;
                border-left:4px solid #FF5252;transition:all 0.25s ease;">
                <div>
                    <span style="color:#E0E0F0;font-weight:600;font-size:0.95rem;">{w['topic']}</span>
                    <span style="color:#9E9EC0;font-size:0.82rem;margin-left:8px;">{w['subject']}</span>
                </div>
                <span style="color:#FF5252;font-weight:700;font-size:1.1rem;">{pct}%</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:2.5rem;color:#4ECDC4;">
            <div style="margin-bottom:0.6rem;">{icons.check_circle(36, "#4ECDC4")}</div>
            <p style="margin:0;font-weight:500;">No weak topics! Keep up the excellent work.</p>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>{icons.star(22, '#FFB700')} Strong Topics (Mastery ≥ 80%)</h4>", unsafe_allow_html=True)
    strong = stats.get("strong_topics", [])
    if strong:
        for s in strong:
            pct = int(s["mastery_score"] * 100)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                padding:0.9rem 1.4rem;background:rgba(78,205,196,0.08);border-radius:14px;margin:8px 0;
                border-left:4px solid #4ECDC4;transition:all 0.25s ease;">
                <div>
                    <span style="color:#E0E0F0;font-weight:600;font-size:0.95rem;">{s['topic']}</span>
                    <span style="color:#9E9EC0;font-size:0.82rem;margin-left:8px;">{s['subject']}</span>
                </div>
                <span style="color:#4ECDC4;font-weight:700;font-size:1.1rem;">{pct}%</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:2.5rem;color:#9E9EC0;">
            <div style="margin-bottom:0.6rem;">{icons.target(36, "#9E9EC0")}</div>
            <p style="margin:0;">Score 80%+ on quizzes to master topics!</p>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Quick actions section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown(f"<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>{icons.lightning(22, '#FFB700')} Quick Actions</h4>", unsafe_allow_html=True)

qa1, qa2, qa3, qa4 = st.columns(4)
with qa1:
    if st.button("Chat Tutor", width="stretch", icon=":material/chat:"):
        st.switch_page("pages/2_Chat_Tutor.py")
with qa2:
    if st.button("Start Quiz", width="stretch", icon=":material/quiz:"):
        st.switch_page("pages/3_Quiz_Mode.py")
with qa3:
    if st.button("Exam Mode", width="stretch", icon=":material/timer:"):
        st.switch_page("pages/4_Exam_Simulation.py")
with qa4:
    if st.button("Flashcards", width="stretch", icon=":material/style:"):
        st.switch_page("pages/5_Flashcards.py")
st.markdown('</div>', unsafe_allow_html=True)
