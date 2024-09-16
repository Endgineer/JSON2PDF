#include "nonterminals.hpp"

#include <set>
#include "../elements/token.hpp"

Nonterminals Nonterminals::nonterminals;

Nonterminals::Nonterminals() :
  LBRACE("LBRACE"),
  RBRACE("RBRACE"),
  LBRACKET("LBRACKET"),
  RBRACKET("RBRACKET"),
  COLON("COLON"),
  COMMA("COMMA"),
  STRING("STRING"),
  ENDOFFILE("ENDOFFILE"),
  CVROOT("CVROOT"),
  RESUME("RESUME"),
  RESUME1("RESUME1"),
  RESUME2("RESUME2"),
  CLROOT("CLROOT"),
  LETTER("LETTER"),
  LETTER1("LETTER1"),
  LETTER2("LETTER2"),
  SECTIONS("SECTIONS"),
  SECTION("SECTION"),
  SECTION1("SECTION1"),
  SECTION2("SECTION2"),
  SECTION3("SECTION3"),
  SECTION4("SECTION4"),
  PSECTION("PSECTION"),
  ITEMS("ITEMS"),
  ITEM("ITEM"),
  ITEM1("ITEM1"),
  ITEM2("ITEM2"),
  PITEM("PITEM"),
  PROPS("PROPS"),
  PROP("PROP"),
  PROP1("PROP1"),
  PROPVAL("PROPVAL"),
  PPROP("PPROP"),
  STRINGLIST("STRINGLIST"),
  STRINGLIST1("STRINGLIST1"),
  STRINGLIST2("STRINGLIST2"),
  STRINGPTS("STRINGPTS"),
  STRINGPT("STRINGPT"),
  PSTRINGPT("PSTRINGPT"),
  STRINGDICT("STRINGDICT"),
  STRINGDICT1("STRINGDICT1"),
  STRINGDICT2("STRINGDICT2"),
  STRINGPAIRS("STRINGPAIRS"),
  STRINGPAIR("STRINGPAIR"),
  STRINGPAIR1("STRINGPAIR1"),
  STRINGPAIR2("STRINGPAIR2"),
  PSTRINGPAIR("PSTRINGPAIR"),
  REFFILE("REFFILE"),
  COLLECTION("COLLECTION"),
  COLLECTION1("COLLECTION1"),
  COLLECTION2("COLLECTION2"),
  REFS("REFS"),
  REF("REF"),
  REF1("REF1"),
  REF2("REF2"),
  REFITEM1("REFITEM1"),
  REFITEM2("REFITEM2"),
  PREF("PREF")
{
  std::set<Nonterminal*> nullables({&REFS, &PREF, &SECTIONS, &PSECTION, &ITEMS, &PITEM, &PPROP, &STRINGPTS, &PSTRINGPT, &STRINGPAIRS, &PSTRINGPAIR});
  std::set<Nonterminal*> phantasms({&ENDOFFILE, &PREF, &PSECTION, &PITEM, &PPROP, &PSTRINGPT, &PSTRINGPAIR});

  for(auto nullable : nullables) nullable->asNullable();
  for(auto phantasm : phantasms) phantasm->asPhantasmal();

  LBRACE.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  RBRACE.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  LBRACKET.define(
    {
      {Token::Kind::LBRACKET, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  RBRACKET.define(
    {
      {Token::Kind::RBRACKET, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  COLON.define(
    {
      {Token::Kind::COLON, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  COMMA.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  STRING.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  ENDOFFILE.define(
    {
      {Token::Kind::ENDOFFILE, std::vector<Nonterminal*>()}
    },
    std::set<Token::Kind>({})
  );

  CVROOT.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&RESUME, &ENDOFFILE})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  RESUME.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &RESUME1})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  RESUME1.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&SECTIONS, &RESUME2})},
      {Token::Kind::STRING, std::vector<Nonterminal*>({&SECTIONS, &RESUME2})}
    },
    RESUME.getFollow()
  );

  RESUME2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    RESUME.getFollow()
  );

  CLROOT.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LETTER, &ENDOFFILE})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  LETTER.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &LETTER1})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  LETTER1.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&PROPS, &LETTER2})}
    },
    LETTER.getFollow()
  );

  LETTER2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    LETTER.getFollow()
  );

  SECTIONS.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&SECTION, &PSECTION})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  SECTION.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING, &SECTION1})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE, Token::Kind::COMMA})
  );

  SECTION1.define(
    {
      {Token::Kind::COLON, std::vector<Nonterminal*>({&COLON, &SECTION2})}
    },
    SECTION.getFollow()
  );

  SECTION2.define(
    {
      {Token::Kind::LBRACKET, std::vector<Nonterminal*>({&LBRACKET, &SECTION3})}
    },
    SECTION.getFollow()
  );

  SECTION3.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&ITEMS, &SECTION4})},
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&ITEMS, &SECTION4})},
      {Token::Kind::RBRACKET, std::vector<Nonterminal*>({&ITEMS, &SECTION4})}
    },
    SECTION.getFollow()
  );

  SECTION4.define(
    {
      {Token::Kind::RBRACKET, std::vector<Nonterminal*>({&RBRACKET})}
    },
    SECTION.getFollow()
  );

  PSECTION.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &SECTION, &PSECTION})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  ITEMS.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&ITEM, &PITEM})},
      {Token::Kind::STRING, std::vector<Nonterminal*>({&ITEM, &PITEM})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACKET})
  );

  ITEM.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &ITEM1})},
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING})}
    },
    std::set<Token::Kind>({Token::Kind::COMMA, Token::Kind::RBRACKET})
  );

  ITEM1.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&PROPS, &ITEM2})}
    },
    ITEM.getFollow()
  );

  ITEM2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    ITEM.getFollow()
  );

  PITEM.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &ITEM, &PITEM})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACKET})
  );

  PROPS.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&PROP, &PPROP})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  PROP.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING, &PROP1})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE, Token::Kind::COMMA})
  );

  PROP1.define(
    {
      {Token::Kind::COLON, std::vector<Nonterminal*>({&COLON, &PROPVAL})}
    },
    PROP.getFollow()
  );

  PROPVAL.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&STRINGDICT})},
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING})},
      {Token::Kind::LBRACKET, std::vector<Nonterminal*>({&STRINGLIST})}
    },
    PROP.getFollow()
  );

  PPROP.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &PROP, &PPROP})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  STRINGLIST.define(
    {
      {Token::Kind::LBRACKET, std::vector<Nonterminal*>({&LBRACKET, &STRINGLIST1})}
    },
    PROPVAL.getFollow()
  );

  STRINGLIST1.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRINGPTS, &STRINGLIST2})},
      {Token::Kind::RBRACKET, std::vector<Nonterminal*>({&STRINGPTS, &STRINGLIST2})}
    },
    STRINGLIST.getFollow()
  );

  STRINGLIST2.define(
    {
      {Token::Kind::RBRACKET, std::vector<Nonterminal*>({&RBRACKET})}
    },
    STRINGLIST.getFollow()
  );

  STRINGPTS.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRINGPT, &PSTRINGPT})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACKET})
  );

  STRINGPT.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING})}
    },
    std::set<Token::Kind>({Token::Kind::COMMA, Token::Kind::RBRACKET})
  );

  PSTRINGPT.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &STRINGPT, &PSTRINGPT})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACKET})
  );

  STRINGDICT.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &STRINGDICT1})}
    },
    PROPVAL.getFollow()
  );

  STRINGDICT1.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRINGPAIRS, &STRINGDICT2})},
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&STRINGPAIRS, &STRINGDICT2})}
    },
    STRINGDICT.getFollow()
  );

  STRINGDICT2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    STRINGDICT.getFollow()
  );

  STRINGPAIRS.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRINGPAIR, &PSTRINGPAIR})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  STRINGPAIR.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING, &STRINGPAIR1})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE, Token::Kind::COMMA})
  );

  STRINGPAIR1.define(
    {
      {Token::Kind::COLON, std::vector<Nonterminal*>({&COLON, &STRINGPAIR2})}
    },
    STRINGPAIR.getFollow()
  );

  STRINGPAIR2.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING})}
    },
    STRINGPAIR.getFollow()
  );

  PSTRINGPAIR.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &STRINGPAIR, &PSTRINGPAIR})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );
  
  REFFILE.define(
    {
      {Token::Kind::ENDOFFILE, std::vector<Nonterminal*>({&ENDOFFILE})},
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&COLLECTION, &ENDOFFILE})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  COLLECTION.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &COLLECTION1})}
    },
    std::set<Token::Kind>({Token::Kind::ENDOFFILE})
  );

  COLLECTION1.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&REFS, &COLLECTION2})},
      {Token::Kind::STRING, std::vector<Nonterminal*>({&REFS, &COLLECTION2})}
    },
    COLLECTION.getFollow()
  );

  COLLECTION2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    COLLECTION.getFollow()
  );

  REFS.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&REF, &PREF})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );

  REF.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&STRING, &REF1})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE, Token::Kind::COMMA})
  );

  REF1.define(
    {
      {Token::Kind::COLON, std::vector<Nonterminal*>({&COLON, &REF2})}
    },
    REF.getFollow()
  );

  REF2.define(
    {
      {Token::Kind::LBRACE, std::vector<Nonterminal*>({&LBRACE, &REFITEM1})}
    },
    REF.getFollow()
  );

  REFITEM1.define(
    {
      {Token::Kind::STRING, std::vector<Nonterminal*>({&PROPS, &REFITEM2})}
    },
    REF.getFollow()
  );

  REFITEM2.define(
    {
      {Token::Kind::RBRACE, std::vector<Nonterminal*>({&RBRACE})}
    },
    REF.getFollow()
  );

  PREF.define(
    {
      {Token::Kind::COMMA, std::vector<Nonterminal*>({&COMMA, &REF, &PREF})}
    },
    std::set<Token::Kind>({Token::Kind::RBRACE})
  );
}
