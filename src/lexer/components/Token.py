import enum

class Token:
  class Kind(enum.Enum):
    DISCARDED = 0
    LBRACE = 1
    RBRACE = 2
    LBRACKET = 3
    RBRACKET = 4
    COLON = 5
    COMMA = 6
    STRING = 7
  
  value: str
  kind: Kind
  line_number: int
  char_number: int

  def __init__(self, value: str, kind: Kind, line_number: int, char_number: int):
    self.value = value
    self.kind = kind
    self.line_number = line_number
    self.char_number = char_number
  
  def __repr__(self):
    return f'{self.kind.name} at line {self.line_number} position {self.char_number}{"" if self.value is None else ": "+repr(self.value)[1:-1]}'