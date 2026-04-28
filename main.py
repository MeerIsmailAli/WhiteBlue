from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# Database Setup (SQLite) it lives in local directory, simplest for common use cases
# -----------------------------
DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    long_url = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# -----------------------------
# App Setup
# -----------------------------
app = FastAPI()

BASE_URL = "http://localhost:8000/"

# -----------------------------
# Request Schema
# -----------------------------
class URLRequest(BaseModel):
    long_url: str

# -----------------------------
# Helper: Generate Short Code
# -----------------------------
def generate_short_code(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

# -----------------------------
# POST /shorten
# -----------------------------
@app.post("/shorten")
def shorten_url(request: URLRequest):
    db = SessionLocal()

    # 1. Check if URL already exists (idempotency)
    existing = db.query(URL).filter(URL.long_url == request.long_url).first()
    if existing:
        return {"short_url": BASE_URL + existing.short_code}

    # 2. Generate short code
    short_code = generate_short_code(request.long_url)

    # 3. Handle collision
    while True:
        collision = db.query(URL).filter(URL.short_code == short_code).first()
        if not collision:
            break
        if collision.long_url == request.long_url:
            return {"short_url": BASE_URL + short_code}
        short_code += "x"

    # 4. Store in DB
    new_url = URL(short_code=short_code, long_url=request.long_url)
    db.add(new_url)
    db.commit()

    return {"short_url": BASE_URL + short_code}

# -----------------------------
# GET /{short_code}
# -----------------------------
@app.get("/{short_code}")
def redirect_url(short_code: str):
    db = SessionLocal()

    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=url_entry.long_url)