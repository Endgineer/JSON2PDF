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
  
  def invoke(self, labels: dict[str, str], anonymize: bool) -> bool:
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