import enum

from compiler.units.Prop import Prop
from compiler.units.Token import Token

class Item:
  class Kind(enum.Enum):
    CVPARAGRAPH = 0
    CVSKILLS = 1
    CVENTRIES = 2
    CVHONORS = 3
    CLLETTER = 4
  
  section: Token
  reference: Token
  line_number: int
  char_number: int
  properties: list[Prop]
  kind: Kind
  labels: dict[str, Token]

  def __init__(self, section: Token, reference: Token, line_number: int, char_number: int, properties: list[Prop]):
    self.section = section
    self.reference = reference
    self.line_number = line_number
    self.char_number = char_number
    self.properties = properties
    self.kind = None
    self.labels = None
  
  def __repr__(self):
    return ''.join([
      f'of type {self.kind.name} ' if self.kind is not None else '',
      f'referenced by "{self.reference.get_string()}" ' if self.reference is not None else '',
      f'at line {self.line_number} position {self.char_number}'
    ])