#include "dllupdater.hpp"

#include "inilogger.hpp"
#include "json.hpp"

bool DllUpdater::versionIsBehind(const std::string &currentCompilerVersion, const std::string &latestCompilerVersion) {
  int currentCompilerVersionNumbers[3], latestCompilerVersionNumbers[3];

  std::istringstream currentVersionParser(currentCompilerVersion);
  currentVersionParser >> currentCompilerVersionNumbers[0];
  currentVersionParser.get();
  currentVersionParser >> currentCompilerVersionNumbers[1];
  currentVersionParser.get();
  currentVersionParser >> currentCompilerVersionNumbers[2];

  std::istringstream latestVersionParser(latestCompilerVersion);
  latestVersionParser >> latestCompilerVersionNumbers[0];
  latestVersionParser.get();
  latestVersionParser >> latestCompilerVersionNumbers[1];
  latestVersionParser.get();
  latestVersionParser >> latestCompilerVersionNumbers[2];

  return std::lexicographical_compare(currentCompilerVersionNumbers, currentCompilerVersionNumbers+3, latestCompilerVersionNumbers, latestCompilerVersionNumbers+3);
}

size_t DllUpdater::writeBufferCallback(char *chunk, size_t size, size_t nmemb, std::string *buffer) {
  buffer->append(chunk, size*nmemb);
  return size*nmemb;
}

CURLcode DllUpdater::update(const std::string *currentCompilerVersion) {
  if(currentCompilerVersion == nullptr) return CURLE_OK;

  IniLogger::log(spdlog::level::info, "Checking for updates");

  CURLcode returnCode = curl_global_init(CURL_GLOBAL_ALL);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to initialize curl global state");
    return returnCode;
  }

  CURL *curlHandle = curl_easy_init();
  if(curlHandle == nullptr) {
    IniLogger::log(spdlog::level::err, "Failed to initialize curl handle");
    curl_global_cleanup();
    return CURLE_FAILED_INIT;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_FOLLOWLOCATION, 1L);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set follow location curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_CAINFO, "cacert.pem");
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set certificate authority information curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_USERAGENT, "JSON2PDF/" + *currentCompilerVersion);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set user agent curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  std::string responseBuffer;

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_WRITEFUNCTION, DllUpdater::writeBufferCallback);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set write buffer function curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_WRITEDATA, &responseBuffer);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set write buffer data curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_URL, "https://api.github.com/repos/Endgineer/JSON2PDF/tags");
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set fetch url curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_perform(curlHandle);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to perform fetch");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  nlohmann::json responseJson = nlohmann::json::parse(responseBuffer);
  if(responseJson.size() == 0) {
    IniLogger::log(spdlog::level::info, "No updates available");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }
  
  std::string latestCompilerVersion = responseJson[0]["name"];
  if(!DllUpdater::versionIsBehind(*currentCompilerVersion, latestCompilerVersion)) {
    IniLogger::log(spdlog::level::info, "Already up to date");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  IniLogger::log(spdlog::level::info, "Found new version "+latestCompilerVersion);

  responseBuffer.clear();

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_WRITEFUNCTION, DllUpdater::writeBufferCallback);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set write file function curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_WRITEDATA, &responseBuffer);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set write file data curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_setopt(curlHandle, CURLOPT_URL, "https://github.com/Endgineer/JSON2PDF/releases/latest/download/compile.dll");
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to set download url curl option");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  returnCode = curl_easy_perform(curlHandle);
  if(returnCode != CURLE_OK) {
    IniLogger::log(spdlog::level::err, "Failed to perform download");
    curl_easy_cleanup(curlHandle);
    curl_global_cleanup();
    return returnCode;
  }

  std::ofstream responseFile("compile.dll", std::ofstream::out | std::ofstream::binary | std::ofstream::trunc);
  responseFile.write(responseBuffer.c_str(), responseBuffer.size());
  responseFile.close();

  curl_easy_cleanup(curlHandle);
  curl_global_cleanup();

  IniLogger::log(spdlog::level::info, "Updated compiler " + *currentCompilerVersion + " -> " + latestCompilerVersion);

  return returnCode;
}
