import pylatex

class Segment:
  active: bool
  value: str
  relative_position: int
  invocation: str
  bold: bool

  def __init__(self, relative_position: int):
    self.relative_position = relative_position
    self.invocation = None
    self.active = False
    self.value = None
    self.bold = False
  
  def define_as_plain(self, string: str) -> None:
    self.value = string
  
  def define_as_invokable(self, string: str) -> None:
    self.invocation = string[1:-1]
  
  def define_as_bold(self, string: str) -> None:
    self.value = string[2:-2]
    self.bold = True
  
  def __repr__(self):
    if self.bold:
      return f'\\textbf{{{pylatex.escape_latex(self.value)}}}' if self.active else f'**{self.value}**'

    if self.invocation is None:
      return pylatex.escape_latex(self.value) if self.active else self.value
    
    return pylatex.escape_latex(self.value) if self.active else f'{{{self.invocation}}}'
  
  def activate(self, labels: dict[str], anonymize: bool, bolded: bool) -> bool:
    if self.active: return None
    self.active = True

    if not bolded:
      self.bold = False
  
    if self.invocation is None:
      return None
    elif anonymize:
      if self.invocation in labels:
        self.value = labels[self.invocation].get_string()
        return True
      
      self.value = ''.join(['█' if c.isalnum() else c for c in self.invocation])
      return False
    else:
      self.value = self.invocation
      return self.invocation in labels