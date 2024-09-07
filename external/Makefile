all: spdlog

spdlog:
	git clone https://github.com/gabime/spdlog.git
	cd spdlog && cmake -B build -G "MinGW Makefiles"
	cd spdlog/build && mingw32-make -j
