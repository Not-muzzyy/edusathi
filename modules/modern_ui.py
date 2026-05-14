"""
Modern UI components with latest Streamlit patterns.
Includes: toast notifications, confirmation dialogs, loading states, input validation.
"""
import streamlit as st
import re
from typing import Callable, Any, Optional


def toast_success(message: str, duration: int = 3):
    """Auto-dismissing success toast (uses st.toast in Streamlit 1.32+)."""
    st.toast(f"✅ {message}", icon="✅")


def toast_error(message: str, duration: int = 3):
    """Auto-dismissing error toast."""
    st.toast(f"❌ {message}", icon="❌")


def toast_info(message: str, duration: int = 3):
    """Auto-dismissing info toast."""
    st.toast(f"ℹ️ {message}", icon="ℹ️")


def toast_warning(message: str, duration: int = 3):
    """Auto-dismissing warning toast."""
    st.toast(f"⚠️ {message}", icon="⚠️")


def confirm_dialog(title: str = "Confirm Action", message: str = "Are you sure?", 
                   confirm_text: str = "Yes", cancel_text: str = "Cancel") -> bool:
    """
    Modern confirmation dialog using session state.
    Returns True if user confirms, False if cancels.
    """
    if "confirm_dialog" not in st.session_state:
        st.session_state.confirm_dialog = None
    
    if st.session_state.confirm_dialog is None:
        st.session_state.confirm_dialog = {"shown": False, "result": None}
    
    if not st.session_state.confirm_dialog["shown"]:
        return False
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:14px;padding:2rem;
            border:1px solid rgba(108,99,255,0.25);text-align:center;">
            <h3 style="color:#E0E0F0;margin:0 0 1rem 0;">{title}</h3>
            <p style="color:#9E9EC0;margin:0 0 1.5rem 0;font-size:0.95rem;">{message}</p>
        </div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"✓ {confirm_text}", key="confirm_yes", use_key_prefix=True, width="stretch"):
                st.session_state.confirm_dialog = {"shown": False, "result": True}
                st.rerun()
        with c2:
            if st.button(f"✗ {cancel_text}", key="confirm_no", use_key_prefix=True, width="stretch"):
                st.session_state.confirm_dialog = {"shown": False, "result": False}
                st.rerun()
    
    return st.session_state.confirm_dialog["result"]


def show_confirm_dialog(title: str = "Confirm Action", message: str = "Are you sure?"):
    """Trigger confirmation dialog."""
    st.session_state.confirm_dialog = {"shown": True, "result": None}


def async_button(label: str, callback: Callable, key: str = None, 
                 icon: str = "", width: str = "stretch", disabled: bool = False, **kwargs) -> bool:
    """
    Button with visual disabled state during async operations.
    Shows spinner and prevents double-clicks.
    """
    is_processing = st.session_state.get(f"processing_{key}", False)
    
    if st.button(
        f"{icon} {label}" if icon else label,
        key=key,
        disabled=is_processing or disabled,
        width=width,
        **kwargs
    ):
        st.session_state[f"processing_{key}"] = True
        st.rerun()
    
    if is_processing:
        with st.spinner(f"Processing {label.lower()}..."):
            try:
                callback()
                st.session_state[f"processing_{key}"] = False
                st.rerun()
            except Exception as e:
                st.session_state[f"processing_{key}"] = False
                toast_error(f"Error: {str(e)}")
                st.rerun()
    
    return is_processing


