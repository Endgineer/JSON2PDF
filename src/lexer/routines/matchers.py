from lexer.components.Context import Context
from lexer.components.Token import Token

# ███████ ████████  █████  ██████  ████████     ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  
# ██         ██    ██   ██ ██   ██    ██        ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ███████ ██████     ██        ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  
#      ██    ██    ██   ██ ██   ██    ██        ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ██   ██ ██   ██    ██        ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ 

def match_start(lexer_context: Context) -> bool:
  if lexer_context.state != Context.State.START: return False

  match(lexer_context.head):
    case ' ':
      lexer_context.token_start_idx += 1
    case '\n':
      lexer_context.token_start_idx += 1
    case '\t':
      lexer_context.token_start_idx += 1
    case '\r':
      lexer_context.token_start_idx += 1
    case '{':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.LBRACE
    case '}':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.RBRACE
    case '[':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.LBRACKET
    case ']':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.RBRACKET
    case ':':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.COLON
    case ',':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.COMMA
    case 'n':
      lexer_context.token_len += 1
      lexer_context.state = Context.State.NULL_AWAIT_U
    case '"':
      lexer_context.token_len += 1
      lexer_context.state = Context.State.STR_AWAIT_CHAR
    case _:
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.DISCARDED
  
  return True

# ███    ██ ██    ██ ██      ██          ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  ███████ 
# ████   ██ ██    ██ ██      ██          ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ ██      
# ██ ██  ██ ██    ██ ██      ██          ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  ███████ 
# ██  ██ ██ ██    ██ ██      ██          ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██      ██ 
# ██   ████  ██████  ███████ ███████     ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ ███████ 

def match_null_u(lexer_context: Context) -> bool:
  if lexer_context.state != Context.State.NULL_AWAIT_U: return False

  if lexer_context.head == 'u':
    lexer_context.token_len += 1
    lexer_context.state = Context.State.NULL_AWAIT_L1
  else:
    lexer_context.token_len += 1
    lexer_context.token_kind = Token.Kind.DISCARDED
  
  return True

def match_null_l1(lexer_context: Context) -> bool:
  if lexer_context.state != Context.State.NULL_AWAIT_L1: return False

  if lexer_context.head == 'l':
    lexer_context.token_len += 1
    lexer_context.state = Context.State.NULL_AWAIT_L2
  else:
    lexer_context.token_len += 1
    lexer_context.token_kind = Token.Kind.DISCARDED
  
  return True

def match_null_l2(lexer_context: Context) -> bool:
  if lexer_context.state != Context.State.NULL_AWAIT_L2: return False

  if lexer_context.head == 'l':
    lexer_context.token_len += 1
    lexer_context.token_kind = Token.Kind.NULL
  else:
    lexer_context.token_len += 1
    lexer_context.token_kind = Token.Kind.DISCARDED
  
  return True

# ███████ ████████ ██████      ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  ███████ 
# ██         ██    ██   ██     ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ ██      
# ███████    ██    ██████      ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  ███████ 
#      ██    ██    ██   ██     ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██      ██ 
# ███████    ██    ██   ██     ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ ███████ 

def match_str_char(lexer_context: Context) -> bool:
  if lexer_context.state != Context.State.STR_AWAIT_CHAR: return False

  match(lexer_context.head):
    case '"':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.STRING
    case '\\':
      lexer_context.token_len += 1
      lexer_context.token_kind = Token.Kind.DISCARDED
    case _:
      lexer_context.token_len += 1
  
  return True