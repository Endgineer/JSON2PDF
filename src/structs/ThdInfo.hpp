#ifndef THDINFO_HPP
#define THDINFO_HPP

#include <vector>
#include <string>

#include "../elements/nonterminal.hpp"

struct Info {
  const Nonterminal *kernel;
  std::string jsonpath;

  std::optional<std::string> varName;
  std::optional<std::vector<std::string>> varTitles;
  std::optional<std::string> varAddress;
  std::optional<std::string> varMobile;
  std::optional<std::string> varEmail;
  std::optional<std::string> varLinkedin;
  std::optional<std::string> varGithub;
  std::optional<std::string> varColor;
  std::optional<std::string> varWebsite;

  bool header;
  bool footer;

  bool spaced;
  bool darken;

  bool anon;
  bool bold;

  bool debug;
  bool interrupt;
};

#endif
