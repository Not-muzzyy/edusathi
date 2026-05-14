"""modules/ui_components.py — Premium styled Streamlit UI components."""
import streamlit as st

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }
code, pre { font-family: 'JetBrains Mono', monospace !important; }

/* Hide Streamlit branding but keep sidebar toggle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stSidebarNav"] {display: none !important;}

/* Hide header bar, deploy, and toolbar — but preserve sidebar collapse button */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    border: none !important;
}
[data-testid="stToolbar"] {display: none !important;}
.stDeployButton {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
button[kind="header"] {display: none !important;}

/* Ensure sidebar is visible when it has content */
section[data-testid="stSidebar"][aria-expanded="true"] {
    transform: none !important;
    width: 300px !important;
    min-width: 300px !important;
}

/* Main background with premium gradient */
.main {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #0F0F1A 100%);
    background-attachment: fixed;
}

/* Enhanced Sidebar Glassmorphism */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(26,26,46,0.97) 0%, rgba(22,33,62,0.97) 100%) !important;
    backdrop-filter: blur(24px) saturate(200%);
    -webkit-backdrop-filter: blur(24px) saturate(200%);
    border-right: 1px solid rgba(108,99,255,0.2);
    box-shadow: 4px 0 32px rgba(0,0,0,0.4);
}
section[data-testid="stSidebar"] * { color: #E0E0F0 !important; }
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

/* Premium Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF 0%, #5B54E8 50%, #4ECDC4 100%);
    background-size: 200% 200%;
    animation: gradientShift 4s ease infinite;
    color: white !important;
    border: none;
    border-radius: 16px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 24px rgba(108,99,255,0.4), 0 0 0 0 rgba(108,99,255,0);
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
    transition: left 0.6s;
}
.stButton > button:hover::before {
    left: 100%;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(108,99,255,0.55), 0 0 0 4px rgba(108,99,255,0.12);
}
.stButton > button:active {
    transform: translateY(-1px);
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Enhanced Form Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(108,99,255,0.3) !important;
    border-radius: 14px !important;
    color: #E0E0F0 !important;
    transition: all 0.3s ease;
    padding: 0.7rem 1.1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 4px rgba(108,99,255,0.18) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #6E6E82 !important;
}

/* Premium Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6C63FF 0%, #4ECDC4 50%, #6C63FF 100%) !important;
    background-size: 200% 100%;
    animation: progressGlow 2.5s ease infinite;
    border-radius: 14px;
    box-shadow: 0 0 24px rgba(108,99,255,0.45);
}
@keyframes progressGlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

div[data-testid="stMetricValue"] { color: #6C63FF !important; font-weight: 700; }
div[data-testid="stMetricDelta"] { font-size: 0.8rem; }

/* Premium Glass Card */
.edusathi-card {
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(24px) saturate(200%);
    -webkit-backdrop-filter: blur(24px) saturate(200%);
    border: 1px solid rgba(108,99,255,0.18);
    border-radius: 24px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.edusathi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.6), transparent);
}
.edusathi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 60px rgba(108,99,255,0.25), inset 0 1px 0 rgba(255,255,255,0.12);
    border-color: rgba(108,99,255,0.35);
}

/* Enhanced Glass Container */
.glass-container {
    background: rgba(108,99,255,0.05);
    backdrop-filter: blur(28px) saturate(220%);
    -webkit-backdrop-filter: blur(28px) saturate(220%);
    border: 1px solid rgba(108,99,255,0.22);
    border-radius: 28px;
    padding: 2.25rem;
    margin: 1.5rem 0;
    box-shadow: 0 10px 48px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative;
}
.glass-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 15%;
    right: 15%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(78,205,196,0.5), transparent);
}

