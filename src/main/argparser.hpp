#ifndef ARGPARSER_HPP
#define ARGPARSER_HPP

#include <argparse/argparse.hpp>

class ArgParser {
  struct Args : public argparse::Args {
    bool &version = flag("v,version", "Display current version").set_default(false);
    bool &update = flag("u,update", "Check for updates").set_default(false);

    std::shared_ptr<std::string> &cvJson = kwarg("cv,cvjson", "Path to cv json");
    std::shared_ptr<std::string> &clJson = kwarg("cl,cljson", "Path to cl json");

    std::shared_ptr<std::string> &varName = kwarg("n,name", "Name");
    std::shared_ptr<std::vector<std::string>> &varTitles = kwarg("t,titles", "Titles").multi_argument();
    std::shared_ptr<std::string> &varAddress = kwarg("a,address", "Address");
    std::shared_ptr<std::string> &varMobile = kwarg("m,mobile", "Mobile");
    std::shared_ptr<std::string> &varEmail = kwarg("e,email", "Email");
    std::shared_ptr<std::string> &varLinkedin = kwarg("l,linkedin", "Linkedin");
    std::shared_ptr<std::string> &varGithub = kwarg("g,github", "Github");
    std::shared_ptr<std::string> &varColor = kwarg("c,color", "Color");
    std::shared_ptr<std::string> &varWebsite = kwarg("w,website", "Website");

    bool &header = flag("header", "Enables document header").set_default(true);
    bool &footer = flag("footer", "Enables document footer").set_default(true);

    bool &spaced = flag("spaced", "Spaces document elements").set_default(true);
    bool &darken = flag("darken", "Darkens document elements").set_default(true);

    bool &anon = flag("anon", "Anonymize during compilation").set_default(false);
    bool &bold = flag("bold", "Bolden during compilation").set_default(false);

    bool &debug = flag("debug", "Run in debug mode").set_default(false);
    bool &interrupt = flag("interrupt", "Interrupt deep compilation").set_default(false);
  };

  inline static std::shared_ptr<std::string> mainVersion = nullptr;

  inline static std::shared_ptr<Args> mainArgs = nullptr;

  public:

  static void parse(int argc, char *argv[]);

  static const std::string& getVersion();

  ArgParser() = delete;

  ArgParser(ArgParser const&) = delete;

  void operator=(ArgParser const&) = delete;
};

#endif
