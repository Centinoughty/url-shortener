from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.services import db, shortener
from datetime import datetime

router = APIRouter()

@router.post("/shorten")
def shorten_url(long_url: str):
  short = shortener.generate_short()

  db.session.execute(
    "INSERT INTO urls (short_url, original_url, created_at) VALUES (%s, %s, %s)",
    (short, long_url, datetime.now())
  )

  return {"short_url": short}


@router.get("/{short}")
def redirect(short: str):
  rows = db.session.execute(
    "SELECT original_url FROM urls WHERE short_url=%s",
    (short,)
  )

  row = rows.one()

  if not row:
    raise HTTPException(status_code=404, detail="Not found")

  long_url = row.original_url

  return RedirectResponse(url=long_url)
