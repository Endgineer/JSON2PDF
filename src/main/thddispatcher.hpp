#ifndef THDDISPATCHER_HPP
#define THDDISPATCHER_HPP

#include "argparser.hpp"
#include <thread>
#include "../elements/nonterminal.hpp"

class ThdDispatcher {
  inline static std::thread *cvThread = nullptr;
  
  inline static std::thread *clThread = nullptr;

  static void routine(const Nonterminal &kernel, const std::string &docJson, const Args &args);
  
  public:

  static void dispatch(const Args* const args);

  static void join();

  ThdDispatcher() = delete;

  ThdDispatcher(ThdDispatcher const&) = delete;

  void operator=(ThdDispatcher const&) = delete;
};

#endif
