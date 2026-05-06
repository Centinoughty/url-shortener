import os
from app.utils.base62 import encode
from app.utils.id_generator import ShardAwareIDGenerator

class ShortCodeGenerator:
  def __init__(self, machine_id: int | None = None):
    self.machine_id = (
      machine_id
      if machine_id is not None
      else int(os.getenv("MACHINE_ID", "0"))
    )

    self.id_generator = ShardAwareIDGenerator(
      machine_id=self.machine_id
    )

  def generate(self) -> str:
    raw_id = self.id_generator.generate_id()
    print(f"Generated Raw ID: ", raw_id)

    return encode(raw_id)
