import subprocess
import argparse
from ruamel.yaml import YAML
import os

from src.sanitizer.cv_sanitizer import sanitize_cv
from src.generator.cv_generator import generate_cv

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
    args = parser.parse_args()

    with open(f'{args.cv_blueprint_json_filepath}.yaml') as file:
        yaml_parser = YAML(typ='safe')
        cv = yaml_parser.load(file)
    
    cv, errors = sanitize_cv(cv)
    if errors: print('\n'.join(errors))
    elif not [error for error in errors if 'ERROR' in error]:
        generate_cv(cv, args)
        process = subprocess.call([f'xelatex', f'{args.cv_blueprint_json_filepath}.tex'])
        process = subprocess.call([f'xelatex', f'{args.cv_blueprint_json_filepath}.tex'])
    
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.aux'): os.remove(f'{args.cv_blueprint_json_filepath}.aux')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.log'): os.remove(f'{args.cv_blueprint_json_filepath}.log')
    if os.path.isfile(f'{args.cv_blueprint_json_filepath}.tex'): os.remove(f'{args.cv_blueprint_json_filepath}.tex')