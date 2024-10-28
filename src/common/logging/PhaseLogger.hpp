#ifndef QUEUELOGGER_HPP
#define QUEUELOGGER_HPP

#include <spdlog/spdlog.h>
#include <spdlog/logger.h>
#include <memory>
#include <string>
#include <vector>

#include "PhaseSink.hpp"

namespace PhaseLogging {
  enum Phase {
    MAIN,
    LEXER,
    PARSER,
    SEMANTER,
    SYNTHESIZER
  };

  class PhaseLogger : public spdlog::logger {
    std::vector<std::shared_ptr<PhaseSink>> sinks_;
    bool trap;

    void log(Phase phase, spdlog::level::level_enum level, const std::string &message);

    using spdlog::logger::log;
    using spdlog::logger::trace;
    using spdlog::logger::debug;
    using spdlog::logger::info;
    using spdlog::logger::warn;
    using spdlog::logger::error;
    using spdlog::logger::critical;
    
    public:

    PhaseLogger(const std::string &name, spdlog::level::level_enum level);

    std::queue<std::string> getTotallyOrderedQueue();

    void trace(Phase phase, const std::string &message);

    void debug(Phase phase, const std::string &message);

    void info(Phase phase, const std::string &message);

    void warn(Phase phase, const std::string &message);

    void error(Phase phase, const std::string &message);

    void critical(Phase phase, const std::string &message);
  };
}

#endif
