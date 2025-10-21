# TransLens | Author: Manvith Reddy Dalli | License: MIT

import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200):
    chunks = []
    n = len(text)
    i = 0
    while i < n:
        end = min(i + chunk_size, n)
        chunks.append(text[i:end])
        i = end - overlap
        if i < 0:
            i = 0
    return chunks

def clamp_tokens(text: str, max_chars: int = 6000) -> str:
    if not text:
        return ""
    return text[:max_chars]
