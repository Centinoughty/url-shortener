from app.utils.base62 import encode

counter = 100000

def generate_short():
  global counter
  counter += 1
  return encode(counter)