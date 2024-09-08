#include "thddispatcher.hpp"

#include "../structs/ThdInfo.hpp"
#include "../compiler/compiler.hpp"

void ThdDispatcher::dispatch(const Args* const args) {
  if(args == nullptr) return;

  Info info = {};
  info.jsonpath = *args->cvJson;
  info.varName = *args->varName;
  info.varTitles = *args->varTitles;
  info.varAddress = *args->varAddress;
  info.varMobile = *args->varMobile;
  info.varEmail = *args->varEmail;
  info.varLinkedin = *args->varLinkedin;
  info.varGithub = *args->varGithub;
  info.varColor = *args->varColor;
  info.varWebsite = *args->varWebsite;
  info.header = args->header;
  info.footer = args->footer;
  info.spaced = args->spaced;
  info.darken = args->darken;
  info.anon = args->anon;
  info.bold = args->bold;
  info.debug = args->debug;
  info.interrupt = args->interrupt;

  if(args->cvJson != nullptr && ThdDispatcher::cvThread == nullptr) {
    info.doctype = "cv";
    ThdDispatcher::cvThread = new std::thread(Compiler::setup, info);
  }

  if(args->clJson != nullptr && ThdDispatcher::clThread == nullptr) {
    info.doctype = "cl";
    ThdDispatcher::clThread = new std::thread(Compiler::setup, info);
  }
}

void ThdDispatcher::join() {
  if(ThdDispatcher::cvThread != nullptr) {
    ThdDispatcher::cvThread->join();
    delete ThdDispatcher::cvThread;
    ThdDispatcher::cvThread = nullptr;
  }

  if(ThdDispatcher::clThread != nullptr) {
    ThdDispatcher::clThread->join();
    delete ThdDispatcher::clThread;
    ThdDispatcher::clThread = nullptr;
  }
}
