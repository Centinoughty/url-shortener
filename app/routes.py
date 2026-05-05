from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services import shortener

router = APIRouter()

@router.post("/shorten")
def shorten_url(long_url: str):
  short = shortener.generate_short()

  return {"short_url": short}


@router.get("/{short}")
def redirect(short: str):
  return RedirectResponse(url="https://google.com")
