import os
from app.utils.base62 import encode
from app.utils.id_generator import ShardAwareIDGenerator

machine_id = int(os.getenv("MACHINE_ID", "0"))
id_generator = ShardAwareIDGenerator(machine_id=machine_id)

def generate_short():
  raw_id = id_generator.generate_id()
  print(raw_id)
  return encode(raw_id)