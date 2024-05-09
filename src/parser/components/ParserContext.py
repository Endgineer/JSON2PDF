from lexer.Lexer import Lexer
from lexer.components.Token import Token

class ParserContext:
  lexer: Lexer
  matched_token: Token

  def __init__(self, lexer: Lexer):
    self.lexer = lexer
    self.matched_token = None
  
  def match(self, target_token_kind: Token.Kind) -> bool:
    lookahead_token_kind = self.lexer.peek()

    if lookahead_token_kind is not None and lookahead_token_kind == target_token_kind:
      token = self.lexer.scan()
      if token.kind == Token.Kind.STRING:
        self.matched_token = token
      return True
    
    return False