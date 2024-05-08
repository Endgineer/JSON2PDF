import enum

from lexer.components.Token import Token

class LexerContext:
  class State(enum.Enum):
    START = 0
    STR_AWAIT_CHAR = 1
    DISCARDED_STRING = 2
  
  document: str
  line_start_idx: int
  matched_token_start_idx: int
  matched_token_len: int
  line_number: int
  state: State
  matched_token_kind: Token.Kind
  matched_token: Token
  current_char: str

  def __init__(self, file_path: str):
    with open(file_path, 'r') as file:
      self.document = file.read()

    self.line_start_idx = 0
    self.matched_token_start_idx = 0
    self.matched_token_len = 0
    self.line_number = 1
    self.state = LexerContext.State.START
    self.matched_token_kind = None
    self.matched_token = None
    self.current_char = ''
  
  def scan_next_char(self) -> None:
    self.current_char = self.document[self.matched_token_start_idx + self.matched_token_len]
  
  def at_end_of_file(self) -> bool:
    return len(self.document) == self.matched_token_start_idx + self.matched_token_len
  
  def capture_token(self) -> None:
    self.matched_token = None if self.matched_token_kind is None else Token(
      self.document[self.matched_token_start_idx : self.matched_token_start_idx + self.matched_token_len] if self.matched_token_kind == Token.Kind.STRING else None,
      self.matched_token_kind,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.state = LexerContext.State.START
  
  def discard_context(self) -> Token:
    while self.state == LexerContext.State.DISCARDED_STRING and self.current_char != '"':
      self.matched_token_len += 1
      self.scan_next_char()
    
    token = Token(
      self.document[self.matched_token_start_idx : self.matched_token_start_idx + self.matched_token_len],
      Token.Kind.DISCARDED,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.state = LexerContext.State.START

    return token