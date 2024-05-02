from lexer.components.Context import Context
from lexer.components.Token import Token

# ███████ ████████  █████  ██████  ████████     ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  
# ██         ██    ██   ██ ██   ██    ██        ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ███████ ██████     ██        ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  
#      ██    ██    ██   ██ ██   ██    ██        ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
# ███████    ██    ██   ██ ██   ██    ██        ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ 

def match_start(lexer_ctx: Context) -> bool:
  if lexer_ctx.state != Context.State.START: return False

  match(lexer_ctx.head):
    case ' ':
      lexer_ctx.token_start_idx += 1
    case '\n':
      lexer_ctx.token_start_idx += 1
    case '\t':
      lexer_ctx.token_start_idx += 1
    case '\r':
      lexer_ctx.token_start_idx += 1
    case '{':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.LBRACE
    case '}':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.RBRACE
    case '[':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.LBRACKET
    case ']':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.RBRACKET
    case ':':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.COLON
    case ',':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.COMMA
    case 'n':
      lexer_ctx.token_len += 1
      lexer_ctx.state = Context.State.NULL_AWAIT_U
    case '"':
      lexer_ctx.token_len += 1
      lexer_ctx.state = Context.State.STR_AWAIT_CHAR
    case _:
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.DISCARDED
  
  return True

# ███    ██ ██    ██ ██      ██          ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  ███████ 
# ████   ██ ██    ██ ██      ██          ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ ██      
# ██ ██  ██ ██    ██ ██      ██          ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  ███████ 
# ██  ██ ██ ██    ██ ██      ██          ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██      ██ 
# ██   ████  ██████  ███████ ███████     ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ ███████ 

def match_null_u(lexer_ctx: Context) -> bool:
  if lexer_ctx.state != Context.State.NULL_AWAIT_U: return False

  if lexer_ctx.head == 'u':
    lexer_ctx.token_len += 1
    lexer_ctx.state = Context.State.NULL_AWAIT_L1
  else:
    lexer_ctx.token_len += 1
    lexer_ctx.token_kind = Token.Kind.DISCARDED
  
  return True

def match_null_l1(lexer_ctx: Context) -> bool:
  if lexer_ctx.state != Context.State.NULL_AWAIT_L1: return False

  if lexer_ctx.head == 'l':
    lexer_ctx.token_len += 1
    lexer_ctx.state = Context.State.NULL_AWAIT_L2
  else:
    lexer_ctx.token_len += 1
    lexer_ctx.token_kind = Token.Kind.DISCARDED
  
  return True

def match_null_l2(lexer_ctx: Context) -> bool:
  if lexer_ctx.state != Context.State.NULL_AWAIT_L2: return False

  if lexer_ctx.head == 'l':
    lexer_ctx.token_len += 1
    lexer_ctx.token_kind = Token.Kind.NULL
  else:
    lexer_ctx.token_len += 1
    lexer_ctx.token_kind = Token.Kind.DISCARDED
  
  return True

# ███████ ████████ ██████      ███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  ███████ 
# ██         ██    ██   ██     ████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ ██      
# ███████    ██    ██████      ██ ████ ██ ███████    ██    ██      ███████ █████   ██████  ███████ 
#      ██    ██    ██   ██     ██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██      ██ 
# ███████    ██    ██   ██     ██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ ███████ 

def match_str_char(lexer_ctx: Context) -> bool:
  if lexer_ctx.state != Context.State.STR_AWAIT_CHAR: return False

  match(lexer_ctx.head):
    case '"':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.STRING
    case '\\':
      lexer_ctx.token_len += 1
      lexer_ctx.token_kind = Token.Kind.DISCARDED
    case _:
      lexer_ctx.token_len += 1
  
  return True