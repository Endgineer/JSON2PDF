import enum

class IdentifierVerifier:
  class State(enum.Enum):
    ACCEPT_SYLLABLE = 0
    ACCEPT_DELIMITER = 1
  
  state: State
  
  DELIMITERS = { '_', '-', '.', '/' }
  UNARY_OPS = { '#', '@', '$', '&', '?', ':' }
  BINARY_OPS = { '=' }
  
  def __init__(self):
    self.state = None
  
  def __call__(self, identifier: str) -> bool:
    self.state = IdentifierVerifier.State.ACCEPT_SYLLABLE

    for char in identifier:
      if self.state == IdentifierVerifier.State.ACCEPT_SYLLABLE:
        if not char.isalnum():
          return False
        self.state = IdentifierVerifier.State.ACCEPT_DELIMITER
      elif self.state == IdentifierVerifier.State.ACCEPT_DELIMITER:
        if char.isalnum():
          pass
        elif char in IdentifierVerifier.DELIMITERS or char in IdentifierVerifier.UNARY_OPS or char in IdentifierVerifier.BINARY_OPS:
          self.state = IdentifierVerifier.State.ACCEPT_SYLLABLE
        else:
          return False
    
    return True