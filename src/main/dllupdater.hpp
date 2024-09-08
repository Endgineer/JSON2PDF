#ifndef DLLUPDATER_HPP
#define DLLUPDATER_HPP

#include <fstream>
#include <curl/curl.h>

class DllUpdater {
  static size_t writeBufferCallback(char *chunk, size_t size, size_t nmemb, std::string* buffer);
  
  static size_t writeFileCallback(char *chunk, size_t size, size_t nmemb, std::ofstream* file);

  public:

  static CURLcode update(const std::string *currentCompilerVersion);

  DllUpdater() = delete;

  DllUpdater(DllUpdater const&) = delete;

  void operator=(DllUpdater const&) = delete;
};

#endif
