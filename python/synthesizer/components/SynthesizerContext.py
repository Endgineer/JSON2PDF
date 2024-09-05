import logging

from semanter.Semanter import Semanter
from compiler.units.Item import Item
from compiler.units.Token import Token
from synthesizer.routines.generators import *
from compiler.components.Flags import Flags

class SynthesizerContext:
  semanter: Semanter
  items: list[Item]
  tree: dict[str, list[dict[str, str | list[str] | dict[str, str]]]]
  flags: Flags

  def __init__(self, semanter: Semanter, flags: Flags):
    self.semanter = semanter
    self.items = None
    self.tree = None
    self.flags = flags
  
  def __repr__(self):
    return generate_from_tree(self)
  


  def build(self) -> None:
    self.items = list()
    
    while True:
      item = self.semanter.analyze()
      if item is None: return
      self.items.append(item)
  


  def invocations(self, anonymize: bool, bolded: bool) -> None:
    for item in self.items:
      invoked_labels = set()
      
      for prop in item.properties:
        if prop.kind == str:
          invoked_labels.update(SynthesizerContext.activate_token(item.labels, prop.value, anonymize, bolded))
        elif prop.kind == list:
          for point in prop.value:
            invoked_labels.update(SynthesizerContext.activate_token(item.labels, point, anonymize, bolded))
        elif prop.kind == dict:
          for pair in prop.value:
            invoked_labels.update(SynthesizerContext.activate_token(item.labels, pair[1], anonymize, bolded))
      
      redundant_labels = set(item.labels) - invoked_labels
      if len(redundant_labels) > 0:
        logging.getLogger('SYNTHESIS').warning(f'Unused labels {sorted(redundant_labels)} in item {item}.')



  def dictify(self) -> None:
    self.tree = dict()

    for item in self.items:
      section = None if item.kind == Item.Kind.CLLETTER else item.section.get_string()

      if section not in self.tree:
        self.tree[section] = list()
      
      self.tree[section].append(dict())

      for prop in item.properties:
        prop_key = prop.key.get_string()
        if prop.kind == str:
          self.tree[section][-1][prop_key] = None if prop.value is None else prop.value.get_string()
        elif prop.kind == list:
          self.tree[section][-1][prop_key] = list()
          for point in prop.value:
            self.tree[section][-1][prop_key].append(None if point is None else point.get_string())
        elif prop.kind == dict:
          self.tree[section][-1][prop_key] = dict()
          for pair in prop.value:
            self.tree[section][-1][prop_key][pair[0].get_string()] = None if pair[1] is None else pair[1].get_string()

      logging.getLogger('SYNTHESIS').debug(f'Dictified item {item}: {self.tree[section][-1]}.')
      
      if item.kind == Item.Kind.CLLETTER:
        self.flags.init_letter(
          self.tree[section][-1][COMPANY] if COMPANY in self.tree[section][-1] else "",
          self.tree[section][-1][POSITION] if POSITION in self.tree[section][-1] else "",
          self.tree[section][-1][REFERENCE] if REFERENCE in self.tree[section][-1] else "",
          self.tree[section][-1][OPENING] if OPENING in self.tree[section][-1] else "",
          self.tree[section][-1][CLOSING] if CLOSING in self.tree[section][-1] else "",
          ", ".join(self.tree[section][-1][ATTACHMENTS]) if ATTACHMENTS in self.tree[section][-1] else None
        )



  def activate_token(labels: dict[str, str], token: Token, anonymize: bool, bolded: bool) -> set[str]:
    if token is None: return set()
    invoked_labels = set()

    token_string = f'{token}'
    for segment in token.value:
      invocation_result = segment.activate(labels, anonymize, bolded)

      if invocation_result is None:
        pass
      elif invocation_result == False:
        logging.getLogger('SYNTHESIS').warning(f'Missing label for invocation "{segment.invocation}" in {token_string}{", will obfuscate instead" if anonymize else ""}.')
      else:
        logging.getLogger('SYNTHESIS').debug(f'Bound invocation "{segment.invocation}" in {token_string} to its label.')
        invoked_labels.add(segment.invocation)
    
    return invoked_labels