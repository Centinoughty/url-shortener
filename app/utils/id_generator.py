import secrets
from threading import Lock


class ShardAwareIDGenerator:
  """Generate distributed IDs using machine-id bits + sequence bits."""

  BASE62_LENGTH = 6
  BASE62_CAP = (62 ** BASE62_LENGTH) - 1

  def __init__(
    self,
    machine_id: int,
    machine_id_bits: int = 15,
    sequence_bits: int = 20,
    randomize_machine_id_if_zero: bool = True,
    randomize_sequence_start: bool = True
  ):
    if machine_id_bits <= 0:
      raise ValueError("machine_id_bits must be > 0")

    if sequence_bits <= 0:
      raise ValueError("sequence_bits must be > 0")

    if machine_id == 0 and randomize_machine_id_if_zero:
      machine_id = secrets.randbits(machine_id_bits)
      if machine_id == 0:
        machine_id = 1

    max_machine_id = (1 << machine_id_bits) - 1
    if machine_id < 0 or machine_id > max_machine_id:
      raise ValueError(f"machine_id must be between 0 and {max_machine_id}")

    self.machine_id = machine_id
    self.machine_id_bits = machine_id_bits
    self.sequence_bits = sequence_bits
    self.max_sequence = (1 << sequence_bits) - 1

    max_id_for_machine = (self.machine_id << self.sequence_bits) | self.max_sequence
    if max_id_for_machine > self.BASE62_CAP:
      raise ValueError(
        "Configured machine_id/machine_id_bits/sequence_bits exceed 6-char Base62 cap"
      )

    if randomize_sequence_start:
      min_sequence = 1 << (sequence_bits - 1) if sequence_bits > 1 else 0
      self._sequence = min_sequence + secrets.randbelow(self.max_sequence - min_sequence + 1)
    else:
      self._sequence = 0

    self._lock = Lock()

  def generate_id(self) -> int:
    with self._lock:
      if self._sequence > self.max_sequence:
        raise OverflowError(
          "Sequence exhausted for configured sequence_bits. "
          "Increase sequence_bits or rotate machine_id."
        )

      sequence = self._sequence
      id_value = (self.machine_id << self.sequence_bits) | sequence
      if id_value > self.BASE62_CAP:
        raise OverflowError("Generated ID exceeded 6-char Base62 cap")

      self._sequence += 1

    return id_value