/* Premium Metric Card with Glow */
.metric-card {
    background: linear-gradient(145deg, rgba(108,99,255,0.14) 0%, rgba(78,205,196,0.1) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(108,99,255,0.28);
    border-radius: 24px;
    padding: 1.75rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 65%);
    opacity: 0;
    transition: opacity 0.35s ease;
}
.metric-card:hover::before {
    opacity: 1;
}
.metric-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 36px rgba(108,99,255,0.28);
    border-color: rgba(108,99,255,0.4);
}
.metric-card .metric-icon {
    display: block;
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.metric-card .metric-value {
    display: block;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
}
.metric-card .metric-label {
    display: block;
    font-size: 0.9rem;
    color: #9E9EC0;
    margin-top: 0.5rem;
    font-weight: 500;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

/* Enhanced Chat Bubbles */
.chat-user {
    background: linear-gradient(135deg, #6C63FF 0%, #5B54E8 100%);
    color: white;
    border-radius: 24px 24px 8px 24px;
    padding: 1.1rem 1.6rem;
    margin: 0.85rem 0 0.85rem 22%;
    font-size: 0.96rem;
    box-shadow: 0 6px 28px rgba(108,99,255,0.4);
    position: relative;
    animation: slideInRight 0.35s ease;
    line-height: 1.6;
}
.chat-ai {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(108,99,255,0.18);
    color: #E0E0F0;
    border-radius: 24px 24px 24px 8px;
    padding: 1.1rem 1.6rem;
    margin: 0.85rem 22% 0.85rem 0;
    font-size: 0.96rem;
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    position: relative;
    animation: slideInLeft 0.35s ease;
    line-height: 1.6;
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(25px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-25px); }
    to { opacity: 1; transform: translateX(0); }
}
.chat-label-user { 
    text-align: right; 
    color: #9E9EC0; 
    font-size: 0.78rem; 
    margin-bottom: 5px;
    font-weight: 500;
    letter-spacing: 0.4px;
}
.chat-label-ai { 
    color: #9E9EC0; 
    font-size: 0.78rem; 
    margin-bottom: 5px;
    font-weight: 500;
    letter-spacing: 0.4px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.chat-label-ai::before {
    content: '🤖';
    font-size: 0.85rem;
}

/* Enhanced Quiz Question Card */
.quiz-question-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    border-left: 5px solid #6C63FF;
    border-radius: 6px 24px 24px 6px;
    padding: 2rem 2.25rem;
    margin: 1.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
    color: #E0E0F0;
    box-shadow: 0 6px 32px rgba(0,0,0,0.25);
    line-height: 1.65;
}

/* Enhanced Option Buttons */
.option-btn {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(108,99,255,0.22);
    border-radius: 16px;
    padding: 1.15rem 1.4rem;
    margin: 0.6rem 0;
    cursor: pointer;
    width: 100%;
    text-align: left;
    color: #E0E0F0;
    font-size: 1.02rem;
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}
.option-btn:hover { 
    background: rgba(108,99,255,0.14); 
    border-color: #6C63FF;
    transform: translateX(10px);
    box-shadow: 0 6px 24px rgba(108,99,255,0.22);
}
.option-correct { 
    background: rgba(78,205,196,0.18) !important; 
    border-color: #4ECDC4 !important;
    box-shadow: 0 0 28px rgba(78,205,196,0.28);
}
.option-wrong { 
    background: rgba(255,82,82,0.14) !important; 
    border-color: #FF5252 !important;
    box-shadow: 0 0 28px rgba(255,82,82,0.22);
}

/* Success/Error Feedback Cards */
.feedback-success {
    background: linear-gradient(135deg, rgba(78,205,196,0.15) 0%, rgba(78,205,196,0.08) 100%);
    border: 1px solid rgba(78,205,196,0.4);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.feedback-success .icon { font-size: 1.5rem; }
.feedback-success .text { color: #4ECDC4; font-weight: 600; font-size: 1.1rem; }

.feedback-error {
    background: linear-gradient(135deg, rgba(255,82,82,0.15) 0%, rgba(255,82,82,0.08) 100%);
    border: 1px solid rgba(255,82,82,0.4);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.feedback-error .icon { font-size: 1.5rem; }
.feedback-error .text { color: #FF5252; font-weight: 600; font-size: 1.1rem; }

/* Enhanced Flashcard with 3D Effect */
.flashcard-container {
    perspective: 1400px;
    width: 100%;
    height: 260px;
    cursor: pointer;
    margin: 1.5rem 0;
}
.flashcard {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 28px;
}
.flashcard.flipped { transform: rotateY(180deg); }
.flashcard-front, .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2.25rem;
    text-align: center;
    font-size: 1.12rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}
.flashcard-front {
    background: linear-gradient(145deg, rgba(108,99,255,0.22) 0%, rgba(78,205,196,0.12) 100%);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(108,99,255,0.4);
    color: #E0E0F0;
    font-weight: 600;
}
.flashcard-back {
    background: linear-gradient(145deg, rgba(78,205,196,0.18) 0%, rgba(108,99,255,0.12) 100%);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(78,205,196,0.4);
    color: #E0E0F0;
    transform: rotateY(180deg);
}

/* Badge Styling */
.badge {
    display: inline-block;
    padding: 0.3rem 0.95rem;
    border-radius: 28px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.4px;
}
.badge-easy { background: rgba(78,205,196,0.18); color: #4ECDC4; border: 1px solid rgba(78,205,196,0.55); }
.badge-medium { background: rgba(255,183,0,0.18); color: #FFB700; border: 1px solid rgba(255,183,0,0.55); }
.badge-hard { background: rgba(255,82,82,0.18); color: #FF5252; border: 1px solid rgba(255,82,82,0.55); }

/* Timer Sticky Header */
.timer-sticky {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(135deg, rgba(15,15,26,0.98), rgba(26,26,46,0.98));
    backdrop-filter: blur(24px);
    border-bottom: 1px solid rgba(108,99,255,0.28);
    padding: 0.85rem 2.5rem;
    border-radius: 0 0 24px 24px;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #6C63FF;
    box-shadow: 0 6px 32px rgba(0,0,0,0.35);
}

/* Enhanced Page Header */
.page-header {
    padding: 1.75rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(108,99,255,0.18);
    margin-bottom: 2.25rem;
    position: relative;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 140px;
    height: 3px;
    background: linear-gradient(90deg, #6C63FF, #4ECDC4);
    border-radius: 3px;
}
.page-header h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    letter-spacing: -0.5px;
}

/* Enhanced Sidebar User Panel */
.sidebar-user {
    background: linear-gradient(145deg, rgba(108,99,255,0.18) 0%, rgba(78,205,196,0.1) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(108,99,255,0.28);
    border-radius: 22px;
    padding: 1.5rem;
    margin: 1.25rem 0 1.75rem 0;
    text-align: center;
    box-shadow: 0 6px 28px rgba(0,0,0,0.25);
}
.sidebar-user .user-name { 
    font-weight: 700; 
    font-size: 1.1rem; 
    color: #E0E0F0;
    margin-top: 0.6rem;
}
.sidebar-user .user-role { 
    font-size: 0.82rem; 
    color: #9E9EC0; 
    margin-top: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
}
.sidebar-user .user-avatar {
    width: 64px; 
    height: 64px; 
    border-radius: 50%;
    background: linear-gradient(145deg, #6C63FF 0%, #4ECDC4 100%);
    display: flex; 
    align-items: center; 
    justify-content: center;
    font-size: 1.65rem; 
    margin: 0 auto;
    box-shadow: 0 6px 24px rgba(108,99,255,0.45);
    font-weight: 700;
    color: white;
}
.sidebar-user .user-course {
    font-size: 0.78rem;
    color: #78788C;
    margin-top: 5px;
}

/* Navigation Links */
.nav-section {
    margin: 1.25rem 0;
    padding: 0 0.6rem;
}
.nav-section-title {
    font-size: 0.72rem;
    color: #6E6E82;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    font-weight: 600;
    margin-bottom: 0.85rem;
    padding-left: 0.6rem;
}

/* Topic Progress Bar */
.topic-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    height: 12px;
    width: 100%;
    overflow: hidden;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
}
.topic-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #6C63FF, #4ECDC4);
    transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 0 14px rgba(108,99,255,0.45);
}

/* Enhanced Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.025) !important;
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 6px;
    gap: 6px;
    border: 1px solid rgba(108,99,255,0.12);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 12px !important;
    color: #9E9EC0 !important;
    font-weight: 500;
    padding: 0.7rem 1.3rem !important;
    transition: all 0.25s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(108,99,255,0.12) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(108,99,255,0.28), rgba(78,205,196,0.18)) !important;
    color: #E0E0F0 !important;
    box-shadow: 0 3px 12px rgba(108,99,255,0.25);
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.025); border-radius: 5px; }
::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, rgba(108,99,255,0.55), rgba(78,205,196,0.55)); 
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover { 
    background: linear-gradient(180deg, rgba(108,99,255,0.75), rgba(78,205,196,0.75)); 
}

/* Profile Setup Modal */
.profile-setup {
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(28px);
    border: 1px solid rgba(108,99,255,0.28);
    border-radius: 28px;
    padding: 3rem;
    max-width: 500px;
    margin: 2.5rem auto;
    box-shadow: 0 20px 80px rgba(0,0,0,0.45);
}
.profile-setup h2 {
    background: linear-gradient(135deg, #6C63FF, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1.75rem;
}

/* Multi-file upload enhancement */
.upload-zone {
    background: rgba(108,99,255,0.06);
    border: 2px dashed rgba(108,99,255,0.35);
    border-radius: 20px;
    padding: 2.25rem;
    text-align: center;
    transition: all 0.3s ease;
}
.upload-zone:hover {
    border-color: #6C63FF;
    background: rgba(108,99,255,0.12);
}

/* Empty State Styling */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #9E9EC0;
}
.empty-state .icon {
    font-size: 4.5rem;
    margin-bottom: 1.25rem;
    opacity: 0.6;
}
.empty-state h3 {
    color: #E0E0F0;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
}
.empty-state p {
    max-width: 360px;
    margin: 0 auto;
    line-height: 1.65;
}

/* Loading Spinner Override */
.stSpinner > div {
    border-top-color: #6C63FF !important;
}

/* Score Display Cards */
.score-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: conic-gradient(#4ECDC4 var(--score-percent), rgba(255,255,255,0.1) 0);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    box-shadow: 0 0 40px rgba(78,205,196,0.3);
}
.score-ring-inner {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: #1A1A2E;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-ring-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #4ECDC4;
}
.score-ring-label {
    font-size: 0.8rem;
    color: #9E9EC0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Stat Item */
.stat-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 1.25rem;
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    margin: 0.5rem 0;
    transition: all 0.25s ease;
}
.stat-item:hover {
    background: rgba(108,99,255,0.1);
    transform: translateX(5px);
}
.stat-item .stat-icon {
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(108,99,255,0.15);
}
.stat-item .stat-info {
    flex: 1;
}
.stat-item .stat-label {
    font-size: 0.85rem;
    color: #9E9EC0;
}
.stat-item .stat-value {
    font-size: 1.15rem;
    font-weight: 600;
    color: #E0E0F0;
}

/* ═══════════════════════════════════════════════════════════════════════
   PREMIUM ANIMATIONS & ENHANCED GLASSMORPHISM
   ═══════════════════════════════════════════════════════════════════════ */

/* Animated background orbs */
.main::before {
    content: '';
    position: fixed;
    top: -150px;
    right: -150px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatOrb1 15s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
.main::after {
    content: '';
    position: fixed;
    bottom: -100px;
    left: -100px;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(78,205,196,0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatOrb2 18s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes floatOrb1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(-80px, 60px) scale(1.1); }
    50% { transform: translate(-40px, 120px) scale(0.95); }
    75% { transform: translate(30px, 80px) scale(1.05); }
}
@keyframes floatOrb2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(60px, -80px) scale(1.08); }
    66% { transform: translate(100px, -40px) scale(0.92); }
}

/* Fade In Up — page entrance animation */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.92); }
    to { opacity: 1; transform: scale(1); }
}

/* Wave animation for hand icon */
@keyframes wave {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(14deg); }
    50% { transform: rotate(-8deg); }
    75% { transform: rotate(14deg); }
}

/* Pulse glow for important elements */
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(108,99,255,0.3); }
    50% { box-shadow: 0 0 40px rgba(108,99,255,0.6), 0 0 60px rgba(78,205,196,0.2); }
}

/* Shimmer loading effect */
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Rotate animation */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Animated gradient border */
@keyframes borderGlow {
    0%, 100% { border-color: rgba(108,99,255,0.3); }
    50% { border-color: rgba(78,205,196,0.5); }
}

/* Hero section entrance */
.hero-section {
    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.hero-section .hero-icon {
    animation: fadeInScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
}
.hero-section .hero-title {
    animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
}
.hero-section .hero-subtitle {
    animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both;
}

/* Staggered entrance for cards */
.glass-container { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both; }
.edusathi-card { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both; }
.metric-card { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both; }

/* Enhanced glass-container with animated border */
.glass-container {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both, borderGlow 4s ease-in-out infinite;
}

/* Premium Login Card */
.login-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(40px) saturate(200%);
    -webkit-backdrop-filter: blur(40px) saturate(200%);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 32px;
    padding: 2.75rem;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.4),
        0 0 0 1px rgba(255,255,255,0.05) inset,
        0 1px 0 rgba(255,255,255,0.08) inset;
    animation: fadeInScale 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    position: relative;
    overflow: hidden;
}
.login-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 10%;
    right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.6), rgba(78,205,196,0.4), transparent);
}
.login-card::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 20%, rgba(108,99,255,0.06) 0%, transparent 50%);
    pointer-events: none;
}

