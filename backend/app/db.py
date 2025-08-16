from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .settings import settings

Base = declarative_base()
engine = None
SessionLocal = None

if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    website = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    about_text = Column(Text)
    meta = Column(JSON)

class ProductRow(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"))
    handle = Column(String(255))
    title = Column(String(255))
    product_type = Column(String(255))
    vendor = Column(String(255))
    status = Column(String(50))
    url = Column(Text)
    images = Column(JSON)
    price_min = Column(Float)
    price_max = Column(Float)
    tags = Column(JSON)

if engine:
    Base.metadata.create_all(engine)
