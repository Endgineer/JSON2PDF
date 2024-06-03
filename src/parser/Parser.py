from parser.components.ParserContext import ParserContext
from parser.constants.grammar import *
from lexer.Lexer import Lexer
from compiler.units.Item import Item

class Parser():
  parser_ctx: ParserContext

  def __init__(self, lexer: Lexer):
    self.parser_ctx = ParserContext(lexer)
  
  def parse(self) -> Item:
    self.parser_ctx.captured_item = None
    
    while len(self.parser_ctx.stack) > 0:
      symbol = self.parser_ctx.stack.popleft()

      self.parser_ctx.update_context_memory(symbol)

      if self.parser_ctx.complete_context_item(symbol):
        break
    
    return self.parser_ctx.captured_item

  # def parse_ref_file(self, filepath: str) -> list[Item]:
  #   self.parser_ctx.stack.append()
  #   self.parser_ctx.lexer.context_switch(filepath)
  #   return derive_references(self.parser_ctx)