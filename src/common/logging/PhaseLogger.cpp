#include "PhaseLogger.hpp"

namespace PhaseLogging {
  PhaseLogger::PhaseLogger(const std::string &name, spdlog::level::level_enum level) : spdlog::logger(name, {}) {
    set_level(level);

    std::string phases[] = { "MAIN", "LEXER", "PARSER", "SEMANTER", "SYNTHESIZER" };
    for(size_t i = 0; i < 5; i++) {
      sinks_.emplace_back(std::make_shared<PhaseSink>(phases[i]));
    }
  }

  void PhaseLogger::log(Phase phase, spdlog::level::level_enum level, const std::string &message) {
    if(level < level_) return;
    spdlog::details::log_msg logMessage;
    logMessage.level = level;
    logMessage.payload = message;
    logMessage.logger_name = this->sinks_[phase]->name;
    this->sinks_[phase]->log(logMessage);
  }

  std::queue<std::string> PhaseLogger::getTotallyOrderedQueue() {
    std::queue<std::string> totallyOrderedQueue;

    bool notAllEmpty = true;
    while(notAllEmpty) {
      notAllEmpty = false;
      for(size_t i = 0; i < 5; i++) {
        std::optional<std::string> message = this->sinks_[i]->pop();
        if(message != std::nullopt) {
          totallyOrderedQueue.push(message.value());
          notAllEmpty = true;
        }
      }
    }

    return totallyOrderedQueue;
  }

  void PhaseLogger::trace(Phase phase, const std::string &message) {
    log(phase, spdlog::level::trace, message);
  }

  void PhaseLogger::debug(Phase phase, const std::string &message) {
    log(phase, spdlog::level::debug, message);
  }

  void PhaseLogger::info(Phase phase, const std::string &message) {
    log(phase, spdlog::level::info, message);
  }

  void PhaseLogger::warn(Phase phase, const std::string &message) {
    log(phase, spdlog::level::warn, message);
  }

  void PhaseLogger::error(Phase phase, const std::string &message) {
    this->trap = true;
    log(phase, spdlog::level::err, message);
  }

  void PhaseLogger::critical(Phase phase, const std::string &message) {
    this->trap = true;
    log(phase, spdlog::level::critical, message);
  }
}
