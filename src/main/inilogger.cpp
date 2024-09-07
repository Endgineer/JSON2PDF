#include "inilogger.hpp"

void IniLogger::log(spdlog::level::level_enum level, const std::string& message) {
  if(IniLogger::initializerLogger == nullptr) {
    IniLogger::initializerLogger = spdlog::stdout_logger_st("main");
    IniLogger::initializerLogger->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [json2pdf] [%n] [%l] %v");
  }

  IniLogger::initializerLogger->log(level, message);
}
