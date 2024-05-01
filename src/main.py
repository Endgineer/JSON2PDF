import errorhandler
import argparse
import logging
import sys
import os

from compiler.Compiler import Compiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='file_path', type=str)
    parser.add_argument('-n', '--name', type=str, default=None)
    parser.add_argument('-p', '--position', nargs='*', type=str, default=None)
    parser.add_argument('-a', '--address', type=str, default=None)
    parser.add_argument('-m', '--mobile', type=str, default=None)
    parser.add_argument('-e', '--email', type=str, default=None)
    parser.add_argument('-l', '--linkedin', type=str, default=None)
    parser.add_argument('-g', '--github', type=str, default=None)
    parser.add_argument('-c', '--color', type=str, default=None)
    parser.add_argument('-w', '--website', type=str, default=None)
    parser.add_argument('--footer', action=argparse.BooleanOptionalAction)
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

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

    with Compiler(args) as compiler:
      compiler.compile(error_handler)
    
    if args.debug: sys.exit()
    if os.path.isfile(f'{args.file_path}.aux'): os.remove(f'{args.file_path}.aux')
    if os.path.isfile(f'{args.file_path}.log'): os.remove(f'{args.file_path}.log')
    if os.path.isfile(f'{args.file_path}.tex'): os.remove(f'{args.file_path}.tex')
    if os.path.isfile(f'{args.file_path}.xdv'): os.remove(f'{args.file_path}.xdv')