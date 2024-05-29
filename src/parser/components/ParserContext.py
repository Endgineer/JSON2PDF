import logging
from collections import deque

from lexer.Lexer import Lexer
from compiler.units.Token import Token
from compiler.consts.typing import SyntacticTypes
from parser.constants.grammar import *
from compiler.units.Item import Item
from parser.components.Scope import Scope

class ParserContext:
  lexer: Lexer
  main_stack: deque[Token.Kind | Nonterminal | None]
  scope: Scope
  captured_item: Item
  memorized_prop: SyntacticTypes.ItemProperty
  memorized_propval_type: list | dict
  memorized_section: str

  def __init__(self, lexer: Lexer):
    self.lexer = lexer
    self.main_stack = deque([ ROOT ])
    self.scope = Scope()
    self.captured_item = None
    self.memorized_prop = None
    self.memorized_propval_type = None
    self.memorized_section = None
  
  def update_context_memory(self, symbol: Token.Kind | Nonterminal | None) -> None:
    if symbol is SECTION and self.lexer.peek() in symbol.first:
        self.memorized_section = self.lexer.lexer_ctx_stack[-1].matched_token.value
    elif symbol is ITEM and self.lexer.peek() in symbol.first:
      self.captured_item = Item(
        self.memorized_section,
        self.lexer.lexer_ctx_stack[-1].matched_token.value if self.lexer.peek() == Token.Kind.STRING else None,
        self.lexer.lexer_ctx_stack[-1].matched_token.line_number,
        self.lexer.lexer_ctx_stack[-1].matched_token.char_number,
        None if self.lexer.peek() == Token.Kind.STRING else list()
      )
    elif symbol is PROP and self.lexer.peek() in symbol.first:
      self.memorized_prop = [None, None]
    elif symbol is STRINGLIST and self.lexer.peek() in symbol.first:
      self.memorized_prop[1] = list()
      self.memorized_propval_type = list
    elif symbol is STRINGDICT and self.lexer.peek() in symbol.first:
      self.memorized_prop[1] = list()
      self.memorized_propval_type = dict
  
  def complete_context_item(self, symbol: Token.Kind | Nonterminal | None) -> bool:
    if isinstance(symbol, Nonterminal):
      self.scope.append(symbol)
      expansion = symbol.expand(self.lexer.peek())
      if type(expansion) == list:
        logging.getLogger('SYNTAX').debug(f'Used production {symbol} -> {" ".join([s.name.lower() if type(s) == Token.Kind else str(s) for s in expansion][::-1]) if len(expansion) > 0 else "ε"}.')
        self.main_stack.extendleft(expansion)
      else:
        logging.getLogger('SYNTAX').error(f'Found {self.lexer.scan()}, expected one of {{{", ".join([s.name for s in symbol.first.keys()])}}}.')
        self.panic()
    
    elif isinstance(symbol, Token.Kind) or symbol is None:
      token = self.lexer.scan()
      
      if token is None and token == symbol:
        return self.log_return(True)
      elif token is not None and token.kind == symbol:
        self.scope.try_enter_scope(token.kind)

        if self.captured_item is not None and token.kind == Token.Kind.STRING:
          if self.captured_item.reference is not None:
            pass
          elif self.memorized_prop[0] is None:
            self.memorized_prop[0] = token
          elif self.memorized_prop[1] is None:
            self.memorized_prop[1] = token
          elif self.memorized_propval_type == list:
            self.memorized_prop[1].append(token)
          elif self.memorized_propval_type == dict:
            if len(self.memorized_prop[1]) == 0 or self.memorized_prop[1][-1][1] is not None:
              self.memorized_prop[1].append([token, None])
            else:
              self.memorized_prop[1][-1][1] = token
        
        nonterminal = self.scope.try_exit_scope(self.lexer.peek())
        if nonterminal is ITEM:
          return self.log_return(True)
        elif nonterminal is PROP:
          self.captured_item.properties.append(self.memorized_prop)
      else:
        logging.getLogger('SYNTAX').error(f'Found {token}, expected {symbol if symbol is None else symbol.name}.')
        self.panic()
    
    return self.log_return(False)
  
  def panic(self) -> None:
    while True:
      token = self.lexer.scan()
      if token is None: return
      self.scope.try_enter_scope(token.kind)
      logging.getLogger('SYNTAX').warning(f'Skipping {token} due to previous error.')
      if self.scope.try_exit_scope(self.lexer.peek()) is not None: return
  
  def log_return(self, status: bool) -> bool:
    logging.getLogger('SYNTAX').debug(f'{self.scope} | Stack: [{", ".join([s.name.lower() if type(s) == Token.Kind else str(s) for s in self.main_stack])}]')
    if status and self.captured_item is not None: logging.getLogger('SYNTAX').debug(f'Captured item {self.captured_item}.')
    return status