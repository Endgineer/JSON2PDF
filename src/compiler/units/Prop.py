from compiler.units.Token import Token
from compiler.units.Pair import Pair

class Prop:
  key: Token
  value: Token | list[Token] | list[Pair]
  kind: type

  def __init__(self):
    self.key = None
    self.value = None
    self.kind = None
  
  def __repr__(self):
    return f'{(self.key.get_string(), self.value.get_string() if self.kind == str else ([token.get_string() for token in self.value] if self.kind == list else self.value))}'
  
  def fill(self, token: Token) -> None:
    if self.key is None:
      self.key = token
    elif self.kind == str:
      self.value = token
    elif self.kind == list:
      self.value.append(token)
    elif self.kind == dict and (len(self.value) == 0 or not self.value[-1].try_fill(token)):
      self.value.append(Pair(token))