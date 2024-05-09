import logging

from compiler.components.Token import Token
from lexer.components.LexerContext import LexerContext
from lexer.routines.matchers import *

class Lexer():
  lexer_ctx: LexerContext

  def __init__(self, filepath: str):
    logging.getLogger('LEXICAL').debug(f'Switched context to "{filepath}"...')
    self.lexer_ctx = LexerContext(filepath)
    self.scan()
  
  def scan(self) -> Token:
    while True:
      while self.lexer_ctx.at_end_of_file():
        if self.lexer_ctx.state != LexerContext.State.START:
          self.__discard_context()
        else:
          return self.__advance_tokens()
      
      self.lexer_ctx.scan_next_char()

      if match_str_char(self.lexer_ctx): pass
      elif match_start(self.lexer_ctx): pass
      
      if self.lexer_ctx.matched_token_kind is None:
        pass
      elif self.lexer_ctx.matched_token_kind == Token.Kind.DISCARDED:
        self.__discard_context()
      else:
        return self.__advance_tokens()
  
  def peek(self) -> Token.Kind:
    return None if self.lexer_ctx.matched_token is None else self.lexer_ctx.matched_token.kind

  def context_switch(self, filepath) -> None:
    logging.getLogger('LEXICAL').debug(f'Switched context to "{filepath}"...')
    self.lexer_ctx.switch(filepath)
    self.scan()

  def __advance_tokens(self) -> Token:
    token = self.lexer_ctx.matched_token
    self.lexer_ctx.capture_token()
    
    if token is not None:
      logging.getLogger('LEXICAL').debug(f'Scanned {token}.')
    
    return token
  
  def __discard_context(self) -> None:
    logging.getLogger('LEXICAL').error(f'Unexpected symbol {self.lexer_ctx.current_char} in {self.lexer_ctx.discard_context()}.')