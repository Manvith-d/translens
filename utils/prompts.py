# TransLens | Author: Manvith Reddy Dalli | License: MIT

SYSTEM_PLAIN_LANG = """You are an assistant that explains complex information in clear, plain language.
Keep answers concise, direct, and helpful for general audiences.
Avoid jargon. Prefer short sentences and step-by-step bullet points."""

USER_SUMMARY_TEMPLATE = """Summarize the following content in simple, plain language (aim for 150–250 words).
Focus on who is eligible, key steps, deadlines, and required documents.
If information is missing, say so clearly.

CONTENT:
{}
"""

USER_TRANSLATE_TEMPLATE = """Translate the following summary into {target_lang}. 
Keep the tone friendly, respectful, and accessible. Do not add new information.

SUMMARY:
{summary}
"""

USER_QA_TEMPLATE = """You are given context from a public document.
Answer the question **using only the context**. If the answer is unknown or not stated, say "Not specified in the document." Keep your answer to 5-8 concise bullet points.

CONTEXT:
{context}

QUESTION:
{question}
"""
