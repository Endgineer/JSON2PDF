import typing

from parser.components.ParserContext import ParserContext
from lexer.components.Token import Token

#  ██████  ███████ ███    ██ ███████ ██████  ██  ██████ 
# ██       ██      ████   ██ ██      ██   ██ ██ ██      
# ██   ███ █████   ██ ██  ██ █████   ██████  ██ ██      
# ██    ██ ██      ██  ██ ██ ██      ██   ██ ██ ██      
#  ██████  ███████ ██   ████ ███████ ██   ██ ██  ██████ 

def __derive_max(parser_ctx: ParserContext, named: bool, prefix: Token.Kind, derivation: typing.Callable, max: int, suffix: Token.Kind):
  '''If name is None, it will assume no name or specifier.\nIf max is not positive, it will assume no limit.'''
  key = None

  if named:
    if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
      return None

    key = parser_ctx.last_string
  
  if not parser_ctx.match(prefix): return None
  
  children = []
  if parser_ctx.lexer.peek() != suffix:
    child = derivation(parser_ctx)
    if child is not None: children.append(child)
  while parser_ctx.lexer.peek() != suffix and (max <= 0 or len(children) < max) and parser_ctx.match(Token.Kind.COMMA):
    child = derivation(parser_ctx)
    if child is not None: children.append(child)

  if not parser_ctx.match(suffix): return None

  return children if key is None else (key, children)

# ███████ ██████  ███████  ██████ ██  █████  ██      
# ██      ██   ██ ██      ██      ██ ██   ██ ██      
# ███████ ██████  █████   ██      ██ ███████ ██      
#      ██ ██      ██      ██      ██ ██   ██ ██      
# ███████ ██      ███████  ██████ ██ ██   ██ ███████ 

def derive_curriculumvitae(parser_ctx: ParserContext):
  return __derive_max(parser_ctx,
    False,
    Token.Kind.LBRACE,
    derive_section,
    0,
    Token.Kind.RBRACE
  )

def derive_references(parser_ctx: ParserContext):
  return __derive_max(parser_ctx,
    False,
    Token.Kind.LBRACE,
    derive_reference,
    0,
    Token.Kind.RBRACE
  )

def derive_reference(parser_ctx: ParserContext):
  return __derive_max(parser_ctx,
    True,
    Token.Kind.LBRACE,
    derive_itemproperty,
    6,
    Token.Kind.RBRACE
  )

# ███████ ██████  ███████  ██████ ██ ███████ ██  ██████ 
# ██      ██   ██ ██      ██      ██ ██      ██ ██      
# ███████ ██████  █████   ██      ██ █████   ██ ██      
#      ██ ██      ██      ██      ██ ██      ██ ██      
# ███████ ██      ███████  ██████ ██ ██      ██  ██████ 

def derive_section(parser_ctx: ParserContext):
  return __derive_max(parser_ctx,
    True,
    Token.Kind.LBRACKET,
    derive_item,
    0,
    Token.Kind.RBRACKET
  )

def derive_item(parser_ctx: ParserContext):
  match(parser_ctx.lexer.peek()):
    case Token.Kind.LBRACE:
      return __derive_max(parser_ctx,
        False,
        Token.Kind.LBRACE,
        derive_itemproperty,
        6,
        Token.Kind.RBRACE
      )
    case Token.Kind.STRING:
      return derive_string(parser_ctx)
  
  return None

def derive_itemproperty(parser_ctx: ParserContext):
  if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
    return None
  
  key = parser_ctx.last_string
  
  match(parser_ctx.lexer.peek()):
    case Token.Kind.LBRACE:
      value = __derive_max(parser_ctx,
        False,
        Token.Kind.LBRACE,
        derive_stringpair,
        0,
        Token.Kind.RBRACE
      )
    case Token.Kind.LBRACKET:
      value = __derive_max(parser_ctx,
        False,
        Token.Kind.LBRACKET,
        derive_string,
        0,
        Token.Kind.RBRACKET
      )
    case Token.Kind.STRING:
      value = derive_string(parser_ctx)
  
  return None if value is None else (key, value)

def derive_stringpair(parser_ctx: ParserContext):
  if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
    return None

  key = parser_ctx.last_string
  value = derive_string(parser_ctx)

  return None if value is None else (key, value)

def derive_string(parser_ctx: ParserContext):
  if parser_ctx.match(Token.Kind.STRING):
    return parser_ctx.last_string
  
  return None