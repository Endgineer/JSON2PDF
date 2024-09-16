#ifndef NONTERMINALS_HPP
#define NONTERMINALS_HPP

#include "../elements/nonterminal.hpp"

class Nonterminals {
  Nonterminals();

  public:

  static Nonterminals nonterminals;

  Nonterminal LBRACE;
  Nonterminal RBRACE;
  Nonterminal LBRACKET;
  Nonterminal RBRACKET;
  Nonterminal COLON;
  Nonterminal COMMA;
  Nonterminal STRING;
  Nonterminal ENDOFFILE;

  Nonterminal CVROOT;
  Nonterminal RESUME;
  Nonterminal RESUME1;
  Nonterminal RESUME2;

  Nonterminal CLROOT;
  Nonterminal LETTER;
  Nonterminal LETTER1;
  Nonterminal LETTER2;

  Nonterminal SECTIONS;
  Nonterminal SECTION;
  Nonterminal SECTION1;
  Nonterminal SECTION2;
  Nonterminal SECTION3;
  Nonterminal SECTION4;
  Nonterminal PSECTION;
  Nonterminal ITEMS;
  Nonterminal ITEM;
  Nonterminal ITEM1;
  Nonterminal ITEM2;
  Nonterminal PITEM;
  Nonterminal PROPS;
  Nonterminal PROP;
  Nonterminal PROP1;
  Nonterminal PROPVAL;
  Nonterminal PPROP;
  Nonterminal STRINGLIST;
  Nonterminal STRINGLIST1;
  Nonterminal STRINGLIST2;
  Nonterminal STRINGPTS;
  Nonterminal STRINGPT;
  Nonterminal PSTRINGPT;
  Nonterminal STRINGDICT;
  Nonterminal STRINGDICT1;
  Nonterminal STRINGDICT2;
  Nonterminal STRINGPAIRS;
  Nonterminal STRINGPAIR;
  Nonterminal STRINGPAIR1;
  Nonterminal STRINGPAIR2;
  Nonterminal PSTRINGPAIR;

  Nonterminal REFFILE;
  Nonterminal COLLECTION;
  Nonterminal COLLECTION1;
  Nonterminal COLLECTION2;
  Nonterminal REFS;
  Nonterminal REF;
  Nonterminal REF1;
  Nonterminal REF2;
  Nonterminal REFITEM1;
  Nonterminal REFITEM2;
  Nonterminal PREF;
};

#endif
