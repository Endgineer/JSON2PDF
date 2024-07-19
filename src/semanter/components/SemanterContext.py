import logging
import os

from parser.Parser import Parser
from compiler.units.Item import Item
from compiler.units.Prop import Prop
import semanter.constants.propset as propset
from semanter.utilities.IdentifierUtils import IdentifierUtils

class SemanterContext:
  parser: Parser
  cache: dict[str, dict[str, Item] | None]
  registry: dict[str, Item.Kind]
  current_item_valid: bool

  def __init__(self, parser: Parser):
    self.parser = parser
    self.cache = dict()
    self.registry = dict()
    self.current_item_valid = True



  def analyze_item(self, item: Item) -> Item:
    if item is None: return None

    self.current_item_valid = True

    analyzable_props = self.analyze_prop_keys(item)
    analyzable_props = self.analyze_prop_vals(analyzable_props)
    labels = self.analyze_prop_labels(analyzable_props)

    if self.analyze_item_registration(item, labels):
      return item



  def error(self, message: str) -> None:
    logging.getLogger('SEMANTIC').error(message)
    self.current_item_valid = False



  def analyze_prop_keys(self, item: Item) -> list[Prop]:
    props_with_valid_keys = list()

    key_registry = dict()
    for property in item.properties:
      if property.key is None:
        continue

      if property.key.get_string() in propset.ALL:
        props_with_valid_keys.append(property)
      else:
        self.error(f'Invalid prop key {property.key}.')

      if property.key.get_string() in key_registry:
        self.error(f'Duplicate prop key {property.key}, previously found {key_registry[property.key.get_string()]} other(s).')
        key_registry[property.key.get_string()] += 1
      else:
        key_registry[property.key.get_string()] = 1
    
    item_kind_probabilities = propset.prop_similarity_coefficients(set(key_registry))
    for item_kind, probability in item_kind_probabilities.items():
      if probability == 1.0:
        item.kind = item_kind
        break
    
    if item.kind is None:
      self.error(f'Item {item} has an undeterminable type due to an invalid combination of props {sorted(key_registry)}.')
    
    return props_with_valid_keys
  


  def analyze_prop_vals(self, props_with_valid_keys: list[Prop]) -> list[Prop]:
    props_with_valid_keys_vals = list()

    for prop in props_with_valid_keys:
      if prop.key.get_string() in propset.STRS:
        if prop.kind == str:
          props_with_valid_keys_vals.append(prop)
        else:
          self.error(f'Prop key {prop.key} expected a value of type {str} instead of {prop.kind}.')
      elif prop.key.get_string() in propset.LISTS:
        if prop.kind == list:
          props_with_valid_keys_vals.append(prop)
        else:
          self.error(f'Prop key {prop.key} expected a value of type {list} instead of {prop.kind}.')
      elif prop.key.get_string() in propset.DICTS:
        if prop.kind == dict:
          props_with_valid_keys_vals.append(prop)
        else:
          self.error(f'Prop key {prop.key} expected a value of type {dict} instead of {prop.kind}.')
    
    return props_with_valid_keys_vals
  


  def analyze_prop_labels(self, props_with_valid_keys_vals: list[Prop]) -> dict[str, str]:
    label_registry = dict()
    label_index = dict()
    
    for prop in props_with_valid_keys_vals:
      if prop.key.get_string() == propset.LABELS:
        for pair in prop.value:
          pair_key = pair[0].get_string()
          if pair_key in label_registry:
            self.error(f'Duplicate label {pair[0]}, previously found {label_registry[pair_key]} other(s).')
            label_registry[pair_key] += 1
          else:
            label_registry[pair_key] = 1
            label_index[pair_key] = None if pair[1] is None else pair[1].get_string()
          
          pair_key_cycle = pair[0].contains_invocation()
          pair_val_cycle = False if pair[1] is None else pair[1].contains_invocation()

          if pair_key_cycle:
            self.error(f'Label key {pair[0]} cannot contain an invocation.')
          if pair_val_cycle:
            self.error(f'Label value {pair[0]} cannot contain an invocation.')
    
    return label_index



  def analyze_item_registration(self, item: Item, labels: dict[str, str]) -> bool:
    section_name = item.section.get_string()

    if section_name.strip() == '':
      self.error(f'Section namespace {item.section} cannot be nameless.')
    elif item.section.contains_invocation():
      self.error(f'Section namespace {item.section} cannot contain an invocation.')
    elif section_name in self.registry and self.registry[section_name] != item.kind:
      self.error(f'Type mismatch between item {item} and section namespace "{section_name}", which has previously accepted items of type {self.registry[section_name].name}.')
    elif self.current_item_valid:
      self.registry[section_name] = item.kind
      logging.getLogger('SEMANTIC').debug(f'Registered item {item} under section namespace "{section_name}".')
      item.labels = labels
      return True
    
    return False



  def query_cache(self, item: Item) -> Item:
    reference_string = item.reference.get_string()
    if reference_string.startswith('//'):
      logging.getLogger('SEMANTIC').debug(f'Item {item} is a comment; skipping semantic analysis.')
      return None

    reference_parts = self.sundered_reference(item, reference_string)
    if reference_parts is None: return None
    fileref, itemref = reference_parts

    cache_entry_dirty = fileref not in self.cache
    if cache_entry_dirty:
      logging.getLogger('SEMANTIC').debug(f'Cache miss for item {item}.')
      self.query_disk(fileref)
    
    properties = None
    regex_tokens = IdentifierUtils.tokenize_regex(itemref)
    for cached_itemref in self.cache[fileref].keys():
      if IdentifierUtils.match_itemref(cached_itemref, regex_tokens):
        logging.getLogger('SEMANTIC').debug(f'Cache hit "{fileref}::{cached_itemref}" matches item {item}.')
        properties = self.cache[fileref][cached_itemref].properties
        break
    
    if properties is None:
      return self.error(f'Item {item} does not exist in referenced file "{fileref}.json".')
    
    return Item(item.section, item.reference, item.line_number, item.char_number, properties)



  def sundered_reference(self, item: Item, reference_string: str) -> tuple[str, str]:
    reference_parts = reference_string.split('::')

    reference_errored = False
    if item.reference.contains_invocation():
      self.error(f'Item {item} cannot contain an invocation.')
      reference_errored = True
    if len(reference_parts) != 2:
      self.error(f'Item {item} is not of the form "<FILE_BASENAME_PATH>::<ITEM_IDENTIFIER>".')
      reference_errored = True
    if reference_errored: return None
    
    fileref, itemref = reference_parts

    if fileref.strip() == '':
      self.error(f'File basename path "{fileref}" in item {item} cannot be empty.')
      reference_errored = True
    if itemref.strip() == '':
      self.error(f'Item identifier "{itemref}" in item {item} cannot be empty.')
      reference_errored = True
    if reference_errored: return None

    if not os.path.isfile(f'{fileref}.json'):
      self.error(f'File path "{fileref}.json" from item {item} does not point to an existing file.')
      reference_errored = True
    if not IdentifierUtils.validate(itemref):
      self.error(f'Item identifier "{itemref}" in item {item} is not a valid identifier.')
      reference_errored = True
    if reference_errored: return None
    
    return (fileref, itemref)



  def query_disk(self, fileref: str) -> None:
    file_items = self.parser.parse_all(f'{fileref}.json')
    self.cache[fileref] = dict()
    reference_registry = dict()

    for file_item in file_items:
      if file_item.reference.contains_invocation():
        self.error(f'The identifier of item {file_item} in file "{fileref}.json" cannot contain an invocation.')
        continue

      file_item_reference_string = file_item.reference.get_string()

      if file_item_reference_string.strip() == '':
        self.error(f'The identifier of item {file_item} in file "{fileref}.json" cannot be empty.')
        continue

      if not IdentifierUtils.validate(file_item_reference_string):
        self.error(f'The identifier of item {file_item} in file "{fileref}.json" is not a valid identifier.')
        continue

      if file_item_reference_string in reference_registry:
        self.error(f'Duplicate identifier of item {file_item} in file "{fileref}.json", previously found {reference_registry[file_item_reference_string]} other(s).')
        reference_registry[file_item_reference_string] += 1
        continue

      reference_registry[file_item_reference_string] = 1
      self.cache[fileref][file_item_reference_string] = file_item