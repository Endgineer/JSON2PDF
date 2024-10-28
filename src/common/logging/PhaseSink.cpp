#include "PhaseSink.hpp"

PhaseSink::PhaseSink(const std::string &name) : name(name) {}

void PhaseSink::log(const spdlog::details::log_msg &message) {
  const static std::string levels[] = { "TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" };
  sinkQueue.push(fmt::format("[{} - {}] {}", message.logger_name, levels[message.level], message.payload));
}

void PhaseSink::flush() {}

void PhaseSink::set_pattern(const std::string &pattern) {}

void PhaseSink::set_formatter(std::unique_ptr<spdlog::formatter> formatter) {}

std::optional<std::string> PhaseSink::pop() {
  if(sinkQueue.empty()) {
    return std::nullopt;
  }

  std::string message = sinkQueue.front();
  sinkQueue.pop();
  return message;
}
