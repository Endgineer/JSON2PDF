from compiler.units.Token import Token

class Pair:
  contents: list[Token]

  def __init__(self, key: Token):
    self.contents = [ key ]
  
  def __repr__(self):
    return f'{tuple(None if token is None else token.get_string() for token in self.contents)}'
  
  def __getitem__(self, index: int):
    return self.contents[index]
  
  def try_fill(self, token: Token) -> bool:
    if len(self.contents) == 2: return False
    self.contents.append(token)
    return True