/* Sidebar SVG icon nav links */
.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.65rem 1rem;
    border-radius: 14px;
    color: #C0C0D8 !important;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.92rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 3px 0;
    cursor: pointer;
}
.nav-link:hover {
    background: rgba(108,99,255,0.12);
    color: #E0E0F0 !important;
    transform: translateX(4px);
}
.nav-link svg {
    opacity: 0.7;
    transition: opacity 0.25s ease;
}
.nav-link:hover svg {
    opacity: 1;
}

/* Quick Action Card */
.quick-action {
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(108,99,255,0.18);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.quick-action::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.5), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.quick-action:hover::before { opacity: 1; }
.quick-action:hover {
    transform: translateY(-6px);
    border-color: rgba(108,99,255,0.4);
    box-shadow: 0 16px 48px rgba(108,99,255,0.2);
}
.quick-action .qa-icon {
    margin-bottom: 0.75rem;
    animation: fadeInScale 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.quick-action .qa-label {
    color: #C0C0D8;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.3px;
}

/* Animated metric card icon */
.metric-card .metric-icon svg {
    filter: drop-shadow(0 2px 8px rgba(108,99,255,0.4));
}

/* Page header with SVG support */
.page-header {
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.page-header h1 {
    display: flex;
    align-items: center;
    gap: 14px;
}
.page-header h1 svg {
    filter: drop-shadow(0 2px 12px rgba(108,99,255,0.5));
}

/* Sidebar user panel entrance */
.sidebar-user {
    animation: fadeInScale 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {f'<p style="color:#9E9EC0;margin:0.6rem 0 0 0;font-size:1.02rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def card(content_html: str):
    st.markdown(f'<div class="edusathi-card">{content_html}</div>', unsafe_allow_html=True)


def glass_container(content_html: str):
    st.markdown(f'<div class="glass-container">{content_html}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, col=None, icon: str = ""):
    icon_html = f'<div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>' if icon else ''
    html = f"""
    <div style="background:linear-gradient(145deg,rgba(108,99,255,0.14),rgba(78,205,196,0.1));
        backdrop-filter:blur(20px);border:1px solid rgba(108,99,255,0.28);border-radius:24px;
        padding:1.75rem 2rem;text-align:center;position:relative;overflow:hidden;
        font-family:'Space Grotesk',sans-serif;
        transition:all 0.35s cubic-bezier(0.4,0,0.2,1);">
        {icon_html}
        <div style="font-size:2.8rem;font-weight:800;
            background:linear-gradient(135deg,#6C63FF,#4ECDC4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;line-height:1.15;">{value}</div>
        <div style="font-size:0.9rem;color:#9E9EC0;margin-top:0.5rem;font-weight:500;
            letter-spacing:0.6px;text-transform:uppercase;">{label}</div>
    </div>"""
    if col:
        with col:
            st.html(html)
    else:
        st.html(html)


def badge(text: str, level: str = "medium"):
    st.markdown(f'<span class="badge badge-{level}">{text}</span>', unsafe_allow_html=True)


def styled_button(label: str, key: str = None, full_width: bool = True):
    """Return a styled button."""
    return st.button(label, key=key, width="stretch" if full_width else "content")


def sidebar_user_panel(name: str, email: str, role: str, course: str = "", semester: str = ""):
    initials = "".join(w[0].upper() for w in name.split()[:2])
    role_icons = {"admin": "★", "faculty": "◆", "student": "●"}
    icon = role_icons.get(role, "●")
    course_info = f'<div class="user-course">{course} {("• Sem " + semester) if semester else ""}</div>' if course else ""
    st.sidebar.markdown(f"""
    <div class="sidebar-user">
        <div class="user-avatar">{initials}</div>
        <div class="user-name">{name}</div>
        <div class="user-role"><span>{icon}</span> {role.capitalize()}</div>
        {course_info}
    </div>
    """, unsafe_allow_html=True)


def nav_section(title: str):
    st.sidebar.markdown(f'<div class="nav-section-title">{title}</div>', unsafe_allow_html=True)


def topic_progress_bar(topic: str, mastery: float):
    pct = int(mastery * 100)
    color = "#4ECDC4" if pct >= 70 else "#FFB700" if pct >= 40 else "#FF5252"
    st.markdown(f"""
    <div style="margin:0.85rem 0;">
        <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
            <span style="color:#E0E0F0;font-size:0.94rem;font-weight:500;">{topic}</span>
            <span style="color:{color};font-weight:700;font-size:0.94rem;">{pct}%</span>
        </div>
        <div class="topic-bar-bg">
            <div class="topic-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}88);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def chat_message(content: str, is_user: bool = False, name: str = ""):
    """Render a styled chat message bubble."""
    if is_user:
        label = name if name else "You"
        st.markdown(f'<div class="chat-label-user">{label}</div><div class="chat-user">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-label-ai">EduSathi AI</div><div class="chat-ai">{content}</div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, description: str):
    """Render a consistent empty state."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def success_feedback(message: str):
    """Render success feedback."""
    st.markdown(f"""
    <div class="feedback-success">
        <span class="icon">✓</span>
        <span class="text">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def error_feedback(message: str):
    """Render error feedback."""
    st.markdown(f"""
    <div class="feedback-error">
        <span class="icon">✗</span>
        <span class="text">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def stat_item(icon: str, label: str, value: str):
    """Render a stat item row."""
    st.markdown(f"""
    <div class="stat-item">
        <div class="stat-icon">{icon}</div>
        <div class="stat-info">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the full sidebar with branding, user panel, role-based nav, and logout.
    Call this from every page to ensure the sidebar is always visible."""
    from modules import icons

    if "user" not in st.session_state or st.session_state.user is None:
        return

    user = st.session_state.user
    course = st.session_state.get("user_course", "")
    semester = st.session_state.get("user_semester", "")

    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:1.25rem 0 0.75rem 0;display:flex;align-items:center;justify-content:center;gap:10px;">
            {icons.graduation_cap(32, "#6C63FF")}
            <span style="font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#6C63FF,#4ECDC4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                letter-spacing:-0.5px;">EduSathi</span>
        </div>
        """, unsafe_allow_html=True)

        sidebar_user_panel(user["name"], user["email"], user["role"], course, semester)

        # Navigation sections with Material icons based on role
        if user["role"] == "student":
            nav_section("LEARNING")
            st.page_link("pages/1_Dashboard.py",       label="Dashboard",        icon=":material/dashboard:")
            st.page_link("pages/2_Chat_Tutor.py",      label="Chat Tutor",       icon=":material/chat:")
            st.page_link("pages/3_Quiz_Mode.py",       label="Quiz Mode",        icon=":material/quiz:")

            nav_section("PRACTICE")
            st.page_link("pages/4_Exam_Simulation.py", label="Exam Simulation",  icon=":material/timer:")
            st.page_link("pages/5_Flashcards.py",      label="Flashcards",       icon=":material/style:")

            nav_section("ANALYTICS")
            st.page_link("pages/6_Progress_Tracker.py",label="Progress Tracker", icon=":material/trending_up:")

        elif user["role"] == "faculty":
            nav_section("FACULTY DASHBOARD")
            st.page_link("pages/8_Faculty_Panel.py", label="Faculty Panel",   icon=":material/school:")

        elif user["role"] == "admin":
            nav_section("ADMINISTRATION")
            st.page_link("pages/7_Admin_Panel.py", label="Admin Panel",     icon=":material/admin_panel_settings:")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div style="padding:0 0.5rem;">', unsafe_allow_html=True)
        if st.button("Logout", width="stretch", icon=":material/logout:", key="sidebar_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

