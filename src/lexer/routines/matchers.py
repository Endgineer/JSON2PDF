from lexer.components.LexerContext import LexerContext
from compiler.units.Token import Token

# ███████ ████████  █████  ██████  ████████     ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  
# ██         ██    ██   ██ ██   ██    ██        ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ███████ ██████     ██        ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  
#      ██    ██    ██   ██ ██   ██    ██        ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ██   ██ ██   ██    ██        ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ 

def match_start(lexer_ctx: LexerContext) -> bool:
  if lexer_ctx.state != LexerContext.State.START: return False

  match(lexer_ctx.current_char):
    case ' ':
      lexer_ctx.matched_token_start_idx += 1
    case '\n':
      lexer_ctx.matched_token_start_idx += 1
      lexer_ctx.line_start_idx = lexer_ctx.matched_token_start_idx
      lexer_ctx.line_number += 1
    case '\t':
      lexer_ctx.matched_token_start_idx += 1
    case '\r':
      lexer_ctx.matched_token_start_idx += 1
    case '{':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.LBRACE
    case '}':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.RBRACE
    case '[':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.LBRACKET
    case ']':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.RBRACKET
    case ':':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.COLON
    case ',':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.COMMA
    case '"':
      lexer_ctx.create_segment()
      lexer_ctx.matched_token_len += 1
      lexer_ctx.state = LexerContext.State.STR_AWAIT_CHAR
    case _:
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
  
  return True

# ███████ ████████ ██████      ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  ███████ 
# ██         ██    ██   ██     ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ ██      
# ███████    ██    ██████      ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  ███████ 
#      ██    ██    ██   ██     ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██      ██ 
# ███████    ██    ██   ██     ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ ███████ 

def match_str_char(lexer_ctx: LexerContext) -> bool:
  if lexer_ctx.state != LexerContext.State.STR_AWAIT_CHAR: return False

  match(lexer_ctx.current_char):
    case '"':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.STRING
      lexer_ctx.define_segment(False)
    case '{':
      lexer_ctx.define_segment(False)
      lexer_ctx.create_segment()
      lexer_ctx.matched_token_len += 1
      lexer_ctx.state = LexerContext.State.STR_AWAIT_INVOCATION_SYLLABLE
    case '}':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
      lexer_ctx.state = LexerContext.State.DISCARDED_STRING
    case '\\':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
      lexer_ctx.state = LexerContext.State.DISCARDED_STRING
    case '\n':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
      lexer_ctx.state = LexerContext.State.DISCARDED_STRING
    case '\t':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
      lexer_ctx.state = LexerContext.State.DISCARDED_STRING
    case '\r':
      lexer_ctx.matched_token_len += 1
      lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
      lexer_ctx.state = LexerContext.State.DISCARDED_STRING
    case _:
      lexer_ctx.matched_token_len += 1
  
  return True

def match_invocation_syllable(lexer_ctx: LexerContext) -> bool:
  if lexer_ctx.state != LexerContext.State.STR_AWAIT_INVOCATION_SYLLABLE: return False

  if lexer_ctx.current_char.isalnum():
    lexer_ctx.matched_token_len += 1
    lexer_ctx.state = LexerContext.State.STR_AWAIT_INVOCATION_DELIMITER
  else:
    lexer_ctx.matched_token_len += 1
    lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
    lexer_ctx.state = LexerContext.State.DISCARDED_STRING
  
  return True

def match_invocation_delimiter(lexer_ctx: LexerContext) -> bool:
  if lexer_ctx.state != LexerContext.State.STR_AWAIT_INVOCATION_DELIMITER: return False

  if lexer_ctx.current_char == '}':
    lexer_ctx.matched_token_len += 1
    lexer_ctx.state = LexerContext.State.STR_AWAIT_CHAR
    lexer_ctx.define_segment(True)
    lexer_ctx.create_segment()
  elif lexer_ctx.current_char == '_':
    lexer_ctx.matched_token_len += 1
    lexer_ctx.state = LexerContext.State.STR_AWAIT_INVOCATION_SYLLABLE
  elif lexer_ctx.current_char.isalnum():
    lexer_ctx.matched_token_len += 1
  else:
    lexer_ctx.matched_token_len += 1
    lexer_ctx.matched_token_kind = Token.Kind.DISCARDED
    lexer_ctx.state = LexerContext.State.DISCARDED_STRING
  
  return True