name = json2pdf

windows: windows-build windows-clean windows-test windows-package

windows-package:
	tar -cf $(name).zip $(name).exe samples -C src\__pycache__ main*.pyc
	del $(name).exe

windows-build:
	python -m py_compile .\src\main.py
	poetry run pyinstaller -F --specpath .\release\spec --distpath .\ --workpath .\release\build --name $(name) .\src\main.py

windows-clean:
	del /f /s /q .\release
	rmdir /s /q .\release

windows-test:
	cd .\test && python test.py

windows-update:
	poetry update
