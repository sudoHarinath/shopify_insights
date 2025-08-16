from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

class URLIn(BaseModel):
    website_url: HttpUrl
    persist: bool = False
    include_competitors: bool = False  # bonus, simple heuristic

class Product(BaseModel):
    handle: str
    title: str
    product_type: Optional[str] = None
    vendor: Optional[str] = None
    status: Optional[str] = None
    tags: List[str] = []
    url: Optional[str] = None
    images: List[str] = []
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    variants: List[Dict[str, Any]] = []

class Policy(BaseModel):
    kind: str  # privacy, returns, refunds, shipping, terms
    url: Optional[str] = None
    text_excerpt: Optional[str] = None

class FAQItem(BaseModel):
    question: str
    answer: str
    url: Optional[str] = None

class SocialHandle(BaseModel):
    platform: str
    url: str

class Contact(BaseModel):
    emails: List[str] = []
    phones: List[str] = []
    addresses: List[str] = []

class ImportantLinks(BaseModel):
    contact_us: Optional[str] = None
    order_tracking: Optional[str] = None
    blog: Optional[str] = None
    sitemap: Optional[str] = None
    other: Dict[str, str] = {}

class BrandContext(BaseModel):
    website: HttpUrl
    brand_name: Optional[str] = None
    hero_products: List[Product] = []
    catalog: List[Product] = []
    policies: List[Policy] = []
    faqs: List[FAQItem] = []
    socials: List[SocialHandle] = []
    contacts: Contact = Contact()
    about_text: Optional[str] = None
    important_links: ImportantLinks = ImportantLinks()
    meta: Dict[str, Any] = {}

class BrandContextOut(BaseModel):
    ok: bool
    data: Optional[BrandContext] = None
    error: Optional[str] = None

