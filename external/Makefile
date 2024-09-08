all: spdlog argparse libcurl

spdlog:
	git clone https://github.com/gabime/spdlog.git
	cd spdlog && cmake -B build -G "MinGW Makefiles"
	cd spdlog/build && mingw32-make -j

argparse:
	git clone https://github.com/morrisfranken/argparse.git

libcurl:
	curl -L -o libcurl.zip https://curl.se/windows/latest.cgi?p=win64-mingw.zip
	tar -xf libcurl.zip && del libcurl.zip && move curl* libcurl
