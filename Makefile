PROJECTNAME = json2pdf

MAINSOURCES = ./src/main/*.cpp
COMPILERSOURCES = ./src/compiler/*.cpp

all: build

install:
	cd external && mingw32-make

build:
	g++ -shared -o compile.dll -g $(COMPILERSOURCES)
	g++ -o $(PROJECTNAME).exe -g $(MAINSOURCES)
