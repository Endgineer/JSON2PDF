PROJECTNAME = json2pdf

MAINSOURCES = ./src/main/*.cpp
COMPILERSOURCES = ./src/compiler/*.cpp

DIR_SPDLOG = ./external/spdlog
LIB_SPDLOG = $(DIR_SPDLOG)/build/*.a
INC_SPDLOG = -I $(DIR_SPDLOG)/include
LNK_SPDLOG = $(LIB_SPDLOG) $(INC_SPDLOG)

all: build

install:
	cd external && mingw32-make

build:
	g++ -shared -o compile.dll -g $(COMPILERSOURCES)
	g++ -o $(PROJECTNAME).exe -g $(MAINSOURCES) $(LNK_SPDLOG)
