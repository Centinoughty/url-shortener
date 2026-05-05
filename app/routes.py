from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.services import db, shortener, cache
from datetime import datetime

router = APIRouter()

@router.post("/shorten")
def shorten_url(long_url: str):
  short = shortener.generate_short()

  db.session.execute(
    "INSERT INTO urls (short_url, original_url, created_at) VALUES (%s, %s, %s)",
    (short, long_url, datetime.now())
  )

  cache.set(short, long_url)

  return {"short_url": short}


@router.get("/{short}")
def redirect(short: str):
  long_url = cache.get(short)

  if not long_url:
    rows = db.session.execute(
      "SELECT original_url FROM urls WHERE short_url=%s",
      (short,)
    )

    row = rows.one()

    if not row:
      raise HTTPException(status_code=404, detail="Not found")

    long_url = row.original_url
    cache.set(short, long_url)
  
  cache.increment(f"clicks:{short}")

  assert long_url is not None
  return RedirectResponse(url=long_url)
