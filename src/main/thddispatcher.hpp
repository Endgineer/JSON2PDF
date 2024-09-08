#ifndef THDDISPATCHER_HPP
#define THDDISPATCHER_HPP

#include "argparser.hpp"
#include <thread>

class ThdDispatcher {
  inline static std::thread *cvThread = nullptr;
  
  inline static std::thread *clThread = nullptr;
  
  public:

  static void dispatch(const Args* const args);

  static void join();

  ThdDispatcher() = delete;

  ThdDispatcher(ThdDispatcher const&) = delete;

  void operator=(ThdDispatcher const&) = delete;
};

#endif
