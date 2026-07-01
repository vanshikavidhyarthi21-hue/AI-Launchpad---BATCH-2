"""
Yojana Sahayak - Streamlit Frontend
AI-powered government scheme discovery chatbot for Indian citizens.
"""

import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from src.chatbot import YojanaChatbot, PROFILE_FIELDS
from src.rag_pipeline import YojanaRetriever
from dotenv import load_dotenv

load_dotenv()

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Yojana Sahayak - Government Schemes AI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* App background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Chat container */
.chat-container {
    max-width: 850px;
    margin: 0 auto;
}

/* User message bubble */
.user-bubble {
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: bold !important;
    border: 1px solid rgba(0, 0, 0, 0.15) !important;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0 8px 80px;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    animation: fadeInRight 0.3s ease;
}

/* Assistant message bubble */
.assistant-bubble {
    background: #eef2f6 !important;
    border: 1px solid #d1d5db !important;
    color: #000000 !important;
    font-weight: bold !important;
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    margin: 8px 80px 8px 0;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    animation: fadeInLeft 0.3s ease;
    line-height: 1.6;
}

.assistant-bubble a {
    color: #1d4ed8 !important; /* Premium dark blue link */
    font-weight: bold !important;
    text-decoration: underline;
}

/* Avatar */
.avatar-bot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-right: 8px;
    box-shadow: 0 2px 10px rgba(240, 147, 251, 0.4);
}

/* Profile progress */
.profile-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.profile-field {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.85);
    font-size: 0.87rem;
}

.profile-field:last-child {
    border-bottom: none;
}

.field-check {
    color: #4ade80;
    font-size: 16px;
}

.field-pending {
    color: rgba(255,255,255,0.3);
    font-size: 16px;
}

/* Scheme card */
.scheme-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
    transition: all 0.2s ease;
    cursor: pointer;
    backdrop-filter: blur(8px);
}

.scheme-card:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.scheme-name {
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 4px;
}

.scheme-state {
    color: #a78bfa;
    font-size: 0.78rem;
    font-weight: 500;
}

.scheme-type {
    background: rgba(102, 126, 234, 0.25);
    color: #c4b5fd;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 500;
    display: inline-block;
    margin-top: 6px;
}

/* Matching count badge */
.matching-badge {
    background: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
    color: #0f172a;
    font-weight: 700;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    display: inline-block;
    margin-left: 8px;
}

/* Input area styling */
div[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: bold !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 16px !important;
    font-size: 0.95rem !important;
}

div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: bold !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
}

/* Fallback override for any dynamic input/textarea elements */
input, textarea {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: bold !important;
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.9) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}

.sub-title {
    text-align: center;
    color: rgba(255,255,255,0.6);
    font-size: 0.95rem;
    margin-bottom: 20px;
}

/* Progress bar */
.progress-bar-outer {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 6px;
    margin: 10px 0;
}

.progress-bar-inner {
    background: linear-gradient(90deg, #667eea, #f5576c);
    border-radius: 10px;
    height: 6px;
    transition: width 0.5s ease;
}

/* Status cards */
.status-card {
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #4ade80;
    font-size: 0.85rem;
    font-weight: 500;
}

.warning-card {
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #fbbf24;
    font-size: 0.85rem;
}

/* Animations */
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 3px;
}

/* Button styling */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
}

/* Markdown in chat */
.assistant-bubble strong {
    color: #f0abfc;
}

.assistant-bubble ul, .assistant-bubble ol {
    padding-left: 20px;
    margin: 8px 0;
}

