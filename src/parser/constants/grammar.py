from compiler.units.Token import Token

class Nonterminal:
  symbol: str
  first: dict[Token.Kind, list]
  follow: set[Token.Kind]
  nullable: bool

  def __init__(self, symbol: str):
    self.symbol = symbol
    self.first = None
    self.follow = None
    self.nullable = False
  
  def define(self, first: dict[Token.Kind, list], follow: set[Token.Kind], nullable: bool) -> None:
    self.first = {key:val[::-1] for key, val in first.items()}
    self.follow = follow
    self.nullable = nullable
  
  def expand(self, token_kind: Token.Kind) -> list | None:
    if token_kind in self.first:
      return self.first[token_kind]
    elif self.nullable and token_kind in self.follow:
      return []
    else:
      return None
  
  def __repr__(self):
    return self.symbol

ROOT = Nonterminal('ROOT')
SECTIONS = Nonterminal('SECTIONS')
SECTION = Nonterminal('SECTION')
PSECTION = Nonterminal('PSECTION')
ITEMS = Nonterminal('ITEMS')
ITEM = Nonterminal('ITEM')
PITEM = Nonterminal('PITEM')
PROP = Nonterminal('PROP')
PPROP = Nonterminal('PPROP')
PROPVAL = Nonterminal('PROPVAL')
STRINGLIST = Nonterminal('STRINGLIST')
STRINGDICT = Nonterminal('STRINGDICT')
STRINGPTS = Nonterminal('STRINGPTS')
STRINGPT = Nonterminal('STRINGPT')
PSTRINGPT = Nonterminal('PSTRINGPT')
STRINGPAIRS = Nonterminal('STRINGPAIRS')
STRINGPAIR = Nonterminal('STRINGPAIR')
PSTRINGPAIR = Nonterminal('PSTRINGPAIR')

ROOT.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, SECTIONS, Token.Kind.RBRACE, None ]
  },
  { None },
  True
)

SECTIONS.define(
  {
    Token.Kind.STRING: [ SECTION, PSECTION ]
  },
  { Token.Kind.RBRACE },
  True
)

SECTION.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, Token.Kind.COLON, Token.Kind.LBRACKET, ITEMS, Token.Kind.RBRACKET ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

PSECTION.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, SECTION, PSECTION ]
  },
  { Token.Kind.RBRACE },
  True
)

ITEMS.define(
  {
    Token.Kind.LBRACE: [ ITEM, PITEM ],
    Token.Kind.STRING: [ ITEM, PITEM ]
  },
  { Token.Kind.RBRACKET },
  True
)

ITEM.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, PROP, PPROP, Token.Kind.RBRACE ],
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  { Token.Kind.COMMA, Token.Kind.RBRACKET },
  False
)

PITEM.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, ITEM, PITEM ]
  },
  { Token.Kind.RBRACKET },
  True
)

PROP.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, Token.Kind.COLON, PROPVAL ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

PPROP.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, PROP, PPROP ]
  },
  { Token.Kind.RBRACE },
  True
)

PROPVAL.define(
  {
    Token.Kind.LBRACE: [ STRINGDICT ],
    Token.Kind.STRING: [ Token.Kind.STRING ],
    Token.Kind.LBRACKET: [ STRINGLIST ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

STRINGLIST.define(
  {
    Token.Kind.LBRACKET: [ Token.Kind.LBRACKET, STRINGPTS, Token.Kind.RBRACKET ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

STRINGDICT.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, STRINGPAIRS, Token.Kind.RBRACE ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

STRINGPTS.define(
  {
    Token.Kind.STRING: [ STRINGPT, PSTRINGPT ]
  },
  { Token.Kind.RBRACKET },
  True
)

STRINGPT.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  { Token.Kind.COMMA, Token.Kind.RBRACKET },
  False
)

PSTRINGPT.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, STRINGPT, PSTRINGPT ]
  },
  { Token.Kind.RBRACKET },
  True
)

STRINGPAIRS.define(
  {
    Token.Kind.STRING: [ STRINGPAIR, PSTRINGPAIR ]
  },
  { Token.Kind.RBRACE },
  True
)

STRINGPAIR.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, Token.Kind.COLON, Token.Kind.STRING ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA },
  False
)

PSTRINGPAIR.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, STRINGPAIR, PSTRINGPAIR ]
  },
  { Token.Kind.RBRACE },
  True
)