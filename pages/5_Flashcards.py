"""pages/5_Flashcards.py — Premium flashcard interface."""
import streamlit as st

st.set_page_config(page_title="Flashcards — EduSathi", page_icon="🃏", layout="wide")

from modules.ui_components import inject_css, page_header, empty_state, render_sidebar
from modules.flashcard_generator import create_flashcards_from_store
from modules.auth import get_user_documents, save_flashcards, get_user_flashcards

inject_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

user = st.session_state.user
if user["role"] != "student":
    st.error("Access denied. Student role required.")
    st.stop()

if "flipped_cards" not in st.session_state:
    st.session_state.flipped_cards = set()

user = st.session_state.user
page_header("▣ Flashcards", "Auto-generated flashcards for rapid revision")

tab1, tab2 = st.tabs(["✨ Generate New", "📚 My Flashcards"])

with tab1:
    docs = get_user_documents(user["id"])
    if not docs:
        empty_state(
            "📄",
            "No Study Materials Yet",
            "Upload PDFs in Chat Tutor first to generate flashcards from your content."
        )
    else:
        col_cfg, col_prev = st.columns([1, 2])
        with col_cfg:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;'>⚙️ Settings</h4>", unsafe_allow_html=True)
            doc_map = {d["filename"]: d for d in docs}
            sel_doc = st.selectbox("📄 Select Document", list(doc_map.keys()))
            topic_hint = st.text_input("🎯 Topic Hint", placeholder="e.g. Sorting Algorithms")
            n_cards = st.slider("📝 Number of Cards", 5, 30, 10)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ Generate Flashcards", width="stretch"):
                doc = doc_map[sel_doc]
                with st.spinner("🧠 Generating flashcards..."):
                    try:
                        cards = create_flashcards_from_store(
                            doc["vector_store_path"], topic=topic_hint, n=n_cards
                        )
                    except Exception as e:
                        cards = []
                        st.error(f"❌ Error generating flashcards: {e}")
                if cards:
                    try:
                        save_flashcards(user["id"], doc["id"], cards)
                        st.success(f"✅ Created {len(cards)} flashcards!")
                        st.session_state.flipped_cards = set()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error saving flashcards: {e}")
                elif not cards:
                    st.error("❌ Could not generate flashcards. Check your API key or try a different topic.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_prev:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#E0E0F0;margin:0 0 1.25rem 0;font-weight:600;'>💡 How to Use</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div style="color:#9E9EC0;line-height:2.1;font-size:0.94rem;">
                <div style="margin-bottom:1rem;display:flex;align-items:flex-start;gap:12px;">
                    <span style="color:#6C63FF;font-weight:700;font-size:1.15rem;">◎</span>
                    <span>Click any card to flip and reveal the answer</span>
                </div>
                <div style="margin-bottom:1rem;display:flex;align-items:flex-start;gap:12px;">
                    <span style="color:#4ECDC4;font-weight:700;font-size:1.15rem;">◎</span>
                    <span>Front shows the term, concept, or question</span>
                </div>
                <div style="margin-bottom:1rem;display:flex;align-items:flex-start;gap:12px;">
                    <span style="color:#FFB700;font-weight:700;font-size:1.15rem;">◎</span>
                    <span>Back shows the definition or explanation</span>
                </div>
                <div style="display:flex;align-items:flex-start;gap:12px;">
                    <span style="color:#9E9EC0;font-weight:700;font-size:1.15rem;">◎</span>
                    <span>Cards are saved automatically to your account</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    all_cards = get_user_flashcards(user["id"])
    if not all_cards:
        empty_state(
            "🃏",
            "No Flashcards Yet",
            "Generate some from the Generate tab to start your revision!"
        )
    else:
        col_info, col_reset = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <p style='color:#9E9EC0;margin:0;font-size:1rem;'>
                You have <strong style='color:#6C63FF;font-size:1.2rem;'>{len(all_cards)}</strong> flashcards
            </p>""", unsafe_allow_html=True)
        with col_reset:
            if st.button("🔄 Reset All Flips", width="stretch"):
                st.session_state.flipped_cards = set()
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        cols_per_row = 3
        rows = [all_cards[i:i+cols_per_row] for i in range(0, len(all_cards), cols_per_row)]
        for row in rows:
            cols = st.columns(cols_per_row)
            for ci, (card, col) in enumerate(zip(row, cols)):
                card_id = card["id"]
                is_flipped = card_id in st.session_state.flipped_cards
                with col:
                    flipped_class = "flipped" if is_flipped else ""
                    st.markdown(f"""
                    <div class="flashcard-container" id="fc_{card_id}">
                        <div class="flashcard {flipped_class}">
                            <div class="flashcard-front">
                                <div>
                                    <div style="font-size:0.72rem;color:#6C63FF;margin-bottom:0.85rem;
                                        text-transform:uppercase;letter-spacing:1.8px;font-weight:600;">
                                        📖 TERM
                                    </div>
                                    <div style="font-size:1.08rem;line-height:1.55;">
                                        {card["front"]}
                                    </div>
                                </div>
                            </div>
                            <div class="flashcard-back">
                                <div>
                                    <div style="font-size:0.72rem;color:#4ECDC4;margin-bottom:0.85rem;
                                        text-transform:uppercase;letter-spacing:1.8px;font-weight:600;">
                                        💡 DEFINITION
                                    </div>
                                    <div style="font-size:0.98rem;line-height:1.55;">
                                        {card["back"]}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    flip_label = "👁️ Show Answer" if not is_flipped else "🔙 Show Term"
                    if st.button(flip_label, key=f"flip_{card_id}", width="stretch"):
                        if card_id in st.session_state.flipped_cards:
                            st.session_state.flipped_cards.discard(card_id)
                        else:
                            st.session_state.flipped_cards.add(card_id)
                        st.rerun()

                    source = card.get("filename", "")
                    if source:
                        st.markdown(f"""
                        <div style='font-size:0.74rem;color:#6E6E82;text-align:center;margin-top:5px;'>
                            📄 {source[:20]}{"..." if len(source) > 20 else ""}
                        </div>""", unsafe_allow_html=True)
