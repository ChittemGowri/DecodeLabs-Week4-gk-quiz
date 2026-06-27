# 🧠 General Knowledge Quiz — DecodeLabs Project 4

**Python Programming · Industrial Training Kit**  
Powered by NVIDIA NIM (LLaMA 3.1 8B Instruct)

---

## What This Does

- AI generates quiz questions on your chosen topic via NVIDIA NIM API
- Accepts user text input, sanitizes with `.strip().lower()`
- Evaluates answers with `if-else` control flow
- Optional: semantic answer checking (handles "Paris" = "paris" = "PARIS")
- Displays final score with f-string interpolation

Covers all DecodeLabs Project 4 requirements:
- ✅ Logic Consistency
- ✅ Whitespace Audit (`.strip()`)
- ✅ Data Normalization (`.lower()`)
- ✅ Type Integrity (`score = 0`)
- ✅ Output Clarity (f-strings)

---

## Files

```
gk_quiz/
├── app.py               ← Main Streamlit app
├── requirements.txt     ← Dependencies
├── .streamlit/
│   └── secrets.toml    ← Optional: store your API key
└── README.md
```

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repo (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your repo → set `app.py` as the main file
4. In **Advanced settings → Secrets**, add:
   ```toml
   NVIDIA_API_KEY = "nvapi-xxxxxxxxxxxx"
   ```
5. Click **Deploy**

---

## Get NVIDIA NIM API Key (Free)

1. Go to [build.nvidia.com](https://build.nvidia.com)
2. Sign up / log in
3. Navigate to **API Keys** → Generate key
4. Paste in the app's configuration screen

---

## Model Used

`meta/llama-3.1-8b-instruct` via NVIDIA NIM inference endpoint  
(`https://integrate.api.nvidia.com/v1`)

Compatible with OpenAI Python SDK — no extra library needed.
