class Segment:
  value: str
  relative_position: int
  invocation: str

  def __init__(self, relative_position: int):
    self.relative_position = relative_position
    self.invocation = None
    self.value = None
  
  def define(self, string: str, invokable: bool) -> None:
    if invokable:
      self.invocation = string[1:-1]
      self.value = None
    else:
      self.invocation = None
      self.value = string
  
  def __repr__(self):
    return self.value if self.invocation is None or self.value is not None else f'{{{self.invocation}}}'
  
  def bind(self, labels: dict[str, str]) -> bool:
    if self.invocation is None:
      return None
    elif self.invocation in labels:
      self.value = labels[self.invocation]
      return True
    
    self.value = ''.join([' ' if c == '_' else '█' for c in self.value])
    return False