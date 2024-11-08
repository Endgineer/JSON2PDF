import enum

class Document(enum.Enum):
  def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
    return count
  
  CV = enum.auto()
  CL = enum.auto()
