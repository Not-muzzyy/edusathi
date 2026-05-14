"""pages/6_Progress_Tracker.py — Enhanced progress analytics and reports."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Progress Tracker — EduSathi", page_icon="📈", layout="wide")

from modules.ui_components import inject_css, page_header, metric_card, topic_progress_bar, empty_state, render_sidebar
from modules.progress_tracker import get_dashboard_stats
from modules.report_generator import generate_performance_report

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()
page_header("◐ Progress Tracker", "Track your learning journey and export reports")

stats = get_dashboard_stats(user["id"])

st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
metric_card("Total Quizzes", str(stats["total_quizzes"]), c1, icon="📝")
metric_card("Avg Score", f"{stats['avg_score_pct']}%", c2, icon="🎯")
metric_card("Overall Mastery", f"{stats['overall_mastery']}%", c3, icon="🏆")
metric_card("Topics Studied", str(len(stats.get("progress", []))), c4, icon="📚")

st.markdown("<br><br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Topic Mastery", "📋 Quiz History", "📈 Trends", "📄 Export Report"])

with tab1:
    progress = stats.get("progress", [])
    if progress:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        subjects = list(set(p["subject"] for p in progress))
        sel_sub = st.selectbox("🏷️ Filter by Subject", ["All Subjects"] + subjects)
        filtered = progress if sel_sub == "All Subjects" else [p for p in progress if p["subject"] == sel_sub]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for p in sorted(filtered, key=lambda x: x["mastery_score"], reverse=True):
            topic_progress_bar(f"{p['subject']} — {p['topic']}", p["mastery_score"])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        empty_state("📊", "No Progress Data Yet", "Complete quizzes to track your topic mastery!")

with tab2:
    history = stats.get("history", [])
    if history:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        df = pd.DataFrame(history)
        df["score_pct"] = (df["score"] / df["total_questions"] * 100).round(1)
        df["Date"] = pd.to_datetime(df["attempted_at"]).dt.strftime("%Y-%m-%d %H:%M")
        display_cols = ["Date", "subject", "topic", "score", "total_questions", "score_pct", "difficulty_level"]
        display_df = df[display_cols].rename(columns={
            "subject": "Subject", "topic": "Topic",
            "score": "Score", "total_questions": "Total",
            "score_pct": "Percentage %", "difficulty_level": "Difficulty"
        })
        
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Percentage %": st.column_config.ProgressColumn(
                    "Percentage %",
                    help="Quiz score percentage",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                )
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        empty_state("📋", "No Quiz History Yet", "Take your first quiz to see your history here!")

with tab3:
    history = stats.get("history", [])
    if len(history) >= 2:
        df_h = pd.DataFrame(history)
        df_h["score_pct"] = (df_h["score"] / df_h["total_questions"] * 100).round(1)
        df_h = df_h[::-1].reset_index(drop=True)
        df_h["quiz_num"] = range(1, len(df_h) + 1)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;'>📈 Score Over Time</h4>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_h["quiz_num"], y=df_h["score_pct"],
                mode="lines+markers",
                line=dict(color="#6C63FF", width=3, shape="spline"),
                marker=dict(color="#4ECDC4", size=10, line=dict(width=2, color="#0F0F1A")),
                fill="tozeroy", fillcolor="rgba(108,99,255,0.12)"
            ))
            fig.add_hline(y=70, line_dash="dash", line_color="#FFB700",
                          annotation_text="70% target", annotation_position="right",
                          annotation_font_color="#FFB700")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="Quiz #", color="#9E9EC0", gridcolor="rgba(255,255,255,0.06)"),
                yaxis=dict(title="Score %", color="#9E9EC0", range=[0,105], gridcolor="rgba(255,255,255,0.06)"),
                height=300, margin=dict(l=10,r=10,t=10,b=10),
                font=dict(color="#9E9EC0", size=11)
            )
            st.plotly_chart(fig, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_t2:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;'>🎯 Difficulty Distribution</h4>", unsafe_allow_html=True)
            diff_counts = df_h["difficulty_level"].value_counts().reset_index()
            diff_counts.columns = ["Difficulty", "Count"]
            colors_map = {"easy":"#4ECDC4","medium":"#FFB700","hard":"#FF5252","exam":"#6C63FF"}
            fig2 = px.pie(diff_counts, values="Count", names="Difficulty",
                          color="Difficulty", color_discrete_map=colors_map,
                          template="plotly_dark")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(l=10,r=10,t=10,b=10), showlegend=True,
                font=dict(color="#9E9EC0", size=11)
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional analytics
        st.markdown("<br>", unsafe_allow_html=True)
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;'>📚 Subject Performance</h4>", unsafe_allow_html=True)
            if "subject" in df_h.columns:
                subj_perf = df_h.groupby("subject")["score_pct"].mean().reset_index()
                subj_perf.columns = ["Subject", "Avg Score %"]
                subj_perf = subj_perf.sort_values("Avg Score %", ascending=False)
                for _, row in subj_perf.iterrows():
                    pct = row["Avg Score %"]
                    color = "#4ECDC4" if pct >= 70 else "#FFB700" if pct >= 50 else "#FF5252"
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.85rem 1.25rem;background:rgba(255,255,255,0.04);border-radius:12px;margin:6px 0;">
                        <span style="color:#E0E0F0;font-weight:500;">{row["Subject"]}</span>
                        <span style="color:{color};font-weight:700;font-size:1.05rem;">{pct:.1f}%</span>
                    </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_a2:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;'>🔥 Recent Activity</h4>", unsafe_allow_html=True)
            recent = df_h.head(5)
            for _, row in recent.iterrows():
                pct = row["score_pct"]
                color = "#4ECDC4" if pct >= 70 else "#FFB700" if pct >= 50 else "#FF5252"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:0.85rem 1.25rem;background:rgba(255,255,255,0.04);border-radius:12px;margin:6px 0;">
                    <div>
                        <div style="color:#E0E0F0;font-weight:500;font-size:0.95rem;">{row["topic"][:25]}</div>
                        <div style="color:#9E9EC0;font-size:0.8rem;">{row["subject"]}</div>
                    </div>
                    <span style="color:{color};font-weight:700;font-size:1.05rem;">{pct:.0f}%</span>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        empty_state("📈", "More Data Needed", "Complete at least 2 quizzes to see trend charts and analytics.")

with tab4:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1rem 0;font-weight:600;'>📄 Performance Report</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#9E9EC0;margin-bottom:1.5rem;line-height:1.7;">
        Export a comprehensive PDF report with your topic mastery, quiz history, and overall statistics.
        Perfect for faculty review, portfolio building, or personal tracking.
    </div>""", unsafe_allow_html=True)
    
    # Report preview
    st.markdown("""
    <div style="background:rgba(108,99,255,0.08);border-radius:14px;padding:1.25rem;margin-bottom:1.5rem;
        border:1px solid rgba(108,99,255,0.2);">
        <div style="color:#E0E0F0;font-weight:600;margin-bottom:0.75rem;">📋 Report includes:</div>
        <div style="color:#9E9EC0;font-size:0.92rem;line-height:1.8;">
            ✓ Overall statistics and summary<br>
            ✓ Topic-wise mastery breakdown<br>
            ✓ Recent quiz history (last 10)<br>
            ✓ Performance trends
        </div>
    </div>""", unsafe_allow_html=True)

    if st.button("📥 Generate & Download Report", width="stretch"):
        with st.spinner("🔄 Generating PDF report..."):
            try:
                pdf_bytes = generate_performance_report(user["name"], stats)
            except Exception as e:
                pdf_bytes = None
                st.error(f"❌ Error generating report: {e}")
        
        if pdf_bytes:
            st.download_button(
                "⬇️ Download Report PDF",
                data=pdf_bytes,
                file_name=f"edusathi_report_{user['name'].replace(' ','_')}.pdf",
                mime="application/pdf",
                width="stretch"
            )
            st.success("✅ Report generated successfully!")
        elif pdf_bytes == b"":
            st.error("❌ Could not generate report. Ensure ReportLab is installed correctly.")
    st.markdown('</div>', unsafe_allow_html=True)
