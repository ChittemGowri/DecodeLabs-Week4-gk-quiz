import streamlit as st
import json
import random

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="General Knowledge Quiz",
    page_icon="🧠",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
    .quiz-header { text-align: center; padding: 2rem 0 1rem 0; }
    .quiz-title {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(90deg, #76b900, #00d4ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .quiz-subtitle { color: #a0a0b0; font-size: 1rem; margin-bottom: 1rem; }
    .mode-badge {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 1.5rem;
    }
    .badge-nvidia { background: linear-gradient(90deg, #76b900, #5a8f00); color: white; }
    .badge-offline { background: linear-gradient(90deg, #0055a4, #003d7a); color: white; }
    .question-card {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(118,185,0,0.3);
        border-radius: 14px; padding: 1.5rem 1.8rem; margin: 1rem 0;
    }
    .question-number { color: #76b900; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }
    .question-text { color: #e8e8f0; font-size: 1.2rem; font-weight: 600; line-height: 1.5; }
    .hint-text { color: #7a7a9a; font-size: 0.85rem; margin-top: 0.5rem; font-style: italic; }
    .score-card {
        text-align: center; background: rgba(118,185,0,0.1);
        border: 2px solid #76b900; border-radius: 16px; padding: 2rem; margin: 1.5rem 0;
    }
    .score-number { font-size: 4rem; font-weight: 900; color: #76b900; line-height: 1; }
    .score-label { color: #a0a0b0; font-size: 1rem; margin-top: 0.3rem; }
    .feedback-correct {
        background: rgba(40,167,69,0.15); border-left: 4px solid #28a745;
        border-radius: 8px; padding: 0.8rem 1rem; color: #6fcf97; margin: 0.5rem 0;
    }
    .feedback-wrong {
        background: rgba(220,53,69,0.15); border-left: 4px solid #dc3545;
        border-radius: 8px; padding: 0.8rem 1rem; color: #ff8080; margin: 0.5rem 0;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(118,185,0,0.4) !important;
        color: #e8e8f0 !important; border-radius: 8px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #76b900, #5a8f00); color: white;
        border: none; border-radius: 8px; font-weight: 600;
        padding: 0.6rem 1.5rem; width: 100%;
    }
    .progress-bar-container { background: rgba(255,255,255,0.08); border-radius: 100px; height: 8px; margin: 0.5rem 0 1.5rem 0; }
    .progress-bar-fill { background: linear-gradient(90deg, #76b900, #00d4ff); border-radius: 100px; height: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Hardcoded Question Bank (offline fallback) ──────────────────────────────
QUESTION_BANK = {
    "World Geography": [
        {"question": "What is the capital of France?", "answer": "paris", "hint": "Located on the Seine river"},
        {"question": "Which is the largest ocean on Earth?", "answer": "pacific", "hint": "It covers more than 30% of the Earth's surface"},
        {"question": "What is the longest river in the world?", "answer": "nile", "hint": "Flows through Egypt into the Mediterranean"},
        {"question": "Which country has the most natural lakes?", "answer": "canada", "hint": "The country with the maple leaf flag"},
        {"question": "What is the smallest country in the world?", "answer": "vatican city", "hint": "Located within Rome, Italy"},
        {"question": "Which continent is the Sahara Desert located on?", "answer": "africa", "hint": "The second largest continent"},
        {"question": "What is the capital of Japan?", "answer": "tokyo", "hint": "One of the most populous cities on Earth"},
    ],
    "World History": [
        {"question": "In which year did World War II end?", "answer": "1945", "hint": "Atomic bombs were dropped that year"},
        {"question": "Who was the first President of the United States?", "answer": "george washington", "hint": "His face is on the one-dollar bill"},
        {"question": "Which ancient wonder was located in Alexandria?", "answer": "lighthouse", "hint": "It guided ships into the harbor"},
        {"question": "In which year did the Berlin Wall fall?", "answer": "1989", "hint": "It marked the end of the Cold War era"},
        {"question": "Who invented the telephone?", "answer": "alexander graham bell", "hint": "He made the first call in 1876"},
        {"question": "Which empire was ruled by Julius Caesar?", "answer": "roman", "hint": "It was centered in Rome, Italy"},
        {"question": "In which year did India gain independence?", "answer": "1947", "hint": "The same year Pakistan was also created"},
    ],
    "Science & Nature": [
        {"question": "What is the chemical symbol for water?", "answer": "h2o", "hint": "Two hydrogen, one oxygen"},
        {"question": "How many bones are in the adult human body?", "answer": "206", "hint": "Babies actually have more"},
        {"question": "What planet is known as the Red Planet?", "answer": "mars", "hint": "The fourth planet from the Sun"},
        {"question": "What gas do plants absorb during photosynthesis?", "answer": "carbon dioxide", "hint": "It's what we exhale"},
        {"question": "What is the speed of light in km/s (approximately)?", "answer": "300000", "hint": "It's approximately 3 × 10⁵"},
        {"question": "What is the hardest natural substance on Earth?", "answer": "diamond", "hint": "Used in engagement rings"},
        {"question": "Which organ pumps blood through the human body?", "answer": "heart", "hint": "It beats about 100,000 times per day"},
    ],
    "Technology": [
        {"question": "What does CPU stand for?", "answer": "central processing unit", "hint": "The brain of a computer"},
        {"question": "Who co-founded Apple with Steve Jobs?", "answer": "steve wozniak", "hint": "Known as 'Woz'"},
        {"question": "What does HTML stand for?", "answer": "hypertext markup language", "hint": "The language of web pages"},
        {"question": "In what year was the World Wide Web invented?", "answer": "1989", "hint": "Tim Berners-Lee created it"},
        {"question": "What does RAM stand for?", "answer": "random access memory", "hint": "Temporary storage while a computer runs"},
        {"question": "Which company developed the Python programming language?", "answer": "python software foundation", "hint": "Guido van Rossum created it in 1991"},
        {"question": "What does URL stand for?", "answer": "uniform resource locator", "hint": "The address of a web page"},
    ],
    "Sports": [
        {"question": "How many players are on a standard football (soccer) team?", "answer": "11", "hint": "Each side has the same number"},
        {"question": "In which country did the Olympic Games originate?", "answer": "greece", "hint": "Ancient civilization, Mediterranean country"},
        {"question": "How many Grand Slam tournaments are there in tennis?", "answer": "4", "hint": "Australian Open, French Open, Wimbledon, and one more"},
        {"question": "What sport is played at Wimbledon?", "answer": "tennis", "hint": "Played on grass courts"},
        {"question": "How many rings are on the Olympic flag?", "answer": "5", "hint": "Each represents a continent"},
        {"question": "In cricket, how many players are on each team?", "answer": "11", "hint": "Same as football/soccer"},
        {"question": "What is the national sport of India?", "answer": "hockey", "hint": "Played with a stick and ball on a field"},
    ],
    "Arts & Literature": [
        {"question": "Who wrote the play Romeo and Juliet?", "answer": "william shakespeare", "hint": "The Bard of Avon"},
        {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci", "hint": "Also known for The Last Supper"},
        {"question": "In which city is the Louvre museum located?", "answer": "paris", "hint": "The capital of France"},
        {"question": "Who wrote the Harry Potter series?", "answer": "j.k. rowling", "hint": "She wrote it as a single mother in cafés"},
        {"question": "What is the name of the hobbit in Tolkien's 'The Hobbit'?", "answer": "bilbo baggins", "hint": "His nephew Frodo is in Lord of the Rings"},
        {"question": "Who sculpted the statue of David?", "answer": "michelangelo", "hint": "He also painted the Sistine Chapel ceiling"},
        {"question": "In which country was the novel '1984' author George Orwell born?", "answer": "india", "hint": "He was born in Motihari in 1903"},
    ],
}

CATEGORIES = list(QUESTION_BANK.keys())

# ─── NVIDIA NIM (optional) ──────────────────────────────────────────────────
def get_nim_client(api_key: str):
    from openai import OpenAI
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

def generate_questions_nim(api_key: str, category: str, num_q: int) -> list[dict]:
    client = get_nim_client(api_key)
    system = "You are a quiz master. Return ONLY a valid JSON array, no markdown, no extra text."
    prompt = f"""Generate exactly {num_q} general knowledge quiz questions about {category}.
Return a JSON array:
[{{"question": "...", "answer": "lowercase answer", "hint": "helpful hint"}}]
Rules: answers must be lowercase, short phrases. Questions must be unambiguous."""
    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0.5, max_tokens=600,
    )
    raw = completion.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    questions = json.loads(raw)
    for q in questions:
        q["answer"] = q["answer"].strip().lower()
    return questions

def nim_evaluate(api_key: str, question: str, correct: str, user: str) -> dict:
    client = get_nim_client(api_key)
    prompt = f"""Question: {question}
Correct answer: {correct}
User's answer: {user}
Is the user correct? Consider synonyms and alternate phrasings.
Return JSON only: {{"is_correct": true/false, "explanation": "brief explanation"}}"""
    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2, max_tokens=150,
    )
    raw = completion.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)

# ─── Core Logic ─────────────────────────────────────────────────────────────
def get_questions_offline(category: str, num_q: int) -> list[dict]:
    pool = QUESTION_BANK.get(category, QUESTION_BANK["World Geography"])
    return random.sample(pool, min(num_q, len(pool)))

def check_answer(user: str, correct: str) -> bool:
    # Input sanitization: strip whitespace + lowercase (DecodeLabs requirement)
    return user.strip().lower() == correct.strip().lower()

# ─── Session State ───────────────────────────────────────────────────────────
for k, v in {
    "api_key": "", "phase": "setup", "questions": [],
    "current_q": 0, "score": 0, "answers": [],
    "category": CATEGORIES[0], "num_q": 3,
    "use_nim": False, "submitted": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Header ─────────────────────────────────────────────────────────────────
mode_label = "⚡ Powered by NVIDIA NIM" if st.session_state.use_nim else "📦 Offline Mode"
mode_class = "badge-nvidia" if st.session_state.use_nim else "badge-offline"
st.markdown(f"""
<div class="quiz-header">
    <div class="quiz-title">🧠 GK Quiz</div>
    <div class="quiz-subtitle">General Knowledge Challenge · DecodeLabs Project 4</div>
    <div class="mode-badge {mode_class}">{mode_label}</div>
</div>
""", unsafe_allow_html=True)

# ─── Phase: Setup ────────────────────────────────────────────────────────────
if st.session_state.phase == "setup":
    st.markdown("### ⚙️ Settings")

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", CATEGORIES)
    with col2:
        num_q = st.selectbox("Questions", [3, 5, 7], index=0)

    st.divider()
    st.markdown("#### 🔑 NVIDIA NIM API Key *(optional)*")
    st.caption("Leave blank to play with built-in questions — no key required.")
    api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="nvapi-xxxx  (optional)",
        label_visibility="collapsed",
    )
    st.session_state.api_key = api_key

    if api_key:
        st.info("✅ API key detected — questions will be AI-generated by NVIDIA NIM.")
    else:
        st.info("📦 No API key — using built-in question bank. Works 100% offline.")

    if st.button("🚀 Start Quiz", use_container_width=True):
        use_nim = bool(api_key.strip())
        questions = []
        error = None

        if use_nim:
            with st.spinner("Generating questions with NVIDIA NIM..."):
                try:
                    questions = generate_questions_nim(api_key.strip(), category, num_q)
                except Exception as e:
                    error = str(e)
                    st.warning(f"NIM failed ({e}). Falling back to offline mode.")
                    questions = get_questions_offline(category, num_q)
                    use_nim = False
        else:
            questions = get_questions_offline(category, num_q)

        st.session_state.questions = questions
        st.session_state.category = category
        st.session_state.num_q = num_q
        st.session_state.use_nim = use_nim
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.submitted = False
        st.session_state.phase = "quiz"
        st.rerun()

# ─── Phase: Quiz ─────────────────────────────────────────────────────────────
elif st.session_state.phase == "quiz":
    questions = st.session_state.questions
    idx = st.session_state.current_q
    total = len(questions)
    q = questions[idx]

    # Progress
    pct = int((idx / total) * 100)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;color:#a0a0b0;font-size:0.85rem;margin-bottom:4px;">
        <span>Question {idx+1} of {total}</span>
        <span>Score: {st.session_state.score}/{idx}</span>
    </div>
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Q{idx+1} · {st.session_state.category}</div>
        <div class="question-text">{q['question']}</div>
        <div class="hint-text">💡 {q.get('hint','')}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.submitted:
        with st.form(key=f"form_{idx}"):
            user_answer = st.text_input("Answer", placeholder="Type your answer...", label_visibility="collapsed")
            if st.form_submit_button("Submit ✓", use_container_width=True):
                if not user_answer.strip():
                    st.warning("Type an answer first.")
                else:
                    # Local check first (strip + lower)
                    is_correct = check_answer(user_answer, q["answer"])
                    explanation = f"Correct answer: **{q['answer']}**"

                    # Semantic NIM check only if key exists and local check failed
                    if st.session_state.use_nim and not is_correct:
                        try:
                            result = nim_evaluate(
                                st.session_state.api_key,
                                q["question"], q["answer"], user_answer.strip().lower()
                            )
                            is_correct = result.get("is_correct", False)
                            explanation = result.get("explanation", explanation)
                        except Exception:
                            pass  # keep local result

                    if is_correct:
                        st.session_state.score += 1

                    st.session_state.answers.append({
                        "user": user_answer,
                        "correct": q["answer"],
                        "is_correct": is_correct,
                        "explanation": explanation,
                    })
                    st.session_state.submitted = True
                    st.rerun()
    else:
        a = st.session_state.answers[-1]
        if a["is_correct"]:
            st.markdown(f'<div class="feedback-correct">✅ <strong>Correct!</strong> {a["explanation"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-wrong">❌ <strong>Wrong.</strong> You said "<em>{a["user"]}</em>". {a["explanation"]}</div>', unsafe_allow_html=True)

        if idx + 1 < total:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_q += 1
                st.session_state.submitted = False
                st.rerun()
        else:
            if st.button("See Results 🎯", use_container_width=True):
                st.session_state.phase = "results"
                st.rerun()

# ─── Phase: Results ──────────────────────────────────────────────────────────
elif st.session_state.phase == "results":
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct = int((score / total) * 100)

    emoji = "🏆" if pct == 100 else "🎉" if pct >= 66 else "📚" if pct >= 33 else "💪"
    grade = "Perfect!" if pct == 100 else "Well Done!" if pct >= 66 else "Keep Practicing" if pct >= 33 else "Keep Learning!"

    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:3rem">{emoji}</div>
        <div class="score-number">{score}<span style="font-size:2rem;color:#a0a0b0">/{total}</span></div>
        <div style="font-size:1.3rem;font-weight:700;color:#76b900;margin-top:0.5rem">{grade}</div>
        <div class="score-label">{pct}% accuracy · {f"Final score: {score}/{total}"}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Review")
    for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
        icon = "✅" if a["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i+1}: {q['question']}"):
            st.markdown(f"**Your answer:** `{a['user']}`")
            st.markdown(f"**Correct:** `{a['correct']}`")
            st.markdown(f"{a['explanation']}")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", use_container_width=True):
            use_nim = st.session_state.use_nim
            if use_nim:
                with st.spinner("Generating new questions..."):
                    try:
                        questions = generate_questions_nim(
                            st.session_state.api_key,
                            st.session_state.category,
                            st.session_state.num_q
                        )
                    except Exception:
                        questions = get_questions_offline(st.session_state.category, st.session_state.num_q)
                        use_nim = False
            else:
                questions = get_questions_offline(st.session_state.category, st.session_state.num_q)

            st.session_state.questions = questions
            st.session_state.use_nim = use_nim
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.submitted = False
            st.session_state.phase = "quiz"
            st.rerun()
    with col2:
        if st.button("⚙️ Change Settings", use_container_width=True):
            st.session_state.phase = "setup"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.submitted = False
            st.rerun()

    with st.expander("🔧 DecodeLabs Technical Checklist"):
        st.markdown("""
| Requirement | Implementation |
|---|---|
| ✅ Logic Consistency | `if is_correct: score += 1` |
| ✅ Whitespace Audit | `user.strip()` on every input |
| ✅ Data Normalization | `.lower()` before comparison |
| ✅ Type Integrity | `score = 0` as integer |
| ✅ Output Clarity | f-string for all score display |
| ✅ NVIDIA NIM | AI questions + semantic evaluation (optional) |
| ✅ Offline Mode | Built-in question bank, no key needed |
        """)
