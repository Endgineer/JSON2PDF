#ifndef TOKEN_HPP
#define TOKEN_HPP

class Token {
  public:
  
  enum Kind {
    DISCARDED,
    LBRACE,
    RBRACE,
    LBRACKET,
    RBRACKET,
    COLON,
    COMMA,
    STRING,
    ENDOFFILE,
  };
};

#endif
