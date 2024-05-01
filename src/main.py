import argparse
import logging
import sys
import os

from compiler.Compiler import Compiler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='cv_blueprint_json_filepath', type=str)
    parser.add_argument('-n', '--name', type=str, default=None)
    parser.add_argument('-p', '--position', type=str, default=None)
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

    with Compiler(f'{args.cv_blueprint_json_filepath}') as compiler:
      compiler.compile()
    
    if args.debug: exit()
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.aux'): os.remove(f'{args.cv_blueprint_json_filepath}.aux')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.log'): os.remove(f'{args.cv_blueprint_json_filepath}.log')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.tex'): os.remove(f'{args.cv_blueprint_json_filepath}.tex')