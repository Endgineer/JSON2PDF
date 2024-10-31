from compiler.units.Token import Token

class Nonterminal:
  symbol: str
  first: dict[Token.Kind, list]
  follow: set[Token.Kind]
  nullable: bool
  phantasmal: bool
  primordial_root: bool

  def __init__(self, symbol: str):
    self.symbol = symbol
    self.first = None
    self.follow = None
    self.nullable = False
    self.phantasmal = False
    self.primordial_root = False
  
  def define(self, first: dict[Token.Kind, list], follow: set[Token.Kind]):
    self.first = {key:val[::-1] for key, val in first.items()}
    self.follow = follow
    return self
  
  def set_nullable(self):
    self.nullable = True
    return self
  
  def set_phantasmal(self):
    self.phantasmal = True
    return self
  
  def set_primordial_root(self):
    self.primordial_root = True
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

EOF = Nonterminal('EOF')

REFF = Nonterminal('REFF')
COLLECTION = Nonterminal('COLLECTION')
COLLECTION1 = Nonterminal('COLLECTION1')
COLLECTION2 = Nonterminal('COLLECTION2')
REFS = Nonterminal('REFS')
REF = Nonterminal('REF')
REF1 = Nonterminal('REF1')
REF2 = Nonterminal('REF2')
REFITEM1 = Nonterminal('REFITEM1')
REFITEM2 = Nonterminal('REFITEM2')
PREF = Nonterminal('PREF')

ROOT = Nonterminal('ROOT')
SPECS = Nonterminal('SPECS')
SPECS1 = Nonterminal('SPECS1')
SPECS2 = Nonterminal('SPECS2')
DOCS = Nonterminal('DOCS')
RESUMESPEC = Nonterminal('RESUMESPEC')
RESUMESPEC1 = Nonterminal('RESUMESPEC1')
RESUMESPEC2 = Nonterminal('RESUMESPEC2')
PRESUMESPEC = Nonterminal('PRESUMESPEC')
LETTERSPEC = Nonterminal('LETTERSPEC')
LETTERSPEC1 = Nonterminal('LETTERSPEC1')
LETTERSPEC2 = Nonterminal('LETTERSPEC2')
PLETTERSPEC = Nonterminal('PLETTERSPEC')

RESUME = Nonterminal('RESUME')
RESUME1 = Nonterminal('RESUME1')
RESUME2 = Nonterminal('RESUME2')

LETTER = Nonterminal('LETTER')
LETTER1 = Nonterminal('LETTER1')
LETTER2 = Nonterminal('LETTER2')

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



for to_be_nullable in [REFS, PREF, DOCS, PRESUMESPEC, PLETTERSPEC, SECTIONS, PSECTION, ITEMS, PITEM, PPROP, STRINGPTS, PSTRINGPT, STRINGPAIRS, PSTRINGPAIR]:
  to_be_nullable.set_nullable()
for to_be_phantasmal in [EOF, PREF, PRESUMESPEC, PLETTERSPEC, PSECTION, PITEM, PPROP, PSTRINGPT, PSTRINGPAIR]:
  to_be_phantasmal.set_phantasmal()
for to_be_primordial_root in [RESUME, LETTER]:
  to_be_primordial_root.set_primordial_root()



EOF.define(
  {
    None: []
  },
  { None }
)



REFF.define(
  {
    Token.Kind.LBRACE: [ COLLECTION, EOF ],
    None: [ EOF ]
  },
  { None }
)

COLLECTION.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, COLLECTION1 ]
  },
  { None }
)

COLLECTION1.define(
  {
    Token.Kind.RBRACE: [ REFS, COLLECTION2 ],
    Token.Kind.STRING: [ REFS, COLLECTION2 ]
  },
  COLLECTION.follow
)

COLLECTION2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  COLLECTION.follow
)

REFS.define(
  {
    Token.Kind.STRING: [ REF, PREF ]
  },
  { Token.Kind.RBRACE }
)

