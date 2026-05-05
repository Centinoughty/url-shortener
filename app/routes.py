from fastapi import APIRouter

router = APIRouter()

@router.post("/shorten")
def shorten_url(long_url: str):
  return {"short_url": long_url}
