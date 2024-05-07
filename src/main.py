import errorhandler
import argparse
import logging
import sys
import os

from compiler.Compiler import Compiler

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(dest='file_path', type=str)
    arg_parser.add_argument('-n', '--name', type=str, default=None)
    arg_parser.add_argument('-p', '--position', nargs='*', type=str, default=None)
    arg_parser.add_argument('-a', '--address', type=str, default=None)
    arg_parser.add_argument('-m', '--mobile', type=str, default=None)
    arg_parser.add_argument('-e', '--email', type=str, default=None)
    arg_parser.add_argument('-l', '--linkedin', type=str, default=None)
    arg_parser.add_argument('-g', '--github', type=str, default=None)
    arg_parser.add_argument('-c', '--color', type=str, default=None)
    arg_parser.add_argument('-w', '--website', type=str, default=None)
    arg_parser.add_argument('--footer', action=argparse.BooleanOptionalAction)
    arg_parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    args = arg_parser.parse_args()

    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt='[%(name)s %(levelname)s]: %(message)s'))
    
    logging.getLogger('COMPILER').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('COMPILER').addHandler(stream_handler)
    logging.getLogger('LEXICAL').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('LEXICAL').addHandler(stream_handler)
    logging.getLogger('SYNTAX').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('SYNTAX').addHandler(stream_handler)
    logging.getLogger('SEMANTIC').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('SEMANTIC').addHandler(stream_handler)
    logging.getLogger('SYNTHESIS').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('SYNTHESIS').addHandler(stream_handler)

    with Compiler(args) as compiler:
      compiler.compile(error_handler)
    
    if args.debug: sys.exit()

    filename = os.path.basename(args.file_path)

    if os.path.isfile(f'{filename}.aux'): os.remove(f'{filename}.aux')
    if os.path.isfile(f'{filename}.log'): os.remove(f'{filename}.log')
    if os.path.isfile(f'{filename}.tex'): os.remove(f'{filename}.tex')
    if os.path.isfile(f'{filename}.xdv'): os.remove(f'{filename}.xdv')