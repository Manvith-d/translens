
# TransLens - Accessible Public Information

**TransLens** makes complex government and healthcare information easier to understand.
- Paste text or upload a PDF/TXT
- Get a **plain-language summary**
- **Translate** the summary into your preferred language
- **Ask questions** grounded in the provided document

Built for **accessibility**, **civic inclusion**, and **responsible AI**.

---

##  Features
- **Plain-Language Summaries** - simple explanations for general audiences
- **Multi-language Translation** - translate summaries via the same LLM (no extra APIs)
- **Grounded Q&A** - ask questions answered *only* from your uploaded/pasted content
- **PDF & Text Support** - upload a document or paste content directly
- **No external storage** - demo keeps data in your session only

---

##  Tech Stack
- Python, Streamlit
- OpenAI Chat Completions API (e.g., `gpt-4o-mini`, fallback `gpt-3.5-turbo`)
- PyPDF for text extraction from PDFs

> Why not a separate Translate API? To reduce dependencies and keep setup simple, translations are performed by the LLM itself with explicit instructions.

---

##  Quickstart (Local)

```bash
git clone https://github.com/<your-username>/translens.git
cd translens
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Add your OpenAI key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit the file and paste your key
# or: export OPENAI_API_KEY=sk-...

streamlit run app.py
```

Open your browser at the URL shown (usually `http://localhost:8501`).

---

##  Try It Fast
Use the sample file:
```
assets/sample_texts/sample_policy_en.txt
```
- Upload it, click **"🔎 Simplify & Translate"**
- Then ask a question like: *"What documents are required?"*

---

##  How It Works
1. **Clean & Clamp** input text for safe token limits
2. **Summarize** with a plain-language system prompt
3. **Translate** the summary to the target language (LLM-based)
4. **Q&A**: Stuff the (truncated) context and answer strictly from it

> Note: For larger documents, a vector index (embeddings + retrieval) can be added. The current version uses a robust "context stuffing" strategy with a user-controlled context size slider.

---

##  Privacy & Responsible Use
- No data is stored outside your session.
- Always verify AI-generated guidance with official sources.
- Prefer community review for deployment in sensitive contexts.

---

##  Project Structure
```
translens/
├── app.py
├── requirements.txt
├── README.md
├── utils/
│   ├── __init__.py
│   ├── text_utils.py
│   └── prompts.py
├── assets/
│   └── sample_texts/
│       └── sample_policy_en.txt
└── .streamlit/
    └── secrets.toml.example
```

---

##  Roadmap
- [ ] Retrieval with embeddings (OpenAI `text-embedding-3-small`)
- [ ] Prompted literacy-level control (e.g., 5th/8th grade reading)
- [ ] Audio mode (text-to-speech) and WhatsApp integration
- [ ] Usage analytics & feedback collection
- [ ] Multi-file compare + bilingual outputs side-by-side

---

##  License
MIT