.assistant-bubble li {
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ───────────────────────────────────────────────
def init_session():
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = YojanaChatbot()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "profile_complete" not in st.session_state:
        st.session_state.profile_complete = False
    if "matching_count" not in st.session_state:
        st.session_state.matching_count = 0
    if "filled_fields" not in st.session_state:
        st.session_state.filled_fields = 0
    if "awaiting_profile_field" not in st.session_state:
        st.session_state.awaiting_profile_field = "state"
    if "db_ready" not in st.session_state:
        try:
            retriever = YojanaRetriever()
            st.session_state.db_ready = retriever.is_ready()
        except Exception:
            st.session_state.db_ready = False
    if "started" not in st.session_state:
        st.session_state.started = False


def reset_conversation():
    """Reset everything to start fresh."""
    st.session_state.chatbot.reset()
    st.session_state.messages = []
    st.session_state.profile_complete = False
    st.session_state.matching_count = 0
    st.session_state.filled_fields = 0
    st.session_state.awaiting_profile_field = "state"
    st.session_state.started = False


# ── Sidebar ────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-size: 3rem;">🇮🇳</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: white;">Yojana Sahayak</div>
            <div style="font-size: 0.78rem; color: rgba(255,255,255,0.5);">योजना सहायक</div>
        </div>
        """, unsafe_allow_html=True)

        # DB Status
        if st.session_state.db_ready:
            st.markdown('<div class="status-card">✅ Vector DB: 269 schemes ready</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-card">
            ⚠️ <strong>Vector DB Not Ready</strong><br>
            Run the setup scripts first:<br>
            <code>python scripts/01_scrape_and_extract.py</code><br>
            <code>python scripts/02_build_vectordb.py</code>
            </div>
            """, unsafe_allow_html=True)

        # API Key Status
        _api = os.getenv("ANTHROPIC_API_KEY", "")
        if _api and _api != "your_anthropic_api_key_here":
            if _api.startswith("AQ.") or _api.startswith("AIzaSy"):
                st.markdown('<div class="status-card">✅ Gemini API: Connected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-card">✅ Anthropic API: Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-card">⚠️ <strong>API Key Missing</strong><br>Enter key in the main area below</div>', unsafe_allow_html=True)

        st.divider()

        # Profile Progress
        profile = st.session_state.chatbot.user_profile
        filled = sum(1 for v in profile.values() if v)
        total = len(PROFILE_FIELDS)
        pct = int((filled / total) * 100)

        st.markdown("**📋 Your Profile**")
        st.markdown(f"""
        <div class="progress-bar-outer">
            <div class="progress-bar-inner" style="width: {pct}%;"></div>
        </div>
        <div style="color: rgba(255,255,255,0.5); font-size: 0.78rem; margin-bottom: 12px;">
            {filled}/{total} fields completed
        </div>
        """, unsafe_allow_html=True)

        field_labels = {
            "state": "📍 State",
            "age": "🎂 Age",
            "gender": "👤 Gender",
            "occupation": "💼 Occupation",
            "income": "💰 Income",
            "category": "🏷️ Category",
            "interest": "🎯 Interest",
        }

        for field in PROFILE_FIELDS:
            value = profile.get(field)
            if value:
                st.markdown(f"""
                <div class="profile-field">
                    <span class="field-check">✓</span>
                    <span style="color: rgba(255,255,255,0.5); flex: 0 0 90px;">{field_labels[field]}</span>
                    <span style="color: #c4b5fd; font-weight: 500;">{value}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="profile-field">
                    <span class="field-pending">○</span>
                    <span style="color: rgba(255,255,255,0.3);">{field_labels[field]}</span>
                </div>
                """, unsafe_allow_html=True)

        if st.session_state.matching_count > 0:
            st.divider()
            st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Matching Schemes Found</div>
                <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #4ade80, #22d3ee);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {st.session_state.matching_count}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        if st.button("🔄 Start New Conversation", use_container_width=True):
            reset_conversation()
            st.rerun()

        st.markdown("""
        <div style="margin-top: 20px; color: rgba(255,255,255,0.3); font-size: 0.72rem; text-align: center;">
            Powered by Claude Sonnet & ChromaDB<br>
            Data: myscheme.gov.in
        </div>
        """, unsafe_allow_html=True)


# ── Main Chat Area ─────────────────────────────────────────────────────────────
def render_chat():
    # Header
    st.markdown("""
    <div class="main-title">🇮🇳 Yojana Sahayak</div>
    <div class="sub-title">Discover Government Schemes You're Eligible For · AI-Powered · Free</div>
    """, unsafe_allow_html=True)

    # Check if DB is ready
    if not st.session_state.db_ready:
        st.error("""
        ### ⚠️ Vector Database Not Found

        Run these commands first:
        ```bash
        python scripts/fetch_all_slugs.py
        python scripts/01_scrape_and_extract.py
        python scripts/02_build_vectordb.py
        ```
        """)
        return

    # Check if API key is set — show inline setup if missing
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key or api_key == "your_anthropic_api_key_here":
        st.markdown("""
        <div style="background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.4);
             border-radius: 16px; padding: 20px 24px; margin-bottom: 20px;">
            <div style="color: #fbbf24; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">⚠️ API Key Required</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.88rem;">
                Add your Anthropic (Claude) or Google Gemini API key to the <code>.env</code> file, or enter it below:
            </div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            entered_key = st.text_input(
                "API Key",
                placeholder="sk-ant-api03-... OR AQ.Ab8RN6J...",
                type="password",
                label_visibility="collapsed",
            )
        with col2:
            if st.button("Apply Key", use_container_width=True):
                if entered_key.strip():
                    os.environ["ANTHROPIC_API_KEY"] = entered_key.strip()
                    # Re-init chatbot with new key
                    from src.chatbot import YojanaChatbot
                    st.session_state.chatbot = YojanaChatbot()
                    st.session_state.started = False
                    st.success("Key applied! Refreshing...")
                    st.rerun()
                else:
                    st.error("Please enter a key")
        st.caption("Get an Anthropic key at [console.anthropic.com](https://console.anthropic.com) or Gemini key at [aistudio.google.com](https://aistudio.google.com)")
        st.divider()

    # Initialize welcome message
    if not st.session_state.started:
        welcome = st.session_state.chatbot.get_welcome_message()
        st.session_state.messages = [{"role": "assistant", "content": welcome}]
        st.session_state.started = True

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin: 8px 0;">
                    <div class="user-bubble">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Use columns to place avatar + message side by side
                col_av, col_msg = st.columns([0.06, 0.94])
                with col_av:
                    st.markdown('<div class="avatar-bot">🤖</div>', unsafe_allow_html=True)
                with col_msg:
                    st.markdown(
                        f'<div class="assistant-bubble">{msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )

    # Chat input
    if prompt := st.chat_input(
        placeholder="Type your answer here... (e.g., 'Maharashtra', 'Farmer', '28 years old')",
        key="chat_input"
    ):
        # Add user message to display
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Determine if this is a profile answer
        next_q = st.session_state.chatbot.get_next_question()
        is_profile = next_q is not None

        # Get chatbot response
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.chatbot.chat(
                    prompt,
                    is_profile_answer=is_profile
                )

                # Update session state
                st.session_state.matching_count = result["matching_count"]
                st.session_state.filled_fields = result["filled_fields"]
                st.session_state.profile_complete = result["profile_complete"]

                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["message"]
                })

            except Exception as e:
                error_msg = f"I encountered an issue. Please try again. (Error: {str(e)[:100]})"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

        st.rerun()


# ── Main App ───────────────────────────────────────────────────────────────────
def main():
    init_session()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
