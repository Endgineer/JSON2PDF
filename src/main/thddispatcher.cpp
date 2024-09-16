#include "thddispatcher.hpp"

#include "../structs/ThdInfo.hpp"
#include "../compiler/compiler.hpp"
#include "../constants/nonterminals.hpp"
#include "inilogger.hpp"

void ThdDispatcher::routine(const Nonterminal &kernel, const std::string &docJson, const Args &args) {
  Info info = {};

  info.kernel = &kernel;
  info.jsonpath = docJson;
  info.varName = args.varName;
  info.varTitles = args.varTitles;
  info.varAddress = args.varAddress;
  info.varMobile = args.varMobile;
  info.varEmail = args.varEmail;
  info.varLinkedin = args.varLinkedin;
  info.varGithub = args.varGithub;
  info.varColor = args.varColor;
  info.varWebsite = args.varWebsite;
  info.header = args.header;
  info.footer = args.footer;
  info.spaced = args.spaced;
  info.darken = args.darken;
  info.anon = args.anon;
  info.bold = args.bold;
  info.debug = args.debug;
  info.interrupt = args.interrupt;

  Compiler compiler(info);
}

void ThdDispatcher::dispatch(const Args* const args) {
  if(args == nullptr) return;
  
  IniLogger::log(spdlog::level::info, "Checking arguments for thread dispatch");

  if(args->cvJson != std::nullopt && ThdDispatcher::cvThread == nullptr) {
    IniLogger::log(spdlog::level::info, "Dispatching CV thread");
    ThdDispatcher::cvThread = new std::thread(ThdDispatcher::routine, std::cref(Nonterminals::nonterminals.CVROOT), std::cref(args->cvJson.value()), std::cref(*args));
  }

  if(args->clJson != std::nullopt && ThdDispatcher::clThread == nullptr) {
    IniLogger::log(spdlog::level::info, "Dispatching CL thread");
    ThdDispatcher::clThread = new std::thread(ThdDispatcher::routine, std::cref(Nonterminals::nonterminals.CLROOT), std::cref(args->clJson.value()), std::cref(*args));
  }
}

void ThdDispatcher::join() {
  IniLogger::log(spdlog::level::info, "Joining running threads");

  if(ThdDispatcher::cvThread != nullptr) {
    ThdDispatcher::cvThread->join();
    IniLogger::log(spdlog::level::info, "Joining CV thread");
    delete ThdDispatcher::cvThread;
    ThdDispatcher::cvThread = nullptr;
  }

  if(ThdDispatcher::clThread != nullptr) {
    ThdDispatcher::clThread->join();
    IniLogger::log(spdlog::level::info, "Joining CL thread");
    delete ThdDispatcher::clThread;
    ThdDispatcher::clThread = nullptr;
  }
}
