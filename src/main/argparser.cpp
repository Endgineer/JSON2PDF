#include "argparser.hpp"

#include "inilogger.hpp"
#include "../compiler/compiler.hpp"

const std::string *ArgParser::init(int argc, char *argv[]) {
  if(mainArgs == nullptr) {
    IniLogger::log(spdlog::level::info, "Parsing arguments");

    ArgParser::mainArgs = new Args(argparse::parse<Args>(argc, argv));

    if(mainArgs->cvJson == std::nullopt && mainArgs->clJson == std::nullopt) {
      IniLogger::log(spdlog::level::err, "Missing cvjson or cljson flag");
    }
    
    ArgParser::mainVersion = new std::string(VERSION);
    if(mainArgs->version) {
      IniLogger::log(spdlog::level::info, "Version " + *ArgParser::mainVersion);
    }
  }

  return ArgParser::mainArgs->update ? ArgParser::mainVersion : nullptr;
}

void ArgParser::clean() {
  if(ArgParser::mainArgs == nullptr) return;
  
  delete ArgParser::mainArgs;
  ArgParser::mainArgs = nullptr;
  delete ArgParser::mainVersion;
  ArgParser::mainVersion = nullptr;
}

const Args* const ArgParser::get() {
  return ArgParser::mainArgs;
}
