from compiler.logger.PhaseLogger import PhaseLogger
from compiler.units.Token import Token
from lexer.components.LexerContext import LexerContext
from lexer.routines.matchers import *

class Lexer():
  lexer_ctx_stack: list[LexerContext]

  def __init__(self, filepath: str, logger: PhaseLogger):
    self.lexer_ctx_stack = [LexerContext(filepath, logger)]
    if not self.lexer_ctx_stack[-1].at_end_of_file(): self.scan()
  
  def scan(self) -> Token:
    while len(self.lexer_ctx_stack) > 0:
      while self.lexer_ctx_stack[-1].at_end_of_file():
        if self.lexer_ctx_stack[-1].state != LexerContext.State.START:
          self.lexer_ctx_stack[-1].discard_context()
        else:
          token = self.lexer_ctx_stack[-1].capture_token()
          if token is None:
            self.lexer_ctx_stack.pop()
            if len(self.lexer_ctx_stack) > 0:
              self.lexer_ctx_stack[-1].restore()
          return token
      
      self.lexer_ctx_stack[-1].scan_next_char()

      if match_str_char(self.lexer_ctx_stack[-1]): pass
      elif match_possible_bold_begin(self.lexer_ctx_stack[-1]): pass
      elif match_bold_char(self.lexer_ctx_stack[-1]): pass
      elif match_possible_bold_end(self.lexer_ctx_stack[-1]): pass
      elif match_invocation_syllable(self.lexer_ctx_stack[-1]): pass
      elif match_invocation_delimiter(self.lexer_ctx_stack[-1]): pass
      elif match_possible_bold_in_invokation(self.lexer_ctx_stack[-1]): pass
      elif match_start(self.lexer_ctx_stack[-1]): pass
      elif match_possible_directive(self.lexer_ctx_stack[-1]): pass
      elif match_directive_char(self.lexer_ctx_stack[-1]): pass
      
      if self.lexer_ctx_stack[-1].matched_token_kind is None:
        pass
      elif self.lexer_ctx_stack[-1].matched_token_kind == Token.Kind.DISCARDED:
        self.lexer_ctx_stack[-1].discard_context()
      else:
        return self.lexer_ctx_stack[-1].capture_token()
  
  def peek(self) -> Token.Kind:
    return None if len(self.lexer_ctx_stack) == 0 or self.lexer_ctx_stack[-1].matched_token is None else self.lexer_ctx_stack[-1].matched_token.kind

  def context_switch(self, filepath: str) -> None:
    self.lexer_ctx_stack.append(LexerContext(filepath, self.lexer_ctx_stack[-1].logger))
    if not self.lexer_ctx_stack[-1].at_end_of_file(): self.scan()
  
  def get_context_name(self) -> str:
    return f'"{self.lexer_ctx_stack[-1].filepath}"' if len(self.lexer_ctx_stack) > 0 else None