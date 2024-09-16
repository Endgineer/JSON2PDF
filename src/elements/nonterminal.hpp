#ifndef NONTERMINAL_HPP
#define NONTERMINAL_HPP

#include <string>
#include <map>
#include <set>
#include "token.hpp"
#include <vector>
#include <optional>

class Nonterminal {
  std::string name;
  std::map<Token::Kind, std::vector<Nonterminal*>> productions;
  std::set<Token::Kind> follow;
  bool nullable;
  bool phantasmal;

  public:

  Nonterminal(const std::string &name);

  const std::string& getName() const;

  Nonterminal* define(const std::map<Token::Kind, std::vector<Nonterminal*>> &productions, const std::set<Token::Kind> &follow);
  
  Nonterminal* asNullable();

  Nonterminal* asPhantasmal();

  std::optional<std::vector<Nonterminal*>> expand(const Token::Kind& tokenKind);
  
  const std::set<Token::Kind>& getFollow() const;
};

#endif
