import streamlit as st
import subprocess


st.set_page_config(page_title="Whealthy 🥗", page_icon="🥗", layout="centered")


custom_css = """
<style>
/* Page background and container */
[data-testid="stAppViewContainer"] {
    background-color: #f2f7f3;
    background-image: linear-gradient(180deg, #f4f9f5 0%, #e5f2e7 100%);
    color: #2e5339;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 2rem;
}

/* Center container card */
.main-block {
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(82, 104, 89, 0.08);
    padding: 25px;
    margin-top: 25px;
    backdrop-filter: blur(4px);
}

/* Chat message bubbles */
.chat-message {
    border-radius: 18px;
    padding: 14px 18px;
    margin: 8px 0;
    max-width: 85%;
    line-height: 1.5;
    word-wrap: break-word;
    font-size: 16px;
}

.chat-message.user {
    background-color: #e3f2e1;
    color: #2e5339;
    align-self: flex-end;
    border: 1px solid #b5d1b1;
}

.chat-message.assistant {
    background-color: #ffffff;
    border: 1px solid #c9dcc5;
    color: #2e5339;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* Input field */
.stChatInput input {
    background-color: #f8fcf9 !important;
    border-radius: 12px !important;
    border: 1px solid #c5e1c6 !important;
    color: #2e5339 !important;
    font-size: 16px !important;
}

/* Title and subtitle */
h1 {
    color: #2e5339 !important;
    font-family: 'Poppins', sans-serif !important;
    text-align: center;
}
h3, h2, h4 {
    color: #2e5339 !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Buttons */
.stButton>button {
    background-color: #7ac27d !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 8px 20px !important;
}
.stButton>button:hover {
    background-color: #69aa6a !important;
}

/* Scrollable chat container */
[data-testid="stVerticalBlock"] {
    overflow-y: auto;
    max-height: 75vh;
}

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(
    """
    <div class="main-block">
        <h1>🥗 Whealthy — Your AI Salad Assistant 🌿</h1>
        <p style='text-align:center; color:#496c50; font-size:17px;'>
        Personalized salad and nutrition suggestions made with care 💚
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey there! 🥬 I’m Whealthy, your AI nutrition buddy. What kind of meal are you craving today?"}
    ]


for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='chat-message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)


def query_ollama(prompt):
    """Runs an Ollama model and returns response."""
    command = ["ollama", "run", "llama3.2", prompt]
    try:
        output = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        return output.stdout.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"


if user_input := st.chat_input("Ask me about your meal plan..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='chat-message user'>{user_input}</div>", unsafe_allow_html=True)

    conversation = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    prompt = f"""
    You are Whealthy 🥗, a friendly, health-focused AI assistant.
    Suggest creative, healthy meal or salad ideas.
    Include approximate macros (calories, protein, fat, carbs).
    Use emojis and warm, encouraging tone.
    Chat so far:
    {conversation}
    """

    with st.spinner("Whealthy is mixing your perfect salad... 🥗"):
        response = query_ollama(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"<div class='chat-message assistant'>{response}</div>", unsafe_allow_html=True)
