import errorhandler
import subprocess
import argparse
import logging
import sys
import os

from lexer.Lexer import Lexer

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

    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt='[%(name)s %(levelname)s]: %(message)s'))
    
    logging.getLogger('COMPILER').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('COMPILER').addHandler(stream_handler)
    logging.getLogger('LEXICAL').setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger('LEXICAL').addHandler(stream_handler)

    if not os.path.isfile(f'{args.cv_blueprint_json_filepath}.json'):
      logging.getLogger('COMPILER').critical(f'The path "{args.cv_blueprint_json_filepath}.json" does not point to an existing file.')
      exit()

    logging.getLogger('COMPILER').info(f'Compiling "{args.cv_blueprint_json_filepath}.json" - Generating typesetting markup...')

    with Lexer(f'{args.cv_blueprint_json_filepath}.json') as lex:
        while lex.next() != None:
            pass

    if error_handler.fired: exit()
    
    logging.getLogger('COMPILER').info(f'Compiling "{args.cv_blueprint_json_filepath}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{args.cv_blueprint_json_filepath}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if False:
        logging.getLogger('COMPILER').critical(f'Xelatex failed to generate auxiliary references. See "{args.cv_blueprint_json_filepath}.log".')
        exit()

    logging.getLogger('COMPILER').info(f'Compiling "{args.cv_blueprint_json_filepath}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{args.cv_blueprint_json_filepath}.tex'], stdout=subprocess.DEVNULL)

    if False:
        logging.getLogger('COMPILER').critical(f'Xelatex failed to generate portable document. See "{args.cv_blueprint_json_filepath}.log".')
        exit()
    
    if args.debug: exit()
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.aux'): os.remove(f'{args.cv_blueprint_json_filepath}.aux')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.log'): os.remove(f'{args.cv_blueprint_json_filepath}.log')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.tex'): os.remove(f'{args.cv_blueprint_json_filepath}.tex')