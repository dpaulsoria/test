import re

def _tokens(text: str) -> set[str]:
    text = (text or "").lower()
    return set(re.findall(r"[a-z0-9\+\#\.]{2,}", text))

def score_job(profile_keywords: list[str], exclude: list[str], title: str, desc: str) -> int:
    t = _tokens(title) | _tokens(desc)

    kw = [k.strip().lower() for k in profile_keywords if k.strip()]
    ex = [k.strip().lower() for k in exclude if k.strip()]

    # base score por matches
    score = 0
    for k in kw:
        if k in t:
            score += 10

    # penalizaciones
    for bad in ex:
        if bad in t:
            score -= 25

    # penaliza restricciones comunes
    restriction_terms = {"eu", "europe", "must", "based", "onsite", "relocation"}
    if "eu" in t and ("based" in t or "only" in t):
        score -= 15
    if "onsite" in t:
        score -= 30

    return max(0, min(100, score))
