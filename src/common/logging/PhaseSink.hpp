#ifndef PHASESINK_HPP
#define PHASESINK_HPP

#include <spdlog/spdlog.h>
#include <spdlog/sinks/sink.h>
#include <optional>
#include <string>
#include <queue>

class PhaseSink : public spdlog::sinks::sink {
  std::queue<std::string> sinkQueue;

  public:
  
  const std::string name;

  PhaseSink(const std::string &name);

  void log(const spdlog::details::log_msg &message) override;

  void flush() override;

  void set_pattern(const std::string &pattern) override;

  void set_formatter(std::unique_ptr<spdlog::formatter> formatter) override;

  std::optional<std::string> pop();
};

#endif
