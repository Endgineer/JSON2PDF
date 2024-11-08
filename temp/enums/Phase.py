import enum

class Phase(enum.Enum):
  def _generate_next_value_(name: str, start: int, count: int, last_values: list[int]) -> int:
    return count
  
  COMPILE = enum.auto()
  LEXICAL = enum.auto()
  SYNTAX = enum.auto()
  SEMANTIC = enum.auto()
  LINKING = enum.auto()
  SYNTHESIS = enum.auto()
