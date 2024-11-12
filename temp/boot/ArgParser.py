import argparse
import pathlib
import requests
import subprocess
import sys

from models.SemanticVersion import SemanticVersion

class ArgParser:
  json_path: pathlib.Path
  about_name: str | None
  about_titles: list[str] | None
  about_address: str | None
  about_mobile: str | None
  about_email: str | None
  about_linkedin: str | None
  about_github: str | None
  about_website: str | None
  color: str
  header: bool
  footer: bool
  spaced: bool
  darken: bool
  anon: bool
  bold: bool
  debug: bool
  abort: bool

  def __init__(self, version: str) -> None:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('json', type=str)
    arg_parser.add_argument('--update', action=argparse.BooleanOptionalAction, default=False)

    arg_parser.add_argument('-n', '--name', type=str, default=None)
    arg_parser.add_argument('-t', '--titles', nargs='*', type=str, default=None)
    arg_parser.add_argument('-a', '--address', type=str, default=None)
    arg_parser.add_argument('-m', '--mobile', type=str, default=None)
    arg_parser.add_argument('-e', '--email', type=str, default=None)
    arg_parser.add_argument('-l', '--linkedin', type=str, default=None)
    arg_parser.add_argument('-g', '--github', type=str, default=None)
    arg_parser.add_argument('-w', '--website', type=str, default=None)

    arg_parser.add_argument('--color', type=str, default='000000')
    
    arg_parser.add_argument('--header', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--footer', action=argparse.BooleanOptionalAction, default=True)
    
    arg_parser.add_argument('--spaced', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--darken', action=argparse.BooleanOptionalAction, default=True)

    arg_parser.add_argument('--anon', action=argparse.BooleanOptionalAction, default=False)
    arg_parser.add_argument('--bold', action=argparse.BooleanOptionalAction, default=False)
    
    arg_parser.add_argument('--debug', action=argparse.BooleanOptionalAction, default=False)
    arg_parser.add_argument('--abort', action=argparse.BooleanOptionalAction, default=False)
    
    args = arg_parser.parse_args()
    
    self.json_path = args.json
    self.about_name = args.name
    self.about_titles = args.titles
    self.about_address = args.address
    self.about_mobile = args.mobile
    self.about_email = args.email
    self.about_linkedin = args.linkedin
    self.about_github = args.github
    self.about_website = args.website
    self.color = args.color
    self.header = args.header
    self.footer = args.footer
    self.spaced = args.spaced
    self.darken = args.darken
    self.anon = args.anon
    self.bold = args.bold
    self.debug = args.debug
    self.abort = args.abort

    if args.update:
      current_version = SemanticVersion(version)

      response = requests.get('https://api.github.com/repos/Endgineer/JSON2PDF/releases/latest')
      response.raise_for_status()
      result = response.json()
      
      if current_version.is_older_than(result['tag_name']):
        response = requests.get('https://github.com/Endgineer/JSON2PDF/releases/latest/download/json2pdf.exe')
        response.raise_for_status()

        exepath = pathlib.Path(sys.argv[0]).with_suffix('.upd')
        with open(f'{exepath}', 'wb') as exefile:
          exefile.write(response.content)
        
        batpath = exepath.parent / 'repl.bat'
        with open(batpath, 'w') as batfile:
          batfile.write((
            f'@echo off\n'
            f'taskkill /F /IM json2pdf.exe\n'
            f'move /Y "{exepath}" "{exepath.with_suffix(".exe")}"\n'
            f'del "%~f0"\n'
          ))
        
        subprocess.Popen(batpath, creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
        sys.exit(0)
