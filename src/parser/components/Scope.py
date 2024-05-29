from compiler.units.Token import Token
from parser.constants.grammar import *

class Scope:
  enclosures: dict[Nonterminal, list[Token.Kind]]
  stack: list[Nonterminal]

  def __init__(self):
    self.enclosures = { ROOT: list(), SECTION: list(), ITEM: list(), PROP: list(), STRINGPT: list(), STRINGPAIR: list() }
    self.stack = list()
  
  def __repr__(self):
    return f'Scope[{len(self.stack)}]: {self.stack[-1] if len(self.stack) > 0 else None}'
  
  def append(self, nonterminal: Nonterminal) -> None:
    if nonterminal in self.enclosures:
      self.stack.append(nonterminal)
  
  def try_enter_scope(self, token_kind: Token.Kind) -> None:
    if token_kind == Token.Kind.LBRACE or token_kind == Token.Kind.LBRACKET:
      self.enclosures[self.stack[-1]].append(token_kind)
    elif token_kind == Token.Kind.RBRACE and self.enclosures[self.stack[-1]][-1] == Token.Kind.LBRACE:
      self.enclosures[self.stack[-1]].pop()
    elif token_kind == Token.Kind.RBRACKET and self.enclosures[self.stack[-1]][-1] == Token.Kind.LBRACKET:
      self.enclosures[self.stack[-1]].pop()

  def try_exit_scope(self, token_kind: Token.Kind) -> Nonterminal:
    if token_kind in self.stack[-1].follow and len(self.enclosures[self.stack[-1]]) == 0:
      return self.stack.pop()
    return None