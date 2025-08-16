import json
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from ..models import (
    Product, Policy, FAQItem, SocialHandle,
    Contact, ImportantLinks, BrandContext
)
from ..utils.text import extract_emails, extract_phones, soup_text, find_socials, abbr
from ..settings import settings

HEADERS = {"User-Agent": settings.USER_AGENT, "Accept": "text/html,application/json"}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
TIMEOUT = settings.TIMEOUT_SECONDS

POLICY_HINTS = {
    "privacy": ["privacy"],
    "returns": ["return", "returns"],
    "refunds": ["refund", "refunds"],
    "shipping": ["shipping", "delivery"],
    "terms": ["terms", "conditions"],
}

FAQ_HINTS = ["faq", "faqs", "help", "support", "questions"]

ABOUT_HINTS = ["about", "our story", "who we are"]

TRACK_HINTS = ["track", "order status"]

def _get(url: str):
    resp = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True)
    return resp

def _abs(base: str, href: str | None) -> str | None:
    if not href: return None
    return urljoin(base, href)

def _is_shopify(base_html: str) -> bool:
    return ("cdn.shopify.com" in base_html) or ("Shopify" in base_html) or ("shopify" in base_html)

def _canonicalize_root(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme or "https"
    return f"{scheme}://{p.netloc}"

class ShopifyScraper:
    def __init__(self, base_url: str):
        self.base_url = _canonicalize_root(base_url)

    def ensure_shopify(self) -> bool:
        r = _get(self.base_url)
        if r.status_code >= 400: return False
        return _is_shopify(r.text)

    def fetch_home(self):
        return _get(self.base_url)

    def fetch_products_json(self):
        # Try /products.json with pagination ?page=1..MAX
        all_products = []
        for page in range(1, settings.MAX_PAGES + 1):
            url = urljoin(self.base_url, f"/products.json?limit=250&page={page}")
            r = _get(url)
            if r.status_code != 200:
                break
            try:
                data = r.json()
            except Exception:
                break
            products = data.get("products", [])
            if not products: break
            all_products.extend(products)
        return all_products

    def parse_products(self, products) -> list[Product]:
        out: list[Product] = []
        for p in products:
            price_min, price_max = None, None
            try:
                prices = [float(v.get("price", 0.0)) for v in p.get("variants", []) if "price" in v]
                if prices:
                    price_min, price_max = min(prices), max(prices)
            except Exception:
                pass
            out.append(Product(
                handle=p.get("handle", ""),
                title=p.get("title", ""),
                product_type=p.get("product_type"),
                vendor=p.get("vendor"),
                status=p.get("status"),
                tags=p.get("tags", []) if isinstance(p.get("tags"), list) else str(p.get("tags","")).split(","),
                url=urljoin(self.base_url, f"/products/{p.get('handle','')}"),
                images=[img.get("src") for img in p.get("images", []) if img.get("src")],
                price_min=price_min,
                price_max=price_max,
                variants=p.get("variants", []),
            ))
        return out

    def find_links(self, html: str) -> dict[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        links = {}
        for a in soup.select("a[href]"):
            text = (a.get_text(" ") or "").strip().lower()
            href = a["href"]
            abs_url = _abs(self.base_url, href)
            if not abs_url: continue
            if any(k in text for k in TRACK_HINTS) and "track" not in links:
                links["order_tracking"] = abs_url
            if "contact" in text and "contact_us" not in links:
                links["contact_us"] = abs_url
            if "blog" in text and "blog" not in links:
                links["blog"] = abs_url
            if "sitemap" in text and "sitemap" not in links:
                links["sitemap"] = abs_url
        return links

    def find_policy_pages(self, html: str) -> list[Policy]:
        soup = BeautifulSoup(html, "html.parser")
        found: dict[str, Policy] = {}
        for a in soup.select("a[href]"):
            text = (a.get_text(" ") or "").strip().lower()
            href = a["href"]
            url = _abs(self.base_url, href)
            if not url: continue
            for kind, hints in POLICY_HINTS.items():
                if any(h in text for h in hints) and kind not in found:
                    # fetch excerpt
                    excerpt = None
                    try:
                        r = _get(url)
                        if r.ok:
                            excerpt = abbr(soup_text(BeautifulSoup(r.text, "html.parser")), 300)
                    except Exception:
                        pass
                    found[kind] = Policy(kind=kind, url=url, text_excerpt=excerpt)
        # also try canonical shopify policy routes
        for kind in ["privacy-policy","refund-policy","shipping-policy","terms-of-service","return-policy"]:
            url = urljoin(self.base_url, f"/policies/{kind}")
            try:
                r = _get(url)
                if r.ok and len(r.text) > 500:
                    s = BeautifulSoup(r.text, "html.parser")
                    found.setdefault(
                        "privacy" if "privacy" in kind else
                        "refunds" if "refund" in kind else
                        "returns" if "return" in kind else
                        "terms" if "terms" in kind else "shipping",
                        Policy(kind="privacy" if "privacy" in kind else
                               "refunds" if "refund" in kind else
                               "returns" if "return" in kind else
                               "terms" if "terms" in kind else "shipping",
                               url=url,
                               text_excerpt=abbr(soup_text(s), 300))
                    )
            except Exception:
                pass
        return list(found.values())

    def find_about(self, html: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        # try meta og:site_name and description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else ""
        # follow About link if present
        about_url = None
        for a in soup.select("a[href]"):
            text = (a.get_text(" ") or "").strip().lower()
            if any(h in text for h in ABOUT_HINTS):
                about_url = _abs(self.base_url, a["href"])
                break
        if about_url:
            try:
                r = _get(about_url)
                if r.ok:
                    return abbr(soup_text(BeautifulSoup(r.text, "html.parser")), 600)
            except Exception:
                pass
        return abbr(desc, 600) if desc else None

    def find_faqs(self, html: str) -> list[FAQItem]:
        faqs: list[FAQItem] = []
        soup = BeautifulSoup(html, "html.parser")
        # JSON-LD FAQPage
        for tag in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(tag.string or "{}")
            except Exception:
                continue
            candidates = data if isinstance(data, list) else [data]
            for d in candidates:
                if d.get("@type") == "FAQPage" and "mainEntity" in d:
                    for e in d["mainEntity"]:
                        q = e.get("name") or e.get("question")
                        a = ""
                        acc = e.get("acceptedAnswer") or {}
                        a = acc.get("text") or ""
                        if q and a:
                            faqs.append(FAQItem(question=q.strip(), answer=abbr(BeautifulSoup(a, "html.parser").get_text(" "), 600)))
        # Crawl likely FAQ pages
        faq_links = set()
        for a in soup.select("a[href]"):
            t = (a.get_text(" ") or "").strip().lower()
            if any(h in t for h in FAQ_HINTS):
                u = _abs(self.base_url, a["href"])
                if u: faq_links.add(u)
        for u in list(faq_links)[:5]:
            try:
                r = _get(u)
                if not r.ok: continue
                s = BeautifulSoup(r.text, "html.parser")
                # naive Q/A pairs collapsed or dt/dd
                for el in s.select("details"):
                    q = (el.find("summary").get_text(" ").strip() if el.find("summary") else "").strip()
                    a = soup_text(el) if not q else soup_text(el).replace(q, "", 1)
                    if q and a: faqs.append(FAQItem(question=q, answer=abbr(a, 600), url=u))
                for qnode, anode in zip(s.select("dt"), s.select("dd")):
                    q = qnode.get_text(" ").strip()
                    a = anode.get_text(" ").strip()
                    if q and a: faqs.append(FAQItem(question=q, answer=abbr(a, 600), url=u))
            except Exception:
                continue
        # de-dup
        seen = set()
        uniq = []
        for f in faqs:
            k = (f.question.lower(), f.answer[:50])
            if k in seen: continue
            seen.add(k)
            uniq.append(f)
        return uniq[:100]

    def hero_products(self, home_html: str, catalog: list[Product]) -> list[Product]:
        soup = BeautifulSoup(home_html, "html.parser")
        links = [a["href"] for a in soup.select("a[href*='/products/']")]
        handles = set()
        for href in links:
            m = re.search(r"/products/([^/?#]+)", href)
            if m: handles.add(m.group(1))
        by_handle = {p.handle: p for p in catalog}
        heroes = []
        for h in handles:
            if h in by_handle:
                heroes.append(by_handle[h])
        return heroes[:20]

    def extract_contacts(self, html: str) -> Contact:
        emails = extract_emails(html)
        phones = extract_phones(html)
        # try Contact page
        soup = BeautifulSoup(html, "html.parser")
        contact_urls = []
        for a in soup.select("a[href]"):
            if "contact" in (a.get_text(" ") or "").strip().lower():
                u = _abs(self.base_url, a["href"])
                if u: contact_urls.append(u)
        addresses = []
        for u in contact_urls[:3]:
            try:
                r = _get(u)
                if not r.ok: continue
                s = BeautifulSoup(r.text, "html.parser")
                txt = soup_text(s)
                emails.extend(extract_emails(r.text))
                phones.extend(extract_phones(r.text))
                # naive address sniff
                for tag in s.select("address"):
                    t = " ".join(tag.get_text(" ").split())
                    if t: addresses.append(t)
            except Exception:
                pass
        return Contact(emails=sorted(set(emails)), phones=sorted(set(phones)), addresses=sorted(set(addresses)))

    def socials(self, html: str) -> list[SocialHandle]:
        pairs = find_socials(html)
        return [SocialHandle(platform=p, url=u) for p, u in pairs]

    def brand_name(self, html: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        og = soup.find("meta", property="og:site_name")
        if og and og.get("content"): return og["content"].strip()
        title = soup.find("title")
        return title.get_text(" ").strip() if title else None

    def collect(self) -> BrandContext:
        home = self.fetch_home()
        html = home.text
        catalog_raw = self.fetch_products_json()
        catalog = self.parse_products(catalog_raw)
        heroes = self.hero_products(html, catalog)
        policies = self.find_policy_pages(html)
        faqs = self.find_faqs(html)
        socials = self.socials(html)
        contacts = self.extract_contacts(html)
        links_map = self.find_links(html)
        about_text = self.find_about(html)
        name = self.brand_name(html)
        important = ImportantLinks(
            contact_us=links_map.get("contact_us"),
            order_tracking=links_map.get("order_tracking"),
            blog=links_map.get("blog"),
            sitemap=links_map.get("sitemap"),
            other={k: v for k, v in links_map.items() if k not in {"contact_us","order_tracking","blog","sitemap"}},
        )
        return BrandContext(
            website=self.base_url,
            brand_name=name,
            hero_products=heroes,
            catalog=catalog,
            policies=policies,
            faqs=faqs,
            socials=socials,
            contacts=contacts,
            about_text=about_text,
            important_links=important,
            meta={"catalog_count": len(catalog_raw)},
        )

    # naive competitor heuristic: parse homepage footer for "as seen in" or "brands" and collect external shopify domains
    def competitors(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        urls = set()
        base_domain = urlparse(self.base_url).netloc
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.startswith("http"):
                dn = urlparse(href).netloc
                if dn != base_domain and "shopify" in href:
                    urls.add(f"{urlparse(href).scheme}://{dn}")
        return list(urls)[:3]
