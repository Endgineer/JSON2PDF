#include "argparser.hpp"
#include "inilogger.hpp"
#include "../compiler/compiler.hpp"

const std::string& ArgParser::parse(int argc, char *argv[]) {
  ArgParser::mainArgs = std::make_shared<Args>(argparse::parse<Args>(argc, argv));
  IniLogger::log(spdlog::level::info, "Parsed arguments");
  std::string version = VERSION;
  if(mainArgs->version) {
    IniLogger::log(spdlog::level::info, "Version " + version);
  }

  return version;
}
