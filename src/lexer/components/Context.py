import enum
import io

from lexer.components.Token import Token

class Context:
  class State(enum.Enum):
    START = 0
    NULL_AWAIT_U = 1
    NULL_AWAIT_L1 = 2
    NULL_AWAIT_L2 = 3
    STR_AWAIT_CHAR = 4
  
  file: io.TextIOWrapper
  token_start_idx: int
  token_len: int
  line_number: int
  token_kind: Token.Kind
  state: State
  line: str
  head: str

  def __init__(self, file_path: str):
    self.file = open(file_path, 'r')

    self.token_start_idx = 0
    self.token_len = 0
    self.line_number = 0
    self.token_kind = None
    self.state = Context.State.START
    self.line = ''
    self.head = ''
  
  def clean(self) -> None:
    '''Closes the file attached to the context.'''
    self.file.close()
  
  def fetch(self) -> None:
    '''Fetches the next line into the context.'''
    self.line = self.file.readline()
    self.token_start_idx = 0
    self.token_len = 0
    self.line_number += 1
    self.token_kind = None
  
  def step(self) -> None:
    '''Moves the scanner head one step forward.'''
    self.head = self.line[self.token_start_idx + self.token_len]
  
  def accept(self) -> Token:
    '''Accepts the token currently captured by the context and resets the context.'''
    token = Token(
      self.line[self.token_start_idx : self.token_start_idx + self.token_len] if self.token_kind == Token.Kind.STRING else None,
      self.token_kind,
      self.line_number,
      self.token_start_idx
    )

    self.token_start_idx += self.token_len
    self.token_len = 0
    self.token_kind = None
    self.state = Context.State.START

    return token
  
  def reject(self) -> Token:
    '''Rejects the line currently captured by the context and resets the context.'''
    token = Token(
      self.line[self.token_start_idx : len(self.line)],
      Token.Kind.DISCARDED,
      self.line_number,
      self.token_start_idx
    )

    self.token_start_idx = len(self.line)
    self.token_len = 0
    self.token_kind = None
    self.state = Context.State.START

    return token