import logging

from parser.components.ParserContext import ParserContext
from parser.routines.derivators import *
from lexer.Lexer import Lexer

class Parser():
  parser_ctx: ParserContext

  def __init__(self, lexer: Lexer):
    self.parser_ctx = ParserContext(lexer)
  
  def parse_cv(self) -> list[tuple[str, list[str | list[tuple[str, str | list[str] | list[tuple[str, str]]]]]]]:
    return derive_curriculumvitae(self.parser_ctx)

  def parse_rf(self, filepath) -> list[tuple[str, list[tuple[str, str | list[str] | list[tuple[str, str]]]]]]:
    self.parser_ctx.lexer.context_switch(filepath)
    return derive_references(self.parser_ctx)