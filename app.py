import streamlit as st
import json
import random

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="General Knowledge Quiz", page_icon="🧠", layout="centered")

# ─── New Vibrant Light-Mode CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%); color: #2d3436; }
    .quiz-header { text-align: center; padding: 2rem 0 1rem 0; }
    .quiz-title {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #2d3436, #0984e3);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .quiz-subtitle { color: #636e72; font-size: 1rem; margin-bottom: 1rem; }
    .mode-badge {
        display: inline-block; padding: 6px 16px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 700; margin-bottom: 1.5rem; color: white;
    }
    .badge-nvidia { background: #00b894; }
    .badge-offline { background: #0984e3; }
    .question-card {
        background: #ffffff; border: 1px solid #dfe6e9;
        border-radius: 16px; padding: 1.8rem; margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .question-number { color: #0984e3; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem; }
    .question-text { color: #2d3436; font-size: 1.3rem; font-weight: 700; }
    .hint-text { color: #636e72; font-size: 0.85rem; margin-top: 0.8rem; font-style: italic; }
    .feedback-correct { background: #dff9fb; border-left: 5px solid #00b894; padding: 1rem; color: #006266; border-radius: 4px; }
    .feedback-wrong { background: #ffeaa7; border-left: 5px solid #d63031; padding: 1rem; color: #634e00; border-radius: 4px; }
    .stButton > button { background: #0984e3 !important; color: white !important; border-radius: 10px; font-weight: 600; }
    .stTextInput > div > div > input { background: #ffffff !important; border: 2px solid #0984e3 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Question Bank ──────────────────────────────────────────────────────────
QUESTION_BANK = {
    "World Geography": [
        {"question": "What is the capital of France?", "answer": "paris", "hint": "Located on the Seine river"},
        {"question": "Which is the largest ocean on Earth?", "answer": "pacific", "hint": "Covers 30% of the Earth's surface"},
        {"question": "What is the longest river in the world?", "answer": "nile", "hint": "Flows through Egypt"}
    ],
    "Technology": [
        {"question": "What does CPU stand for?", "answer": "central processing unit", "hint": "The brain of a computer"},
        {"question": "What does HTML stand for?", "answer": "hypertext markup language", "hint": "The language of web pages"}
    ]
}

# ─── API Functions ──────────────────────────────────────────────────────────
def get_nim_client(api_key):
    from openai import OpenAI
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

def generate_questions_nim(api_key, category, num_q):
    client = get_nim_client(api_key)
    prompt = f"Generate {num_q} quiz questions about {category}. Return JSON: [{'question': '...', 'answer': '...', 'hint': '...'}]"
    completion = client.chat.completions.create(model="meta/llama-3.1-8b-instruct", messages=[{"role": "user", "content": prompt}])
    raw = completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

# ─── App Flow ───────────────────────────────────────────────────────────────
if "phase" not in st.session_state:
    st.session_state.update({"phase": "setup", "score": 0, "current_q": 0, "answers": [], "use_nim": False})

st.markdown(f"""
<div class="quiz-header">
    <div class="quiz-title">🧠 GK Quiz</div>
    <div class="quiz-subtitle">General Knowledge Challenge · DecodeLabs</div>
    <div class="mode-badge {'badge-nvidia' if st.session_state.use_nim else 'badge-offline'}">
        {'⚡ Powered by NVIDIA NIM' if st.session_state.use_nim else '📦 Offline Mode'}
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.phase == "setup":
    api_key = st.text_input("NVIDIA API Key (Optional)", type="password")
    category = st.selectbox("Category", list(QUESTION_BANK.keys()))
    if st.button("🚀 Start Quiz"):
        st.session_state.use_nim = bool(api_key)
        if st.session_state.use_nim:
            st.session_state.questions = generate_questions_nim(api_key, category, 3)
        else:
            st.session_state.questions = QUESTION_BANK[category]
        st.session_state.phase = "quiz"
        st.rerun()

elif st.session_state.phase == "quiz":
    q = st.session_state.questions[st.session_state.current_q]
    st.markdown(f'<div class="question-card"><div class="question-number">Q{st.session_state.current_q+1}</div><div class="question-text">{q["question"]}</div><div class="hint-text">💡 {q["hint"]}</div></div>', unsafe_allow_html=True)
    
    user_ans = st.text_input("Your Answer", key="ans")
    if st.button("Submit"):
        # Sanitization: Strip + Lowercase (DecodeLabs Requirement)
        correct = (user_ans.strip().lower() == q["answer"].strip().lower())
        if correct: st.session_state.score += 1
        st.session_state.answers.append({"user": user_ans, "correct": q["answer"], "status": correct})
        st.session_state.current_q += 1
        if st.session_state.current_q >= len(st.session_state.questions): st.session_state.phase = "results"
        st.rerun()

elif st.session_state.phase == "results":
    st.markdown(f'<div class="question-card"><h2>Final Score: {st.session_state.score}/{len(st.session_state.questions)}</h2></div>', unsafe_allow_html=True)
    if st.button("Restart"):
        st.session_state.update({"phase": "setup", "score": 0, "current_q": 0, "answers": []})
        st.rerun()
