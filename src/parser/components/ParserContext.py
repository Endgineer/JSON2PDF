import logging
from collections import deque

from lexer.Lexer import Lexer
from compiler.units.Token import Token
from compiler.units.Prop import Prop
from parser.constants.grammar import *
from compiler.units.Item import Item
from parser.components.Scope import Scope

class ParserContext:
  lexer: Lexer
  stack: deque[Token.Kind | Nonterminal | None]
  scope: Scope
  captured_item: Item
  memorized_prop: Prop
  memorized_section: Token

  def __init__(self, lexer: Lexer, root: Nonterminal):
    self.lexer = lexer
    self.stack = deque([ root ])
    self.scope = Scope()
    self.captured_item = None
    self.memorized_prop = None
    self.memorized_section = None
  
  def update_context_memory(self, symbol: Token.Kind | Nonterminal | None) -> None:
    if symbol is REF:
      self.memorized_section = self.lexer.lexer_ctx_stack[-1].matched_token
    elif symbol is REF2:
      self.captured_item = Item(
        self.memorized_section,
        None,
        self.memorized_section.line_number,
        self.memorized_section.char_number,
        list()
      )
    elif symbol is SECTION:
      self.memorized_section = self.lexer.lexer_ctx_stack[-1].matched_token
    elif symbol is ITEM:
      self.captured_item = Item(
        self.memorized_section,
        self.lexer.lexer_ctx_stack[-1].matched_token if self.lexer.peek() == Token.Kind.STRING else None,
        self.lexer.lexer_ctx_stack[-1].matched_token.line_number,
        self.lexer.lexer_ctx_stack[-1].matched_token.char_number,
        None if self.lexer.peek() == Token.Kind.STRING else list()
      )
    elif symbol is LETTER:
      self.captured_item = Item(
        None,
        None,
        self.lexer.lexer_ctx_stack[-1].matched_token.line_number,
        self.lexer.lexer_ctx_stack[-1].matched_token.char_number,
        list()
      )
    elif symbol is PROP:
      self.memorized_prop = Prop()
      self.memorized_prop.kind = str
    elif symbol is STRINGLIST:
      self.memorized_prop.value = list()
      self.memorized_prop.kind = list
    elif symbol is STRINGDICT:
      self.memorized_prop.value = list()
      self.memorized_prop.kind = dict
  
  def complete_context_item(self, symbol: Token.Kind | Nonterminal | None) -> bool:
    if isinstance(symbol, Nonterminal):
      self.scope.append(symbol)
      expansion = symbol.expand(self.lexer.peek())
      if type(expansion) == list:
        logging.getLogger('SYNTAX').debug(f'Used production {symbol} -> {" ".join([s.name.lower() if type(s) == Token.Kind else str(s) for s in expansion][::-1]) if len(expansion) > 0 else "ε"}.')
        self.stack.extendleft(expansion)
        if len(self.stack) == 0: self.scope.pop()
        else:
          upcoming_token_is_expected = any([
            self.lexer.peek() == self.stack[0],
            isinstance(self.stack[0], Nonterminal) and (self.lexer.peek() in self.stack[0].first or self.stack[0].nullable and self.lexer.peek() in self.stack[0].follow)
          ])
          synchronizations = self.scope.synchronize(self.lexer.peek()) if upcoming_token_is_expected else None
          if synchronizations is not None and len(synchronizations) > 0:
            logging.getLogger('SYNTAX').debug(f'Synchronized scope based on an upcoming {None if self.lexer.peek() is None else self.lexer.peek().name} token, popping {synchronizations}.')
      else:
        logging.getLogger('SYNTAX').error(f'Encountered {self.lexer.lexer_ctx_stack[-1].matched_token}, expected one of {sorted([str(s) if s is None else s.name for s in symbol.first.keys()])}.')
        self.panic()
    
    elif isinstance(symbol, Token.Kind) or symbol is None:
      corrected_nonterminal = self.scope.correct(self.lexer.peek())
      if corrected_nonterminal is not None:
        logging.getLogger('SYNTAX').debug(f'Corrected scope based on {corrected_nonterminal} being fulfilled.')
      
      if self.lexer.peek() is None and symbol is None:
        self.lexer.scan()
        return self.log_return(True)
      elif self.lexer.peek() == symbol:
        token = self.lexer.scan()
        if self.captured_item is not None and token.kind == Token.Kind.STRING:
          if self.captured_item.reference is not None: pass
          else: self.memorized_prop.fill(token)
        
        upcoming_token_is_expected = any([
          self.lexer.peek() == self.stack[0],
          isinstance(self.stack[0], Nonterminal) and (self.lexer.peek() in self.stack[0].first or self.stack[0].nullable and self.lexer.peek() in self.stack[0].follow)
        ])
        synchronizations = self.scope.synchronize(self.lexer.peek()) if upcoming_token_is_expected else None
        if synchronizations is not None:
          if len(synchronizations) > 0:
            logging.getLogger('SYNTAX').debug(f'Synchronized scope based on an upcoming {None if self.lexer.peek() is None else self.lexer.peek().name} token, popping {synchronizations}.')
          
          if PROP in synchronizations:
            self.captured_item.properties.append(self.memorized_prop)
          
          if ITEM in synchronizations:
            return self.log_return(True)
          elif REF2 in synchronizations:
            return self.log_return(True)
          elif LETTER2 in synchronizations:
            return self.log_return(True)
      else:
        logging.getLogger('SYNTAX').error(f'Encountered {self.lexer.lexer_ctx_stack[-1].matched_token}, expected {symbol if symbol is None else symbol.name}.')
        self.panic()
    
    return self.log_return(False)
  
  def panic(self) -> None:
    while True:
      synchronizations = self.scope.synchronize(self.lexer.peek())
      if synchronizations is not None:
        logging.getLogger('SYNTAX').warning(f'Synchronized to {self.lexer.lexer_ctx_stack[-1].matched_token} in an attempt to recover from previous error, popping {synchronizations}.')
        if STRINGPT in synchronizations or STRINGPAIR in synchronizations:
          self.memorized_prop.fill(None)
        elif PROP in synchronizations:
          self.captured_item.properties.append(self.memorized_prop)
        return
      token = self.lexer.scan()
      if token is None: return
      logging.getLogger('SYNTAX').warning(f'Skipping {token} in an attempt to synchronize.')
  
  def log_return(self, status: bool) -> bool:
    logging.getLogger('SYNTAX').debug(f'Context: {self.lexer.get_context_name()} | {self.scope} | Stack: [{", ".join([s.name.lower() if type(s) == Token.Kind else str(s) for s in self.stack])}]')
    if status and self.captured_item is not None: logging.getLogger('SYNTAX').debug(f'Captured item {self.captured_item}.')
    return status