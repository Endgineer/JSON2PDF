import enum
import logging

from compiler.units.Token import Token

class LexerContext:
  class State(enum.Enum):
    START = 0
    STR_AWAIT_CHAR = 1
    DISCARDED_STRING = 2
  
  filepath: str
  document: str
  line_start_idx: int
  matched_token_start_idx: int
  matched_token_len: int
  line_number: int
  state: State
  matched_token_kind: Token.Kind
  matched_token: Token
  current_char: str

  def __init__(self, filepath: str):
    self.switch(filepath)
  
  def switch(self, filepath: str) -> None:
    logging.getLogger('LEXICAL').debug(f'Switched context to "{filepath}"...')

    with open(filepath, 'r') as file:
      self.document = file.read()

    self.filepath = filepath
    self.line_start_idx = 0
    self.matched_token_start_idx = 0
    self.matched_token_len = 0
    self.line_number = 1
    self.state = LexerContext.State.START
    self.matched_token_kind = None
    self.matched_token = None
    self.current_char = ''
  
  def restore(self) -> None:
    logging.getLogger('LEXICAL').debug(f'Restored context of "{self.filepath}"...')
  
  def scan_next_char(self) -> None:
    self.current_char = self.document[self.matched_token_start_idx + self.matched_token_len]
  
  def at_end_of_file(self) -> bool:
    return len(self.document) == self.matched_token_start_idx + self.matched_token_len
  
  def capture_token(self) -> Token:
    token = self.matched_token
    if token is not None:
      logging.getLogger('LEXICAL').debug(f'Scanned {token}.')
    
    self.matched_token = None if self.matched_token_kind is None else Token(
      self.document[self.matched_token_start_idx + 1 : self.matched_token_start_idx + self.matched_token_len - 1] if self.matched_token_kind == Token.Kind.STRING else None,
      self.matched_token_kind,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.state = LexerContext.State.START

    return token
  
  def discard_context(self) -> None:
    while self.state == LexerContext.State.DISCARDED_STRING and self.current_char != '"' and self.current_char != '\n' and not self.at_end_of_file():
      self.matched_token_len += 1
      self.scan_next_char()
    
    token = Token(
      self.document[self.matched_token_start_idx : self.matched_token_start_idx + self.matched_token_len],
      Token.Kind.DISCARDED,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    logging.getLogger('LEXICAL').error(f'Unexpected symbol {self.current_char} in {token}.')

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.state = LexerContext.State.START