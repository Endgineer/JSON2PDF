exe = json2cv

windows: windows-build windows-clean

windows-build:
	poetry run pyinstaller -F --specpath .\release\spec --distpath .\ --workpath .\release\build --name $(exe) .\src\main.py

windows-clean:
	del /f /s /q .\release
	rmdir /s /q .\release

windows-test:
	.\$(exe) .\samples\resume --footer --debug