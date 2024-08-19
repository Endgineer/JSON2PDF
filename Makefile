exe = json2cv

windows: windows-build windows-clean windows-test windows-package

windows-package:
	tar.exe -a -c -f json2cv.zip json2cv.exe samples
	del json2cv.exe

windows-build:
	poetry run pyinstaller -F --specpath .\release\spec --distpath .\ --workpath .\release\build --name $(exe) .\src\main.py

windows-clean:
	del /f /s /q .\release
	rmdir /s /q .\release

windows-test:
	cd .\test && python test.py