REF.define(
  {
    Token.Kind.STRING: [ Token.Kind.STRING, REF1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

REF1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, REF2 ]
  },
  REF.follow
)

REF2.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, REFITEM1 ]
  },
  REF.follow
)

REFITEM1.define(
  {
    Token.Kind.STRING: [ PROPS, REFITEM2 ]
  },
  REF.follow
)

REFITEM2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  REF.follow
)

PREF.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, REF, PREF ]
  },
  { Token.Kind.RBRACE }
)



ROOT.define(
  {
    None: [ EOF ],
    Token.Kind.LBRACE: [ SPECS, EOF ]
  },
  { None }
)

SPECS.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, SPECS1 ]
  },
  { None }
)

SPECS1.define(
  {
    Token.Kind.RBRACE: [ DOCS, SPECS2 ],
    Token.Kind.RESUMEKEY: [ DOCS, SPECS2 ],
    Token.Kind.LETTERKEY: [ DOCS, SPECS2 ]
  },
  SPECS.follow
)

SPECS2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  SPECS.follow
)

DOCS.define(
  {
    Token.Kind.RESUMEKEY: [ RESUMESPEC, PLETTERSPEC ],
    Token.Kind.LETTERKEY: [ LETTERSPEC, PRESUMESPEC ]
  },
  { Token.Kind.RBRACE }
)

RESUMESPEC.define(
  {
    Token.Kind.RESUMEKEY: [ Token.Kind.RESUMEKEY, RESUMESPEC1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

RESUMESPEC1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, RESUMESPEC2 ]
  },
  RESUMESPEC.follow
)

RESUMESPEC2.define(
  {
    Token.Kind.LBRACE: [ RESUME ],
    Token.Kind.NULL: [ Token.Kind.NULL ]
  },
  RESUMESPEC.follow
)

PRESUMESPEC.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, RESUMESPEC ]
  },
  DOCS.follow
)

LETTERSPEC.define(
  {
    Token.Kind.LETTERKEY: [ Token.Kind.LETTERKEY, LETTERSPEC1 ]
  },
  { Token.Kind.RBRACE, Token.Kind.COMMA }
)

LETTERSPEC1.define(
  {
    Token.Kind.COLON: [ Token.Kind.COLON, LETTERSPEC2 ]
  },
  LETTERSPEC.follow
)

LETTERSPEC2.define(
  {
    Token.Kind.LBRACE: [ LETTER ],
    Token.Kind.STRING: [ LETTER ],
    Token.Kind.NULL: [ Token.Kind.NULL ]
  },
  LETTERSPEC.follow
)

PLETTERSPEC.define(
  {
    Token.Kind.COMMA: [ Token.Kind.COMMA, LETTERSPEC ]
  },
  DOCS.follow
)



LETTER.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, LETTER1 ],
    Token.Kind.STRING: [ Token.Kind.STRING ]
  },
  LETTERSPEC.follow
)

LETTER1.define(
  {
    Token.Kind.STRING: [ PROPS, LETTER2 ]
  },
  LETTER.follow
)

LETTER2.define(
  {
    Token.Kind.RBRACE: [ Token.Kind.RBRACE ]
  },
  LETTER.follow
)



RESUME.define(
  {
    Token.Kind.LBRACE: [ Token.Kind.LBRACE, RESUME1 ]
  },
  RESUMESPEC.follow
)

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
)

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
)

ITEMS.define(
  {
    Token.Kind.LBRACE: [ ITEM, PITEM ],
    Token.Kind.STRING: [ ITEM, PITEM ]
  },
  { Token.Kind.RBRACKET }
)

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
)

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
)

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
)

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
)

STRINGPAIRS.define(
  {
    Token.Kind.STRING: [ STRINGPAIR, PSTRINGPAIR ]
  },
  { Token.Kind.RBRACE }
)

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
)
