# GENERAL VARIABLES

CXX = g++
CXXFLAGS = -std=c++17

PROJECT = json2pdf

# DIRECTORY VARIABLES

SRC = ./src
BIN = ./bin
LIBS = ./external

MAIN = main
BIN_MAIN = $(BIN)/$(MAIN)
SRC_MAIN = $(SRC)/$(MAIN)
MAIN_SRCS = $(wildcard $(SRC_MAIN)/*.cpp)
MAIN_OBJS = $(addprefix $(BIN_MAIN)/, $(notdir $(MAIN_SRCS:.cpp=.o)))

COMP = compiler
BIN_COMP = $(BIN)/$(COMP)
SRC_COMP = $(SRC)/$(COMP)
COMP_SRCS = $(wildcard $(SRC_COMP)/*.cpp)
COMP_OBJS = $(addprefix $(BIN_COMP)/, $(notdir $(COMP_SRCS:.cpp=.o)))

# LIBRARY VARIABLES

DIR_SPDLOG = $(LIBS)/spdlog
LNK_SPDLOG = $(DIR_SPDLOG)/build/*.a -I $(DIR_SPDLOG)/include

DIR_ARGPARSE = $(LIBS)/argparse
LNK_ARGPARSE = -I $(DIR_ARGPARSE)/include

DIR_LIBCURL = $(LIBS)/libcurl
LNK_LIBCURL = -L$(DIR_LIBCURL)/lib -I$(DIR_LIBCURL)/include

DIR_JSON = $(LIBS)/json
LNK_JSON = -I $(DIR_JSON)/single_include/nlohmann

DIR_PATHFIND = $(LIBS)/pathfind
LNK_PATHFIND = -I $(DIR_PATHFIND)/src $(DIR_PATHFIND)/lib/libpathfind_static.a

LNKS = $(LNK_SPDLOG) $(LNK_ARGPARSE) $(LNK_LIBCURL) $(LNK_JSON) $(LNK_PATHFIND)
LDFLAGS = -lcurl

# ALL TARGET

all: build

# INSTALL TARGET

install:
	cd external && mingw32-make

# BUILD TARGET

$(BIN_COMP)/%.o: $(SRC_COMP)/%.cpp
	$(CXX) $(CXXFLAGS) $(LNK_SPDLOG) -c $< -o $@

$(BIN_MAIN)/%.o: $(SRC_MAIN)/%.cpp
	$(CXX) $(CXXFLAGS) $(LNKS) -c $< -o $@

$(BIN)/compile.dll: $(COMP_OBJS)
	$(CXX) -shared $(COMP_OBJS) -o $@

$(BIN)/$(PROJECT).exe: $(MAIN_OBJS)
	$(CXX) $(MAIN_OBJS) $(LNKS) $(BIN)/compile.dll -o $@ $(LDFLAGS)

prebuild:
	if not exist "$(BIN_MAIN)" mkdir "$(BIN_MAIN)"
	if not exist "$(BIN_COMP)" mkdir "$(BIN_COMP)"
	if not exist "$(BIN)/libcurl-x64.dll" cd $(DIR_LIBCURL)/bin && copy libcurl-x64.dll "../../../$(BIN)"
	if not exist "$(BIN)/cacert.pem" cd $(BIN) && curl -L -o cacert.pem https://curl.se/ca/cacert.pem

build: prebuild $(BIN)/compile.dll $(BIN)/$(PROJECT).exe

# EOF
