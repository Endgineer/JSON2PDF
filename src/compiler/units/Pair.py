from compiler.units.Token import Token

class Pair:
  contents: list[Token]

  def __init__(self, key: Token):
    self.contents = [ key ]
  
  def __repr__(self):
    return f'{tuple(None if token is None else token.value for token in self.contents)}'
  
  def try_fill(self, token: Token) -> bool:
    if len(self.contents) == 2: return False
    self.contents.append(token)
    return True