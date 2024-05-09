import typing

from parser.components.ParserContext import ParserContext
from compiler.components.Token import Token
import compiler.consts.typing as ptype

#  ██████  ███████ ███    ██ ███████ ██████  ██  ██████ 
# ██       ██      ████   ██ ██      ██   ██ ██ ██      
# ██   ███ █████   ██ ██  ██ █████   ██████  ██ ██      
# ██    ██ ██      ██  ██ ██ ██      ██   ██ ██ ██      
#  ██████  ███████ ██   ████ ███████ ██   ██ ██  ██████ 

def __derive_max(parser_ctx: ParserContext, named: bool, prefix: Token.Kind, derivation: typing.Callable, max: int, suffix: Token.Kind):
  key = None

  if named:
    if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
      return None

    key = parser_ctx.matched_token
  
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

def derive_curriculumvitae(parser_ctx: ParserContext) -> ptype.SectionsList:
  return __derive_max(parser_ctx,
    False,
    Token.Kind.LBRACE,
    derive_section,
    0,
    Token.Kind.RBRACE
  )

def derive_references(parser_ctx: ParserContext) -> ptype.ReferencedItemsList:
  return __derive_max(parser_ctx,
    False,
    Token.Kind.LBRACE,
    derive_reference,
    0,
    Token.Kind.RBRACE
  )

def derive_reference(parser_ctx: ParserContext) -> ptype.ReferencedItem:
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

def derive_section(parser_ctx: ParserContext) -> ptype.Section:
  return __derive_max(parser_ctx,
    True,
    Token.Kind.LBRACKET,
    derive_item,
    0,
    Token.Kind.RBRACKET
  )

def derive_item(parser_ctx: ParserContext) -> ptype.RefOrItem:
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

def derive_itemproperty(parser_ctx: ParserContext) -> ptype.ItemProperty:
  if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
    return None
  
  key = parser_ctx.matched_token
  
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

def derive_stringpair(parser_ctx: ParserContext) -> ptype.StringTokenPair:
  if not (parser_ctx.match(Token.Kind.STRING) and parser_ctx.match(Token.Kind.COLON)):
    return None

  key = parser_ctx.matched_token
  value = derive_string(parser_ctx)

  return None if value is None else (key, value)

def derive_string(parser_ctx: ParserContext) -> ptype.StringToken:
  if parser_ctx.match(Token.Kind.STRING):
    return parser_ctx.matched_token
  
  return None