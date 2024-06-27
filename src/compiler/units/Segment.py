import pylatex

class Segment:
  active: bool
  value: str
  relative_position: int
  invocation: str

  def __init__(self, relative_position: int):
    self.relative_position = relative_position
    self.invocation = None
    self.active = False
    self.value = None
  
  def define_as_plain(self, string: str) -> None:
    self.value = string
  
  def define_as_invokable(self, string: str) -> None:
    self.invocation = string[1:-1]
  
  def __repr__(self):
    if self.invocation is None:
      return pylatex.escape_latex(self.value) if self.active else self.value
    
    return pylatex.escape_latex(self.value) if self.active else f'{{{self.invocation}}}'
  
  def activate(self, labels: dict[str, str], anonymize: bool) -> bool:
    if self.active: return None
    self.active = True
  
    if self.invocation is None:
      return None
    elif anonymize:
      if self.invocation in labels:
        self.value = labels[self.invocation]
        return True
      
      self.value = ''.join(['█' if c.isalnum() else c for c in self.invocation])
      return False
    else:
      self.value = self.invocation
      return self.invocation in labels