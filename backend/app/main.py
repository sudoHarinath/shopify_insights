from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import URLIn, BrandContextOut
from .scraper.shopify_scraper import ShopifyScraper
from .settings import settings
from .db import SessionLocal, Brand, ProductRow, engine

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/insights", response_model=BrandContextOut)
def insights(payload: URLIn):
    scraper = ShopifyScraper(str(payload.website_url))
    try:
        if not scraper.ensure_shopify():
            raise HTTPException(status_code=401, detail="Website not found or not a Shopify storefront")

        ctx = scraper.collect()

        # naive competitors bonus
        if payload.include_competitors:
            try:
                comp_urls = scraper.competitors(scraper.fetch_home().text)
                ctx.meta["competitors_sample"] = comp_urls
            except Exception:
                ctx.meta["competitors_sample"] = []

        if payload.persist and SessionLocal:
            with SessionLocal() as s:
                b = s.query(Brand).filter(Brand.website == str(ctx.website)).one_or_none()
                if not b:
                    b = Brand(website=str(ctx.website))
                    s.add(b)
                    s.flush()
                b.name = ctx.brand_name
                b.about_text = ctx.about_text
                b.meta = ctx.meta
                s.query(ProductRow).filter(ProductRow.brand_id == b.id).delete()
                for p in ctx.catalog[:1000]:
                    s.add(ProductRow(
                        brand_id=b.id, handle=p.handle, title=p.title,
                        product_type=p.product_type, vendor=p.vendor, status=p.status,
                        url=p.url, images=p.images, price_min=p.price_min, price_max=p.price_max, tags=p.tags
                    ))
                s.commit()

        return BrandContextOut(ok=True, data=ctx)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e!s}")
