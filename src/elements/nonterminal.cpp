#include "nonterminal.hpp"

#include <algorithm>

Nonterminal::Nonterminal(const std::string &name) {
  this->name = name;
  this->nullable = false;
  this->phantasmal = false;
}

const std::string& Nonterminal::getName() const {
  return this->name;
}

Nonterminal* Nonterminal::define(const std::map<Token::Kind, std::vector<Nonterminal*>> &productions, const std::set<Token::Kind> &follow) {
  this->productions = productions;
  for(auto& [lhs, rhs] : this->productions) {
    std::reverse(rhs.begin(), rhs.end());
  }
  this->follow = follow;
  return this;
}

Nonterminal* Nonterminal::asNullable() {
  this->nullable = true;
  return this;
}

Nonterminal* Nonterminal::asPhantasmal() {
  this->phantasmal = true;
  return this;
}

std::optional<std::vector<Nonterminal*>> Nonterminal::expand(const Token::Kind& tokenKind) {
  if(this->productions.count(tokenKind) > 0) {
    return std::vector<Nonterminal*>(this->productions[tokenKind]);
  } else if(this->nullable && this->follow.count(tokenKind) > 0) {
    return std::vector<Nonterminal*>();
  } else {
    return std::nullopt;
  }
}

const std::set<Token::Kind>& Nonterminal::getFollow() const {
  return this->follow;
}