def progressive_loader(steps: list[str], current_step: int):
    """
    Display multi-step progress with visual indicators.
    Args:
        steps: List of step descriptions (e.g., ["Uploading", "Processing", "Indexing"])
        current_step: Current step index (0-based)
    """
    progress_pct = (current_step + 1) / len(steps)
    st.progress(progress_pct)
    
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i < current_step:
                status = "✓"
                color = "#4ECDC4"
            elif i == current_step:
                status = "●"
                color = "#6C63FF"
            else:
                status = "○"
                color = "#4A4A5E"
            
            st.markdown(f"""
            <div style="text-align:center;color:{color};font-weight:600;font-size:0.9rem;">
                <div style="font-size:1.4rem;margin-bottom:0.3rem;">{status}</div>
                {step}
            </div>""", unsafe_allow_html=True)


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email format with feedback.
    Returns: (is_valid, message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email:
        return False, "Email is required"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, "✓ Valid email"


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength with feedback.
    Returns: (is_valid, message)
    """
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Add uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Add lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Add a number"
    return True, "✓ Strong password"


def validate_input(text: str, min_len: int = 1, max_len: int = 100, 
                   pattern: str = None) -> tuple[bool, str]:
    """
    Generic input validation.
    Returns: (is_valid, message)
    """
    if not text or not text.strip():
        return False, "This field is required"
    if len(text) < min_len:
        return False, f"Minimum {min_len} characters required"
    if len(text) > max_len:
        return False, f"Maximum {max_len} characters allowed"
    if pattern and not re.match(pattern, text):
        return False, f"Invalid format"
    return True, "✓ Valid"


def sanitize_input(text: str, max_length: int = 100) -> str:
    """
    Sanitize user input to prevent injection attacks.
    Removes special characters and limits length.
    """
    # Remove newlines and tabs
    text = text.replace('\n', ' ').replace('\t', ' ')
    # Remove leading/trailing whitespace
    text = text.strip()
    # Limit length
    text = text[:max_length]
    # Allow only alphanumeric, spaces, hyphens, commas, periods, parentheses
    text = re.sub(r'[^a-zA-Z0-9\s\-,.()\']', '', text)
    return text


def inline_validation_input(label: str, validator: Callable, key: str = None, **kwargs) -> str:
    """
    Text input with real-time validation feedback.
    Shows validation status inline.
    """
    value = st.text_input(label, key=key, **kwargs)
    
    if value:
        is_valid, message = validator(value)
        color = "#4ECDC4" if is_valid else "#FF5252"
        icon = "✓" if is_valid else "✗"
        st.markdown(f'<p style="color:{color};font-size:0.85rem;margin:-0.5rem 0 0.5rem 0;">{icon} {message}</p>', 
                   unsafe_allow_html=True)
    
    return value


def file_upload_progress(uploaded_file, process_fn: Callable):
    """
    Enhanced file upload with per-file status indicator.
    Returns: (success, result, error_message)
    """
    if not uploaded_file:
        return False, None, None
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.markdown(f"📤 Uploading **{uploaded_file.name}**...")
    progress_bar.progress(25)
    
    try:
        status_text.markdown(f"⚙️ Processing **{uploaded_file.name}**...")
        progress_bar.progress(50)
        
        result = process_fn(uploaded_file)
        
        status_text.markdown(f"✓ **{uploaded_file.name}** processed successfully")
        progress_bar.progress(100)
        
        return True, result, None
    
    except Exception as e:
        status_text.markdown(f"✗ **{uploaded_file.name}** failed: {str(e)}")
        progress_bar.progress(100)
        return False, None, str(e)


def metric_card(label: str, value: str, icon: str = "", color: str = "#6C63FF", width: float = 1):
    """
    Modern metric card with icon and color support.
    """
    st.markdown(f"""
    <div style="background:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:], 16)},0.08);
        border-radius:14px;padding:1.5rem;border:1px solid rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:], 16)},0.2);
        text-align:center;">
        <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
        <div style="color:{color};font-size:2rem;font-weight:700;margin-bottom:0.5rem;">{value}</div>
        <div style="color:#9E9EC0;font-size:0.9rem;font-weight:500;">{label}</div>
    </div>""", unsafe_allow_html=True)


def animated_stat_counter(start: int, end: int, duration: float = 1.0, 
                         label: str = "", icon: str = ""):
    """
    Animated counter for metric cards (visual appeal).
    """
    placeholder = st.empty()
    
    steps = int(duration * 60)  # 60 FPS
    for step in range(steps + 1):
        current = int(start + (end - start) * (step / steps))
        with placeholder.container():
            metric_card(label, str(current), icon)
        
        if step < steps:
            st.sleep(1 / 60)


def loading_skeleton(num_items: int = 3):
    """Skeleton loader for better perceived performance."""
    for i in range(num_items):
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:14px;padding:1.5rem;
            margin-bottom:1rem;height:60px;animation:pulse 1.5s infinite;">
        </div>
        <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
        }}
        </style>""", unsafe_allow_html=True)


def empty_state_modern(icon: str, title: str, message: str, cta_text: str = None, cta_action: Callable = None):
    """Modern empty state with CTA button."""
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 2rem;">
        <div style="font-size:4rem;margin-bottom:1rem;">{icon}</div>
        <h3 style="color:#E0E0F0;margin:0 0 0.5rem 0;font-size:1.4rem;">{title}</h3>
        <p style="color:#9E9EC0;margin:0;font-size:0.95rem;line-height:1.6;max-width:400px;margin:0 auto 0.5rem auto;">
            {message}
        </p>
    </div>""", unsafe_allow_html=True)
    
    if cta_text and cta_action:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(cta_text, width="stretch"):
                cta_action()
