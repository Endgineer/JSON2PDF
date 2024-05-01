windows: windows-build windows-clean windows-hash

windows-build:
	pyinstaller -F --specpath .\release\spec --distpath .\ --workpath .\release\build --name json2cv .\src\main.py

windows-clean:
	del /f /s /q .\release
	rmdir /s /q .\release

windows-hash:
	Certutil -hashfile .\json2cv.exe SHA512