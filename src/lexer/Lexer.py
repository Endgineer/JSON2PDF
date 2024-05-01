import logging

from lexer.components.Token import Token
from lexer.components.Context import Context
from lexer.routines.matchers import *

class Lexer():
  context: Context

  def __init__(self, file_path: str):
    self.context = Context(file_path)
  
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.context.clean()

  def next(self) -> Token:
    '''Scans the next token in the stream. Returns None if at EOF.'''
    while True:
      if len(self.context.line) == self.context.token_start_idx + self.context.token_len:
        if self.context.state != Context.State.START:
          self.__reject()
        
        self.context.fetch()
      
      if not self.context.line:
        return None
      
      self.context.step()

      if match_str_char(self.context): pass
      elif match_start(self.context): pass
      elif match_null_u(self.context): pass
      elif match_null_l1(self.context): pass
      elif match_null_l2(self.context): pass
      
      if self.context.token_kind is None:
        pass
      elif self.context.token_kind == Token.Kind.DISCARDED:
        self.__reject()
      else:
        return self.__accept()
  
  def __accept(self) -> Token:
    token = self.context.accept()
    logging.getLogger('LEXICAL').debug(f'Scanned {token}.')
    return token
  
  def __reject(self) -> None:
    token = self.context.reject()
    logging.getLogger('LEXICAL').error(f'Unexpected symbol {self.context.head} in {token}.')