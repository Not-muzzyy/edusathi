"""pages/2_Chat_Tutor.py — AI-powered chat with premium UI."""
import streamlit as st

st.set_page_config(page_title="Chat Tutor — EduSathi", page_icon="💬", layout="wide")

from modules.ui_components import inject_css, page_header, chat_message, empty_state, render_sidebar
from modules.rag_pipeline import ingest_pdf, retrieve_context_from_multiple
from modules.llm_client import chat
from modules.auth import save_document_record, get_user_documents
from modules.modern_ui import toast_success, toast_error, toast_warning, validate_input, progressive_loader

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user = st.session_state.user
page_header("◉ Chat Tutor", "Ask anything from your uploaded study material")

col_main, col_side = st.columns([3, 1])

with col_side:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;'>📤 Upload Material</h4>", unsafe_allow_html=True)
    subject = st.text_input("Subject Tag", placeholder="e.g. Data Structures", label_visibility="collapsed")
    st.markdown("<p style='color:#9E9EC0;font-size:0.82rem;margin:-0.5rem 0 0.75rem 0;'>Subject tag for organization</p>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload PDFs (max 50MB each)",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can select multiple PDF files at once"
    )

    if uploaded_files:
        valid_files = [f for f in uploaded_files if f.size <= 50 * 1024 * 1024]
        oversized = [f for f in uploaded_files if f.size > 50 * 1024 * 1024]

        if oversized:
            st.warning(f"⚠️ {len(oversized)} file(s) exceed 50MB limit")

        if valid_files and st.button("🚀 Process PDFs", width="stretch"):
            progress = st.progress(0)
            success_count = 0
            total_chunks = 0

            for idx, uploaded in enumerate(valid_files):
                with st.spinner(f"Processing {uploaded.name}..."):
                    try:
                        result = ingest_pdf(
                            uploaded.read(),
                            uploaded.name,
                            user["id"],
                            subject or "general"
                        )
                        if result["success"]:
                            save_document_record(
                                user["id"],
                                uploaded.name,
                                subject or "general",
                                result["store_path"]
                            )
                            success_count += 1
                            total_chunks += result["chunk_count"]
                        else:
                            st.error(f"❌ {uploaded.name}: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ {uploaded.name}: {str(e)}")

                progress.progress((idx + 1) / len(valid_files))

            if success_count > 0:
                st.success(f"✅ Processed {success_count} PDF(s) with {total_chunks} total chunks!")
                st.rerun()

    st.markdown("<hr style='border-color:rgba(108,99,255,0.18);margin:1.25rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#E0E0F0;margin:0 0 0.85rem 0;font-weight:600;'>📚 Your Documents</h4>", unsafe_allow_html=True)

    docs = get_user_documents(user["id"])
    if docs:
        for d in docs:
            st.markdown(f"""
            <div style="padding:0.7rem 0.9rem;background:rgba(108,99,255,0.08);
                border-radius:12px;margin:6px 0;border-left:3px solid rgba(108,99,255,0.55);">
                <div style="font-size:0.88rem;color:#E0E0F0;font-weight:500;
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    📄 {d['filename'][:26]}{"..." if len(d['filename']) > 26 else ""}
                </div>
                <div style="font-size:0.74rem;color:#9E9EC0;margin-top:3px;">{d['subject_tag']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#9E9EC0;font-size:0.88rem;text-align:center;padding:1rem 0;'>No documents yet. Upload PDFs above.</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", width="stretch"):
        if st.session_state.get("confirm_clear_chat", False):
            st.session_state.chat_history = []
            st.session_state.confirm_clear_chat = False
            toast_success("Chat history cleared!")
            st.rerun()
        else:
            st.session_state.confirm_clear_chat = True
            st.warning("⚠️ This will delete all messages. Click again to confirm.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # Chat messages container
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            empty_state(
                "💬",
                "Start a Conversation",
                "Upload your study material and ask any questions. I'll help you understand concepts from your notes."
            )
        else:
            for msg in st.session_state.chat_history:
                chat_message(msg["content"], is_user=(msg["role"] == "user"), name=user["name"])

    # Chat input form
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        q = st.text_area(
            "Ask a question...",
            height=100,
            placeholder="💡 What is a binary search tree? How does quicksort work?",
            label_visibility="collapsed"
        )
        col_btn1, col_btn2 = st.columns([4, 1])
        with col_btn2:
            submitted = st.form_submit_button("Send 📨", width="stretch")

    if submitted and q.strip():
        docs = get_user_documents(user["id"])
        store_paths = [d["vector_store_path"] for d in docs if d.get("vector_store_path")]

        if not store_paths:
            st.warning("⚠️ Upload a PDF first to enable context-aware answers.")
        else:
            with st.spinner("🤔 Thinking..."):
                try:
                    context = retrieve_context_from_multiple(q, store_paths)
                    if not context:
                        answer = "I don't have information on that in your uploaded material. Try uploading more relevant PDFs."
                    else:
                        answer = chat(context, q, st.session_state.chat_history)
                except Exception as e:
                    answer = f"Sorry, I encountered an error: {str(e)}. Please try again."

            st.session_state.chat_history.append({"role": "user", "content": q})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
