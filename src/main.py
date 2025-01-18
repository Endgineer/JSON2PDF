import argparse
import pathlib

from compiler.Compiler import Compiler
from parser.constants.grammar import *

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser()

  arg_parser.add_argument('path', type=str)

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

  with Compiler(args) as compiler:
    compiler.compile(args)
  
  if not args.debug:
    pathlib.Path(f'{args.path}.aux').unlink(missing_ok=True)
    pathlib.Path(f'{args.path}.log').unlink(missing_ok=True)
    pathlib.Path(f'{args.path}.tex').unlink(missing_ok=True)
    pathlib.Path(f'{args.path}.xdv').unlink(missing_ok=True)
