from compiler.consts.typing import SyntacticTypes

class Item:
  section: str
  reference: str
  line_number: int
  char_number: int
  properties: list[SyntacticTypes.ItemProperty]

  def __init__(self, section: str, reference: str, line_number: int, char_number: int, properties: list[SyntacticTypes.ItemProperty]):
    self.section = section
    self.reference = reference
    self.line_number = line_number
    self.char_number = char_number
    self.properties = properties
  
  def __repr__(self):
    refstr = f'referenced by "{self.reference}" ' if self.reference is not None else ''
    return f'{refstr}at line {self.line_number} position {self.char_number}'