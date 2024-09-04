from compiler.units.Item import Item
from semanter.components.SemanterContext import SemanterContext
from parser.Parser import Parser
from compiler.components.Flags import Flags

class Semanter:
  semanter_ctx: SemanterContext

  def __init__(self, parser: Parser, flags: Flags):
    self.semanter_ctx = SemanterContext(parser, flags)
  
  def analyze(self) -> Item:
    while True:
      item = self.semanter_ctx.parser.parse()

      if item is None:
        return None
      elif item.reference is not None:
        item = self.semanter_ctx.query_cache(item)

      item = self.semanter_ctx.analyze_item(item)

      if item is not None:
        return item