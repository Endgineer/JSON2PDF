#include "inilogger.hpp"
#include "argparser.hpp"
#include "dllupdater.hpp"
#include "thddispatcher.hpp"

int main(int argc, char *argv[]) {
  IniLogger::log(spdlog::level::info, "Initialized logger");
  return 0;
}
