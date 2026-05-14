"""app.py — EduSathi entry point."""
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="EduSathi",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.auth import init_db, login_user, register_user
from modules.ui_components import inject_css, sidebar_user_panel, nav_section
from modules.modern_ui import validate_email, validate_password, toast_success, toast_error
from modules import icons

inject_css()
init_db()

# Hide sidebar entirely when not logged in
if "user" not in st.session_state or st.session_state.user is None:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        button[data-testid="stSidebarCollapsedControl"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_session" not in st.session_state:
    st.session_state.quiz_session = None
if "exam_session" not in st.session_state:
    st.session_state.exam_session = None
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False
if "user_course" not in st.session_state:
    st.session_state.user_course = ""
if "user_semester" not in st.session_state:
    st.session_state.user_semester = ""

def login_page():
    st.markdown(f"""
    <div class="hero-section" style="text-align:center;padding:2.5rem 0 1.5rem 0;">
        <div class="hero-icon" style="margin-bottom:0.75rem;">
            {icons.graduation_cap(56, "#6C63FF")}
        </div>
        <h1 class="hero-title" style="font-size:3.2rem;font-weight:800;background:linear-gradient(135deg,#6C63FF,#4ECDC4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
            margin:0;letter-spacing:-1px;">
            EduSathi
        </h1>
        <p class="hero-subtitle" style="color:#9E9EC0;font-size:1.15rem;margin:0.75rem 0 0 0;">AI-Powered Study Companion for VSKUB Students</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            email = st.text_input("Email", key="li_email", placeholder="student@vskub.ac.in")
            password = st.text_input("Password", type="password", key="li_pass", placeholder="Enter your password")
            
            # Show validation feedback
            if email:
                is_valid, msg = validate_email(email)
                icon_svg = icons.check_circle(14, "#4ECDC4") if is_valid else icons.x_circle(14, "#FF5252")
                color = "#4ECDC4" if is_valid else "#FF5252"
                st.markdown(f'<p style="color:{color};font-size:0.8rem;margin:-0.5rem 0 0.5rem 0;display:flex;align-items:center;gap:6px;">{icon_svg} {msg}</p>', 
                           unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In", width="stretch"):
                if email and password:
                    result = login_user(email, password)
                    if result["success"]:
                        st.session_state.user = result["user"]
                        st.session_state.profile_complete = False
                        toast_success(f"Welcome back, {result['user']['name']}!")
                        st.rerun()
                    else:
                        toast_error(result["error"])
                else:
                    toast_error("Please enter email and password.")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            name = st.text_input("Full Name", key="reg_name", placeholder="Your full name")
            email2 = st.text_input("Email", key="reg_email", placeholder="student@vskub.ac.in")
            pwd2 = st.text_input("Password (min 8 chars)", type="password", key="reg_pass")
            role = st.selectbox("Role", ["student", "faculty", "admin"], key="reg_role")
            
            # Show real-time validation
            validation_msgs = []
            if email2:
                is_valid, msg = validate_email(email2)
                validation_msgs.append((msg, is_valid))
            if pwd2:
                is_valid, msg = validate_password(pwd2)
                validation_msgs.append((msg, is_valid))
            
            if validation_msgs:
                for msg, is_valid in validation_msgs:
                    icon_svg = icons.check_circle(14, "#4ECDC4") if is_valid else icons.alert_triangle(14, "#FFB700")
                    color = "#4ECDC4" if is_valid else "#FFB700"
                    st.markdown(f'<p style="color:{color};font-size:0.8rem;margin:0.25rem 0;display:flex;align-items:center;gap:6px;">{icon_svg} {msg}</p>', 
                               unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account", width="stretch"):
                if name and email2 and pwd2:
                    is_email_valid, _ = validate_email(email2)
                    is_pwd_valid, _ = validate_password(pwd2)
                    
                    if not is_email_valid:
                        toast_error("Invalid email format.")
                    elif not is_pwd_valid:
                        toast_error("Password must be 8+ chars with uppercase, lowercase, and numbers.")
                    else:
                        result = register_user(name, email2, pwd2, role)
                        if result["success"]:
                            toast_success("Account created! Please sign in.")
                        else:
                            toast_error(result["error"])
                else:
                    toast_error("Fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)


def profile_setup_page():
    """Ask student for course and semester after login."""
    user = st.session_state.user
    st.markdown(f"""
    <div class="hero-section" style="text-align:center;padding:2rem 0;">
        <div class="hero-icon" style="margin-bottom:0.5rem;">
            {icons.wave_hand(56, "#6C63FF")}
        </div>
        <h2 class="hero-title" style="color:#E0E0F0;margin:0;">Welcome, {user["name"]}!</h2>
        <p class="hero-subtitle" style="color:#9E9EC0;margin:0.5rem 0 0 0;">Let's set up your profile</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="profile-setup">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#E0E0F0;text-align:center;margin-bottom:1.5rem;'>Academic Details</h3>", unsafe_allow_html=True)

        course = st.selectbox(
            "Select Your Course",
            ["", "BCA", "BBA", "B.Com", "B.Sc Computer Science", "B.Sc Mathematics",
             "B.Sc Physics", "B.Sc Chemistry", "BA English", "BA History",
             "MCA", "MBA", "M.Com", "M.Sc Computer Science", "Other"],
            key="profile_course"
        )

        semester = st.selectbox(
            "Select Your Semester",
            ["", "1st Semester", "2nd Semester", "3rd Semester", "4th Semester",
             "5th Semester", "6th Semester", "7th Semester", "8th Semester"],
            key="profile_semester"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col_skip, col_continue = st.columns(2)
        with col_skip:
            if st.button("Skip for now", width="stretch"):
                st.session_state.profile_complete = True
                st.rerun()
        with col_continue:
            if st.button("Continue", width="stretch", type="primary"):
                st.session_state.user_course = course
                st.session_state.user_semester = semester.replace(" Semester", "") if semester else ""
                st.session_state.profile_complete = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# Always show sidebar if user is logged in
if st.session_state.user is not None:
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

        # Navigation sections with SVG icons based on role
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
        if st.button("Logout", width="stretch", icon=":material/logout:"):
            # Clear all session state to prevent data leakage
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

# Now show page content
if st.session_state.user is None:
    login_page()
elif not st.session_state.profile_complete and st.session_state.user.get("role") == "student":
    profile_setup_page()
else:
    # Show main app content (without sidebar - it's already rendered above)
    user = st.session_state.user
    course = st.session_state.get("user_course", "")
    semester = st.session_state.get("user_semester", "")

    # Main welcome content with SVG and animations
    st.markdown(f"""
    <div class="hero-section" style="text-align:center;padding:4rem 1rem;">
        <div class="hero-icon" style="margin-bottom:1.25rem;">
            {icons.graduation_cap(64, "#6C63FF")}
        </div>
        <h1 class="hero-title" style="font-size:2.8rem;font-weight:800;background:linear-gradient(135deg,#6C63FF,#4ECDC4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
            margin:0;letter-spacing:-0.5px;">
            Welcome back, {user["name"]}!
        </h1>
        <p class="hero-subtitle" style="color:#9E9EC0;font-size:1.15rem;margin:1rem 0 0 0;">
            Use the sidebar to navigate between features
        </p>
    </div>
    """, unsafe_allow_html=True)

    if user["role"] == "student":
        # Quick actions section with SVG icons
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown(f"""<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;display:flex;align-items:center;gap:10px;'>
            {icons.lightning(22, "#FFB700")} Quick Actions</h4>""", unsafe_allow_html=True)

        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            st.markdown(f"""<div class="quick-action">
                <div class="qa-icon">{icons.chat(36, "#6C63FF")}</div>
                <div class="qa-label">Chat Tutor</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Open Chat", width="stretch", key="qa_chat"):
                st.switch_page("pages/2_Chat_Tutor.py")
        with qa2:
            st.markdown(f"""<div class="quick-action">
                <div class="qa-icon">{icons.quiz(36, "#4ECDC4")}</div>
                <div class="qa-label">Start Quiz</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Open Quiz", width="stretch", key="qa_quiz"):
                st.switch_page("pages/3_Quiz_Mode.py")
        with qa3:
            st.markdown(f"""<div class="quick-action">
                <div class="qa-icon">{icons.exam(36, "#FFB700")}</div>
                <div class="qa-label">Exam Mode</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Open Exam", width="stretch", key="qa_exam"):
                st.switch_page("pages/4_Exam_Simulation.py")
        with qa4:
            st.markdown(f"""<div class="quick-action">
                <div class="qa-icon">{icons.flashcard(36, "#FF5252")}</div>
                <div class="qa-label">Flashcards</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Open Cards", width="stretch", key="qa_flash"):
                st.switch_page("pages/5_Flashcards.py")
        st.markdown('</div>', unsafe_allow_html=True)
    elif user["role"] == "faculty":
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Go to Faculty Panel", width="stretch", icon=":material/school:"):
            st.switch_page("pages/8_Faculty_Panel.py")
    elif user["role"] == "admin":
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Go to Admin Panel", width="stretch", icon=":material/admin_panel_settings:"):
            st.switch_page("pages/7_Admin_Panel.py")
