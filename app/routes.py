from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.services.shortener import ShortCodeGenerator
from app.services.cache import RedisManager
from datetime import datetime

router = APIRouter()
redis_manager = RedisManager()

@router.post("/shorten")
def shorten_url(long_url: str, request: Request):
  db = request.app.state.db
  short_generator = ShortCodeGenerator()
  short_code = short_generator.generate()

  db.insert(
    table_name="urls",
    columns=["short_url", "original_url", "created_at"],
    values=(
        short_code,
        long_url,
        datetime.now()
    )
  )

  redis_manager.set(short_code, long_url)

  return {"short_url": short_code}


@router.get("/{short}")
def redirect(short: str, request: Request):
  db = request.app.state.db
  long_url = redis_manager.get(short)

  if not long_url:
    row = db.select_one(
      table_name="urls",
      where_clause="short_url = %s",
      values=(short,)
    )

    if not row:
      raise HTTPException(status_code=404, detail="Not found")

    long_url = row.original_url
    redis_manager.set(short, long_url)
  
  redis_manager.increment(f"clicks:{short}")

  assert long_url is not None
  return RedirectResponse(url=long_url)
