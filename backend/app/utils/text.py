import re
from bs4 import BeautifulSoup
from typing import Iterable, List

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3,4}\)?[-.\s]?)?\d{3}[-.\s]?\d{4,6}")

SOCIAL_PATTERNS = {
    "instagram": r"instagram\.com\/[A-Za-z0-9_.%-]+",
    "facebook": r"facebook\.com\/[A-Za-z0-9_.%-]+",
    "tiktok": r"tiktok\.com\/@[A-Za-z0-9_.%-]+",
    "twitter": r"(?:x|twitter)\.com\/[A-Za-z0-9_.%-]+",
    "youtube": r"youtube\.com\/(?:c\/|channel\/|@)[A-Za-z0-9_\-]+",
    "pinterest": r"pinterest\.com\/[A-Za-z0-9_.%-]+",
    "linkedin": r"linkedin\.com\/company\/[A-Za-z0-9_.%-]+",
}

def extract_emails(text: str) -> List[str]:
    return sorted(set(EMAIL_RE.findall(text)))

def extract_phones(text: str) -> List[str]:
    return sorted(set(PHONE_RE.findall(text)))

def soup_text(soup: BeautifulSoup) -> str:
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    return " ".join(soup.get_text(" ").split())

def find_socials(html: str) -> List[tuple[str, str]]:
    found = []
    for platform, pat in SOCIAL_PATTERNS.items():
        for m in re.findall(pat, html, flags=re.I):
            url = "https://" + m if not m.startswith("http") else m
            found.append((platform, url))
    # also check <a> tags
    return list({(p, u) for p, u in found})

def abbr(text: str, n: int = 400) -> str:
    t = " ".join(text.split())
    return t[: n - 3] + "..." if len(t) > n else t
