# TransLens | Author: Manvith Reddy Dalli | License: MIT

import os
import io
import streamlit as st
from typing import List, Tuple
from openai import OpenAI
from pypdf import PdfReader

from utils.text_utils import clean_text, chunk_text, clamp_tokens
from utils.prompts import (
    SYSTEM_PLAIN_LANG,
    USER_SUMMARY_TEMPLATE,
    USER_TRANSLATE_TEMPLATE,
    USER_QA_TEMPLATE,
)

APP_TITLE = "TransLens — Accessible Public Information"
APP_SUBTITLE = "Summarize → Translate → Ask Questions (Gov/Health/Civic content)"

# ---------- Config & Client ----------
def get_openai_client():
    # Prefer Streamlit secrets; fall back to env var
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    if not api_key:
        st.warning("⚠️ Add your OpenAI key in .streamlit/secrets.toml or as env var OPENAI_API_KEY to use the app.")
    return OpenAI(api_key=api_key) if api_key else None

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in pdf.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            pass
    return "\n".join(parts)

def read_uploaded_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file.read())
    else:
        # Assume text
        data = uploaded_file.read()
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return data.decode("latin-1", errors="ignore")

# ---------- LLM Helpers ----------
def llm_chat(client: OpenAI, system_prompt: str, user_prompt: str, model="gpt-4o-mini", max_tokens=800) -> str:
    if client is None:
        return "⚠️ OpenAI API key not configured."
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # Lightweight fallback to a commonly-available model name
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e2:
            return f"LLM error: {e2}"

# ---------- UI ----------
st.set_page_config(page_title="TransLens", page_icon="🗣️", layout="wide")
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

with st.expander("ℹ️ What is this?", expanded=False):
    st.markdown(
        """
**TransLens** helps make complex government and healthcare information easier to understand.
- Paste text or upload a PDF / text file.
- Get a **plain-language summary**.
- **Translate** it to a language of your choice.
- **Ask questions** about the content.

> Designed for accessibility and civic inclusion.
"""
    )

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1) Input")
    source_choice = st.radio("Choose input type:", ["Paste text", "Upload file"], horizontal=True)
    raw_text = ""
    uploaded = None
    if source_choice == "Paste text":
        raw_text = st.text_area("Paste government or healthcare text here", height=220, placeholder="Paste policy, IEP, healthcare info...")
    else:
        uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
        if uploaded:
            raw_text = read_uploaded_file(uploaded)

    lang = st.selectbox(
        "Translate summary into:",
        [
            ("English", "en"),
            ("Hindi", "hi"),
            ("Kannada", "kn"),
            ("Spanish", "es"),
            ("Tamil", "ta"),
            ("Telugu", "te"),
            ("Arabic", "ar"),
            ("Chinese (Simplified)", "zh"),
        ],
        format_func=lambda x: x[0]
    )

    max_context_chars = st.slider("Context size (characters to include for Q&A)", min_value=2000, max_value=20000, value=8000, step=1000)

with col_right:
    st.subheader("2) Summary & Translation")
    client = get_openai_client()

    cleaned = clean_text(raw_text)
    if cleaned:
        # Summarize in plain language
        if st.button("🔎 Simplify & Translate", use_container_width=True):
            # Create a compact summary
            user_sum = USER_SUMMARY_TEMPLATE.format(text=clamp_tokens(cleaned, max_chars=6000))
            simple_summary = llm_chat(client, SYSTEM_PLAIN_LANG, user_sum, max_tokens=500)

            # Translate using the LLM (single vendor dependency)
            user_tr = USER_TRANSLATE_TEMPLATE.format(summary=simple_summary, target_lang=lang[0])
            translated = llm_chat(client, SYSTEM_PLAIN_LANG, user_tr, max_tokens=500)

            st.markdown("#### Plain-Language Summary")
            st.write(simple_summary)

            st.markdown(f"#### Translated Summary ({lang[0]})")
            st.write(translated)

            st.session_state["ctx_text"] = cleaned
            st.session_state["summary"] = simple_summary
            st.session_state["translated"] = translated
    else:
        st.info("Paste text or upload a document to begin.")

st.divider()

st.subheader("3) Ask Questions about the Document")
question = st.text_input("What would you like to know?", placeholder="e.g., Who is eligible? What are the steps? Deadlines?")
ask_btn = st.button("💬 Answer from the Document")

if ask_btn:
    if not raw_text:
        st.warning("Please provide some input text or upload a file first.")
    else:
        # Prepare context chunks and clamp
        ctx = clamp_tokens(st.session_state.get("ctx_text", cleaned), max_chars=max_context_chars)
        user_qa = USER_QA_TEMPLATE.format(context=ctx, question=question)
        answer = llm_chat(client, SYSTEM_PLAIN_LANG, user_qa, max_tokens=600)

        st.markdown("#### Answer")
        st.write(answer)

        with st.expander("Show the (truncated) context used", expanded=False):
            st.code(ctx[:2000] + ("..." if len(ctx) > 2000 else ""))

st.divider()
with st.expander("🔐 Privacy & Ethics"):
    st.markdown(
        """
- No data is stored by this demo beyond your session.
- Always verify AI-generated content with official sources.
- Use accessible language and consider community review when deploying.
"""
    )

st.caption("© 2025 TransLens")
