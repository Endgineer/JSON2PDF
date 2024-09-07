all: spdlog argparse

spdlog:
	git clone https://github.com/gabime/spdlog.git
	cd spdlog && cmake -B build -G "MinGW Makefiles"
	cd spdlog/build && mingw32-make -j

argparse:
	git clone https://github.com/morrisfranken/argparse.git
	cd argparse && cmake -B build -G "MinGW Makefiles"
	cd argparse/build && mingw32-make -j
