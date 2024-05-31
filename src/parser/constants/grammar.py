from compiler.units.Token import Token

class Nonterminal:
  symbol: str
  first: dict[Token.Kind, list]
  follow: set[Token.Kind]
  nullable: bool
  phantasmal: bool

  def __init__(self, symbol: str):
    self.symbol = symbol
    self.first = None
    self.follow = None
    self.nullable = False
    self.phantasmal = False
  
  def define(self, first: dict[Token.Kind, list], follow: set[Token.Kind]):
    self.first = {key:val[::-1] for key, val in first.items()}
    self.follow = follow
    return self
  
  def is_nullable(self):
    self.nullable = True
    return self
  
  def is_phantasmal(self):
    self.nullable = True
    self.phantasmal = True
    return self
  
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
EOF = Nonterminal('EOF')
RESUME = Nonterminal('RESUME')
RESUME1 = Nonterminal('RESUME1')
RESUME2 = Nonterminal('RESUME2')
SECTIONS = Nonterminal('SECTIONS')
SECTION = Nonterminal('SECTION')
SECTION1 = Nonterminal('SECTION1')
SECTION2 = Nonterminal('SECTION2')
SECTION3 = Nonterminal('SECTION3')
SECTION4 = Nonterminal('SECTION4')
PSECTION = Nonterminal('PSECTION')
ITEMS = Nonterminal('ITEMS')
ITEM = Nonterminal('ITEM')
ITEM1 = Nonterminal('ITEM1')
ITEM2 = Nonterminal('ITEM2')
PITEM = Nonterminal('PITEM')
PROPS = Nonterminal('PROPS')
PROP = Nonterminal('PROP')
PROP1 = Nonterminal('PROP1')
PROPVAL = Nonterminal('PROPVAL')
PPROP = Nonterminal('PPROP')
STRINGLIST = Nonterminal('STRINGLIST')
STRINGLIST1 = Nonterminal('STRINGLIST1')
STRINGLIST2 = Nonterminal('STRINGLIST2')
STRINGPTS = Nonterminal('STRINGPTS')
STRINGPT = Nonterminal('STRINGPT')
PSTRINGPT = Nonterminal('PSTRINGPT')
STRINGDICT = Nonterminal('STRINGDICT')
STRINGDICT1 = Nonterminal('STRINGDICT1')
STRINGDICT2 = Nonterminal('STRINGDICT2')
STRINGPAIRS = Nonterminal('STRINGPAIRS')
STRINGPAIR = Nonterminal('STRINGPAIR')
STRINGPAIR1 = Nonterminal('STRINGPAIR1')
STRINGPAIR2 = Nonterminal('STRINGPAIR2')
PSTRINGPAIR = Nonterminal('PSTRINGPAIR')

ROOT.define(
  {
    Token.Kind.LBRACE: [ RESUME, EOF ],
    None: [ RESUME, EOF ]
  },
  { None }
)

EOF.define(
  {
    None: []
  },
  { None }
)

RESUME.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, RESUME1 ]
  },
  { None }
).is_nullable()

RESUME1.define(
  {
    Token.Kind.RBRACE: [ SECTIONS, RESUME2 ],
    Token.Kind.STRING: [ SECTIONS, RESUME2 ]
  },
  RESUME.follow
)

RESUME2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  RESUME.follow
)

SECTIONS.define(
  {
    Token.Kind.STRING: [ SECTION, PSECTION ]
  },
  { Token.Kind.RBRACE }
).is_nullable()

SECTION.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, SECTION1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

SECTION1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, SECTION2 ]
  },
  SECTION.follow
)

SECTION2.define(
  {
    Token.Kind.LBRACKET: [ Token.Kind.LBRACKET, SECTION3 ]
  },
  SECTION.follow
)

SECTION3.define(
  {
    Token.Kind.STRING: [ ITEMS, SECTION4 ],
    Token.Kind.LBRACE: [ ITEMS, SECTION4 ],
    Token.Kind.RBRACKET: [ ITEMS, SECTION4 ]
  },
  SECTION.follow
)

SECTION4.define(
  {
    Token.Kind.RBRACKET: [ Token.Kind.RBRACKET ]
  },
  SECTION.follow
)

PSECTION.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, SECTION, PSECTION ]
  },
  { Token.Kind.RBRACE }
).is_phantasmal()

ITEMS.define(
  {
    Token.Kind.LBRACE: [ ITEM, PITEM ],
    Token.Kind.STRING: [ ITEM, PITEM ]
  },
  { Token.Kind.RBRACKET }
).is_nullable()

ITEM.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, ITEM1 ],
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  { Token.Kind.COMMA, Token.Kind.RBRACKET }
)

ITEM1.define(
  {
    Token.Kind.STRING: [ PROPS, ITEM2 ]
  },
  ITEM.follow
)

ITEM2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  ITEM.follow
)

PITEM.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, ITEM, PITEM ]
  },
  { Token.Kind.RBRACKET }
).is_phantasmal()

PROPS.define(
  {
    Token.Kind.STRING: [ PROP, PPROP ]
  },
  { Token.Kind.RBRACE }
)

PROP.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, PROP1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

PROP1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, PROPVAL ]
  },
  PROP.follow
)

PPROP.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, PROP, PPROP ]
  },
  { Token.Kind.RBRACE }
).is_phantasmal()

PROPVAL.define(
  {
    Token.Kind.LBRACE: [ STRINGDICT ],
    Token.Kind.STRING: [ Token.Kind.STRING ],
    Token.Kind.LBRACKET: [ STRINGLIST ]
  },
  PROP.follow
)

STRINGLIST.define(
  {
    Token.Kind.LBRACKET: [ Token.Kind.LBRACKET, STRINGLIST1 ]
  },
  PROPVAL.follow
)

STRINGLIST1.define(
  {
    Token.Kind.STRING: [ STRINGPTS, STRINGLIST2 ],
    Token.Kind.RBRACKET: [ STRINGPTS, STRINGLIST2 ]
  },
  STRINGLIST.follow
)

STRINGLIST2.define(
  {
    Token.Kind.RBRACKET: [ Token.Kind.RBRACKET ]
  },
  STRINGLIST.follow
)

STRINGDICT.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, STRINGDICT1 ]
  },
  PROPVAL.follow
)

STRINGDICT1.define(
  {
    Token.Kind.STRING: [ STRINGPAIRS, STRINGDICT2 ],
    Token.Kind.RBRACE: [ STRINGPAIRS, STRINGDICT2 ]
  },
  STRINGDICT.follow
)

STRINGDICT2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  STRINGDICT.follow
)

STRINGPTS.define(
  {
    Token.Kind.STRING: [ STRINGPT, PSTRINGPT ]
  },
  { Token.Kind.RBRACKET }
).is_nullable()

STRINGPT.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  { Token.Kind.COMMA, Token.Kind.RBRACKET }
)

PSTRINGPT.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, STRINGPT, PSTRINGPT ]
  },
  { Token.Kind.RBRACKET }
).is_phantasmal()

STRINGPAIRS.define(
  {
    Token.Kind.STRING: [ STRINGPAIR, PSTRINGPAIR ]
  },
  { Token.Kind.RBRACE }
).is_nullable()

STRINGPAIR.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, STRINGPAIR1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

STRINGPAIR1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, STRINGPAIR2 ]
  },
  STRINGPAIR.follow
)

STRINGPAIR2.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  STRINGPAIR.follow
)

PSTRINGPAIR.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, STRINGPAIR, PSTRINGPAIR ]
  },
  { Token.Kind.RBRACE }
).is_phantasmal()