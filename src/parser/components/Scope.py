from compiler.units.Token import Token
from parser.constants.grammar import *

class Scope:
  stack: list[Nonterminal]

  def __init__(self):
    self.stack = list()
  
  def __repr__(self):
    return f'Scope[{len(self.stack)}]: {self.stack[-1] if len(self.stack) > 0 else None}'
  
  def append(self, nonterminal: Nonterminal) -> None:
    if not nonterminal.phantasmal:
      self.stack.append(nonterminal)
  
  def pop(self) -> Nonterminal:
    return self.stack.pop()
  
  def correct(self, token_kind: Token.Kind) -> Nonterminal:
    if token_kind in self.stack[-1].first and token_kind in self.stack[-1].follow:
      return self.stack.pop()
  
  def synchronize(self, token_kind: Token.Kind) -> list[Nonterminal]:
    skipped_nonterminals = list()
    while True:
      if token_kind in self.stack[-1].first:
        return skipped_nonterminals
      elif token_kind in self.stack[-1].follow:
        skipped_nonterminals.append(self.stack.pop())
      elif len(skipped_nonterminals) > 0:
        return skipped_nonterminals
      else:
        return None