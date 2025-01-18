import enum
import logging
from collections import deque

from compiler.logger.PhaseLogger import *
from compiler.units.Token import Token
from compiler.units.Segment import Segment

class LexerContext:
  class State(enum.Enum):
    DISCARDED_STRING = -1
    START = 0
    STR_AWAIT_CHAR = 1
    STR_AWAIT_INVOCATION_SYLLABLE = 2
    STR_AWAIT_INVOCATION_DELIMITER = 3
    STR_POSSIBLE_BOLD_BEGIN = 4
    STR_AWAIT_BOLD_CHAR = 5
    STR_POSSIBLE_BOLD_END = 6
    STR_POSSIBLE_BOLD_IN_INVOKATION = 7
    STR_POSSIBLE_DIRECTIVE = 8
    STR_DIRECTIVE_CHAR = 9
  
  logger: PhaseLogger
  filepath: str
  document: str
  line_start_idx: int
  matched_token_start_idx: int
  matched_token_len: int
  line_number: int
  state: State
  matched_token_kind: Token.Kind
  matched_token_value: list[Segment]
  matched_token: Token
  current_char: str
  errors: deque[str]

  def __init__(self, filepath: str, logger: PhaseLogger):
    self.switch(filepath, logger)
  
  def switch(self, filepath: str, logger: PhaseLogger) -> None:
    self.logger = logger
    self.logger.log(None, Phase.LEXICAL, logging.DEBUG, f'Switched context to "{filepath}"...')

    with open(filepath, 'r') as file:
      self.document = file.read()

    self.filepath = filepath
    self.line_start_idx = 0
    self.matched_token_start_idx = 0
    self.matched_token_len = 0
    self.line_number = 1
    self.state = LexerContext.State.START
    self.matched_token_kind = None
    self.matched_token_value = list()
    self.matched_token = None
    self.current_char = ''
    self.errors = deque()
  
  def restore(self) -> None:
    self.logger.log(None, Phase.LEXICAL, logging.DEBUG, f'Restored context of "{self.filepath}"...')
  
  def scan_next_char(self) -> None:
    self.current_char = self.document[self.matched_token_start_idx + self.matched_token_len]
  
  def at_end_of_file(self) -> bool:
    return len(self.document) == self.matched_token_start_idx + self.matched_token_len
  
  def create_new_segment(self, backtrack_end: int = 0) -> None:
    self.matched_token_value.append(Segment(self.matched_token_len - backtrack_end))
  
  def get_segment_value(self) -> str:
    return self.document[self.matched_token_start_idx + self.matched_token_value[-1].relative_position : self.matched_token_start_idx + self.matched_token_len]
  
  def finalize_segment_plain(self, backtrack_end: int = 0) -> None:
    self.matched_token_value[-1].define_as_plain(self.document[self.matched_token_start_idx + self.matched_token_value[-1].relative_position : self.matched_token_start_idx + self.matched_token_len - backtrack_end])
  
  def finalize_segment_invokable(self, backtrack_end: int = 0) -> None:
    self.matched_token_value[-1].define_as_invokable(self.document[self.matched_token_start_idx + self.matched_token_value[-1].relative_position : self.matched_token_start_idx + self.matched_token_len - backtrack_end])
  
  def finalize_segment_bold(self, backtrack_end: int = 0) -> None:
    self.matched_token_value[-1].define_as_bold(self.document[self.matched_token_start_idx + self.matched_token_value[-1].relative_position : self.matched_token_start_idx + self.matched_token_len - backtrack_end])
  
  def capture_token(self) -> Token:
    token = self.matched_token
    if token is not None:
      self.logger.log(None, Phase.LEXICAL, logging.DEBUG, f'Scanned {token}.')
    
    while len(self.errors) > 0:
      self.logger.log(None, Phase.LEXICAL, logging.ERROR, self.errors.popleft())
    
    self.matched_token = None if self.matched_token_kind is None else Token(
      self.matched_token_value if self.matched_token_kind == Token.Kind.STRING else None,
      self.matched_token_kind,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.matched_token_value = list()
    self.state = LexerContext.State.START

    return token
  
  def discard_context(self) -> None:
    responsible_char = None if self.at_end_of_file() and self.state != LexerContext.State.START else self.current_char

    if self.state == LexerContext.State.DISCARDED_STRING or responsible_char is None:
      while self.current_char != '\n' and not self.at_end_of_file():
        self.scan_next_char()
        self.matched_token_len += 1
        if self.current_char == '"': break
      string = self.document[self.matched_token_start_idx : self.matched_token_start_idx + self.matched_token_len + (-1 if self.current_char == '\n' else 0)]+('' if self.current_char == '"' else '"')
    else:
      string = None

    token = Token(
      string,
      Token.Kind.DISCARDED,
      self.line_number,
      self.matched_token_start_idx - self.line_start_idx
    )

    if responsible_char is not None and responsible_char != '\n':
      self.errors.append(f'Unexpected symbol {repr(responsible_char)} in {token}.')
    if responsible_char is None or (self.at_end_of_file() and self.state == LexerContext.State.DISCARDED_STRING and self.current_char != '"'):
      self.errors.append(f'Unexpected EOF before the end of {token}')
    if responsible_char == '\n' or (self.state == LexerContext.State.DISCARDED_STRING and self.current_char == '\n'):
      self.errors.append(f'Unexpected NEWLINE before the end of {token}')

    self.matched_token_start_idx += self.matched_token_len
    self.matched_token_len = 0
    self.matched_token_kind = None
    self.matched_token_value = list()
    self.state = LexerContext.State.START

    if self.current_char == '\n':
      self.line_start_idx = self.matched_token_start_idx
      self.line_number += 1