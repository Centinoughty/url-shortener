from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes import router
from app.services.db import DBManager

db = DBManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
  """
  Initialize and tear down application resources.
  """

  db.connect()
  app.state.db = db

  # Create keyspace
  db.create_keyspace()

  # Use keyspace
  db.use_keyspace()

  # Create table
  db.create_table(
    table_name="urls",
    schema="""
      short_url text PRIMARY KEY,
      original_url text,
      created_at timestamp
    """
  )

  print("Database initialized successfully")

  try:
    yield
  finally:
    db.shutdown()
    print("Database connection closed")


app = FastAPI(
  title="URL Shortener",
  version="1.0.0",
  lifespan=lifespan,
)


app.include_router(router=router)
