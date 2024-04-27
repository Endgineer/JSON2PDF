import errorhandler
import subprocess
import argparse
import logging
import sys
import os

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
    parser.add_argument('--footer', action=argparse.BooleanOptionalAction)
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logger = logging.getLogger()
    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt='[%(levelname)s]: %(message)s'))
    logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
    logger.addHandler(stream_handler)

    if error_handler.fired: exit()
    subprocess.call([f'xelatex', f'{args.cv_blueprint_json_filepath}.tex'])
    subprocess.call([f'xelatex', f'{args.cv_blueprint_json_filepath}.tex'])
    
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.aux'): os.remove(f'{args.cv_blueprint_json_filepath}.aux')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.log'): os.remove(f'{args.cv_blueprint_json_filepath}.log')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.tex'): os.remove(f'{args.cv_blueprint_json_filepath}.tex')