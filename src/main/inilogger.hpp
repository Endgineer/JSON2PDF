#ifndef INILOGGER_CPP
#define INILOGGER_CPP

#include <spdlog/sinks/stdout_sinks.h>

class IniLogger {
  inline static std::shared_ptr<spdlog::logger> initializerLogger = nullptr;
  
  public:

  static void log(spdlog::level::level_enum level, const std::string& message);

  IniLogger() = delete;

  IniLogger(IniLogger const&) = delete;

  void operator=(IniLogger const&) = delete;
};

#endif
