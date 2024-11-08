import argparse
import pathlib

class ArgParser:
  json: pathlib.Path
  update: bool
  docName: str | None
  docTitles: list[str] | None
  docAddress: str | None
  docMobile: str | None
  docEmail: str | None
  docLinkedin: str | None
  docGithub: str | None
  docWebsite: str | None
  color: str
  header: bool
  footer: bool
  spaced: bool
  darken: bool
  anon: bool
  bold: bool
  debug: bool
  abort: bool

  def __init__(self) -> None:
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
    
    self.json = args.json
    self.update = args.update
    self.docName = args.name
    self.docTitles = args.titles
    self.docAddress = args.address
    self.docMobile = args.mobile
    self.docEmail = args.email
    self.docLinkedin = args.linkedin
    self.docGithub = args.github
    self.docWebsite = args.website
    self.color = args.color
    self.header = args.header
    self.footer = args.footer
    self.spaced = args.spaced
    self.darken = args.darken
    self.anon = args.anon
    self.bold = args.bold
    self.debug = args.debug
    self.abort = args.abort
