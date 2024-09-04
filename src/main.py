import errorhandler
import argparse
import logging
import sys
import os

from compiler.Compiler import Compiler
from parser.constants.grammar import *

def compile(args, root: Nonterminal) -> bool:
  assert root.primordial_root

  if root is CVROOT:
    json = args.cvjson
  elif root is CLROOT:
    json = args.cljson
  
  if json is None: return True

  filename = os.path.basename(json)
  if os.path.isfile(f'{filename}.debug.log'):
    os.remove(f'{filename}.debug.log')
  
  error_handler = errorhandler.ErrorHandler()
  handler = logging.FileHandler(filename=f'{filename}.debug.log', encoding='utf-8') if args.debug else logging.StreamHandler(stream=sys.stderr)
  handler.setFormatter(logging.Formatter(fmt='[%(name)s %(levelname)s]: %(message)s'))

  loggers = dict()
  logging_level = logging.DEBUG if args.debug else logging.INFO
  for phase in ['COMPILER', 'LEXICAL', 'SYNTAX', 'SEMANTIC', 'SYNTHESIS']:
    logger = logging.getLogger(phase)
    logger.setLevel(logging_level)
    logger.addHandler(handler)
    loggers[phase] = logger

  with Compiler(args, root) as compiler:
    compiler.compile(error_handler, args.interrupt)
  
  for logger in loggers.values():
    logger.handlers.clear()
  
  handler.close()
  
  if not args.debug:
    if os.path.isfile(f'{filename}.aux'): os.remove(f'{filename}.aux')
    if os.path.isfile(f'{filename}.log'): os.remove(f'{filename}.log')
    if os.path.isfile(f'{filename}.tex'): os.remove(f'{filename}.tex')
    if os.path.isfile(f'{filename}.xdv'): os.remove(f'{filename}.xdv')
  
  return False

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-cv', '--cvjson', type=str, default=None)
    arg_parser.add_argument('-cl', '--cljson', type=str, default=None)

    arg_parser.add_argument('-n', '--name', type=str, default=None)
    arg_parser.add_argument('-p', '--position', nargs='*', type=str, default=None)
    arg_parser.add_argument('-a', '--address', type=str, default=None)
    arg_parser.add_argument('-m', '--mobile', type=str, default=None)
    arg_parser.add_argument('-e', '--email', type=str, default=None)
    arg_parser.add_argument('-l', '--linkedin', type=str, default=None)
    arg_parser.add_argument('-g', '--github', type=str, default=None)
    arg_parser.add_argument('-c', '--color', type=str, default=None)
    arg_parser.add_argument('-w', '--website', type=str, default=None)
    
    arg_parser.add_argument('--footer', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--header', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--spaced', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--darken', action=argparse.BooleanOptionalAction, default=True)
    arg_parser.add_argument('--anonymized', action=argparse.BooleanOptionalAction, default=False)
    arg_parser.add_argument('--bolded', action=argparse.BooleanOptionalAction, default=False)
    arg_parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    arg_parser.add_argument('--interrupt', action=argparse.BooleanOptionalAction)
    
    args = arg_parser.parse_args()

    basenameError = True
    basenameError = compile(args, CVROOT) and basenameError
    basenameError = compile(args, CLROOT) and basenameError

    if basenameError:
      arg_parser.error('Must specify file basename path for cv or cl.')
