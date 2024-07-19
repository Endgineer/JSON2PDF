import enum

class IdentifierUtils:
  class State(enum.Enum):
    ACCEPT_SYLLABLE = 0
    ACCEPT_DELIMITER = 1
    ACCEPT_NONWILDCARD = 2
  
  DELIMITERS = { '_', '-', '.', '/' }
  UNARY_OPS = { '#', '@', '$', '&', '?', ':' }
  BINARY_OPS = { '=' }
  WILDCARDS = { '*' }
  
  def validate(identifier: str) -> bool:
    state = IdentifierUtils.State.ACCEPT_SYLLABLE

    for char in identifier:
      if state == IdentifierUtils.State.ACCEPT_NONWILDCARD:
        if char in IdentifierUtils.DELIMITERS or char in IdentifierUtils.UNARY_OPS or char in IdentifierUtils.BINARY_OPS:
          state = IdentifierUtils.State.ACCEPT_SYLLABLE
        elif char.isalnum():
          state = IdentifierUtils.State.ACCEPT_DELIMITER
        else:
          return False
      elif state == IdentifierUtils.State.ACCEPT_SYLLABLE:
        if char in IdentifierUtils.WILDCARDS:
          state = IdentifierUtils.State.ACCEPT_NONWILDCARD
        elif not char.isalnum():
          return False
        else:
          state = IdentifierUtils.State.ACCEPT_DELIMITER
      elif state == IdentifierUtils.State.ACCEPT_DELIMITER:
        if char in IdentifierUtils.WILDCARDS:
          state = IdentifierUtils.State.ACCEPT_NONWILDCARD
        elif char.isalnum():
          pass
        elif char in IdentifierUtils.DELIMITERS or char in IdentifierUtils.UNARY_OPS or char in IdentifierUtils.BINARY_OPS:
          state = IdentifierUtils.State.ACCEPT_SYLLABLE
        else:
          return False
    
    return True
  
  def tokenize_regex(regex: str) -> list[str]:
    regex_tokens = list()
    
    token_start, token_end = 0, 0
    for char in regex:
      if char == '*':
        regex_tokens.append(char)
        token_start = token_end + 1
        token_end = token_start
      elif token_end == len(regex)-1 or regex[token_end+1] == '*':
        regex_tokens.append(regex[token_start:token_end+1])
        token_start = token_end + 1
        token_end = token_start
      else:
        token_end += 1
    
    return regex_tokens
  
  def match_itemref(itemref: str, regex_tokens: list[str]) -> bool:
    itemref_checkpoints = [ 0 ]
    matched_regex_tokens = 0

    symbol_idx, token_idx = 0, 0

    while symbol_idx <= len(itemref):
      if regex_tokens[matched_regex_tokens] == '*':
        if matched_regex_tokens == len(regex_tokens)-1:
          return True
        elif symbol_idx == len(itemref):
          return False
        elif itemref[symbol_idx] == regex_tokens[matched_regex_tokens+1][0]:
          itemref_checkpoints.append(symbol_idx)
          matched_regex_tokens += 1
          token_idx = 1
        symbol_idx += 1
      
      else:
        if token_idx == len(regex_tokens[matched_regex_tokens]):
          if matched_regex_tokens == len(regex_tokens)-1:
            if symbol_idx == len(itemref):
              return True
            token_idx = 0
            while matched_regex_tokens > 0 and regex_tokens[matched_regex_tokens] != '*':
              itemref_checkpoints.pop()
              matched_regex_tokens -= 1
          matched_regex_tokens += 1
          token_idx = 0
        elif itemref[symbol_idx] == regex_tokens[matched_regex_tokens][token_idx]:
          token_idx += 1
          symbol_idx += 1
        elif matched_regex_tokens > 0:
          itemref_checkpoints.pop()
          matched_regex_tokens -= 1
          token_idx = 0
        else:
          return False