import hashlib
import re

_ws = re.compile(r"\s+")

def normalize_text(s: str) -> str:
    s = (s or "").lower().strip()
    s = _ws.sub(" ", s)
    s = re.sub(r"[^a-z0-9\s\-\+\.]", "", s)
    return s

def dedup_key(title: str, company: str, location: str) -> str:
    base = f"{normalize_text(company)}|{normalize_text(title)}|{normalize_text(location)}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()
