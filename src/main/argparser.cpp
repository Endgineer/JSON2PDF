#include "argparser.hpp"
#include "inilogger.hpp"
#include "../compiler/compiler.hpp"

void ArgParser::parse(int argc, char *argv[]) {
  ArgParser::mainArgs = std::make_shared<Args>(argparse::parse<Args>(argc, argv));
  IniLogger::log(spdlog::level::info, "Parsed arguments");
  ArgParser::mainVersion = std::make_shared<std::string>(VERSION);
  if(mainArgs->version) {
    IniLogger::log(spdlog::level::info, "Version " + *ArgParser::mainVersion);
  }
}

const std::string& ArgParser::getVersion() {
  return *ArgParser::mainVersion;
}
