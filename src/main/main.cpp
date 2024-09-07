#include "inilogger.hpp"
#include "argparser.hpp"
#include "dllupdater.hpp"
#include "thddispatcher.hpp"

int main(int argc, char *argv[]) {
  IniLogger::log(spdlog::level::info, "Initialized logger");
  
  const std::shared_ptr<std::string> currentCompilerVersion = ArgParser::parse(argc, argv);

  return 0;
}
