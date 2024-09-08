#ifndef THDINFO_HPP
#define THDINFO_HPP

#include <vector>
#include <string>

struct Info {
  std::string doctype;
  std::string jsonpath;

  std::string varName;
  std::vector<std::string> varTitles;
  std::string varAddress;
  std::string varMobile;
  std::string varEmail;
  std::string varLinkedin;
  std::string varGithub;
  std::string varColor;
  std::string varWebsite;

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
