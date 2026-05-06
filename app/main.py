from fastapi import FastAPI
from app.services.db import init_db
from app.routes import router

app = FastAPI()

@app.on_event('startup')
def startup():
  init_db()

app.include_router(router=router)
