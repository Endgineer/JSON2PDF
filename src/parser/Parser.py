from parser.components.ParserContext import ParserContext
from parser.constants.grammar import *
from lexer.Lexer import Lexer
from compiler.units.Item import Item

class Parser():
  primary_parser_ctx: ParserContext
  auxiliary_parser_ctx: ParserContext

  def __init__(self, lexer: Lexer):
    self.primary_parser_ctx = ParserContext(lexer)
    self.auxiliary_parser_ctx = None
  
  def parse(self) -> Item:
    self.primary_parser_ctx.captured_item = None
    
    while len(self.primary_parser_ctx.stack) > 0:
      symbol = self.primary_parser_ctx.stack.popleft()

      self.primary_parser_ctx.update_context_memory(symbol)

      if self.primary_parser_ctx.complete_context_item(symbol):
        break
    
    return self.primary_parser_ctx.captured_item

  def parse_all(self, filepath: str) -> list[Item]:
    self.auxiliary_parser_ctx = ParserContext(self.primary_parser_ctx.lexer, REFF)
    self.auxiliary_parser_ctx.lexer.context_switch(filepath)
    
    items = list()
    while True:
      self.auxiliary_parser_ctx.captured_item = None
    
      while len(self.auxiliary_parser_ctx.stack) > 0:
        symbol = self.auxiliary_parser_ctx.stack.popleft()

        self.auxiliary_parser_ctx.update_context_memory(symbol)

        if self.auxiliary_parser_ctx.complete_context_item(symbol):
          break
      
      if self.auxiliary_parser_ctx.captured_item == None:
        self.auxiliary_parser_ctx.lexer.scan()
        self.auxiliary_parser_ctx = None
        return items
      
      items.append(self.auxiliary_parser_ctx.captured_item)
      items[-1].reference = items[-1].section
      items[-1].section = None