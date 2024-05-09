from parser.components.ParserContext import ParserContext
from parser.routines.derivators import *
from lexer.Lexer import Lexer
from compiler.consts.typing import *

class Parser():
  parser_ctx: ParserContext

  def __init__(self, lexer: Lexer):
    self.parser_ctx = ParserContext(lexer)
  
  def parse_cv(self) -> SyntacticTypes.SectionsList:
    return derive_curriculumvitae(self.parser_ctx)

  def parse_rf(self, filepath) -> SyntacticTypes.ReferencedItemsList:
    self.parser_ctx.lexer.context_switch(filepath)
    return derive_references(self.parser_ctx)