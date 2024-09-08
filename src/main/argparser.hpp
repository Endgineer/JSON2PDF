#ifndef ARGPARSER_HPP
#define ARGPARSER_HPP

#include "../structs/CmdArgs.hpp"

class ArgParser {
  inline static std::string *mainVersion = nullptr;

  inline static Args *mainArgs = nullptr;

  public:

  static const std::string *init(int argc, char *argv[]);

  static void clean();

  static const Args* const get();

  ArgParser() = delete;

  ArgParser(ArgParser const&) = delete;

  void operator=(ArgParser const&) = delete;
};

#endif
