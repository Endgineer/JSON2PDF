from parser.components.ParserContext import ParserContext
from parser.constants.grammar import *
from lexer.Lexer import Lexer
from compiler.units.Item import Item

class Parser():
  primary_parser_ctx: ParserContext

  def __init__(self, lexer: Lexer):
    self.primary_parser_ctx = ParserContext(lexer)
  
  def parse(self) -> Item:
    self.primary_parser_ctx.captured_item = None
    
    while len(self.primary_parser_ctx.stack) > 0:
      symbol = self.primary_parser_ctx.stack.popleft()

      self.primary_parser_ctx.update_context_memory(symbol)

      if self.primary_parser_ctx.complete_context_item(symbol):
        break
    
    return self.primary_parser_ctx.captured_item