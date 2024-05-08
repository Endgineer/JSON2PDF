from lexer.Lexer import Lexer
from lexer.components.Token import Token

class ParserContext:
  lexer: Lexer
  last_string: Token

  def __init__(self, lexer: Lexer):
    self.lexer = lexer
    self.last_string = None
  
  def match(self, target_token_kind: Token.Kind) -> bool:
    lookahead_token_kind = self.lexer.peek()

    if lookahead_token_kind is not None and lookahead_token_kind == target_token_kind:
      token = self.lexer.scan()
      if token.kind == Token.Kind.STRING:
        self.last_string = token.value[1:-1]
      return True
    
    return False