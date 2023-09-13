import subprocess
import argparse
import json

from src.AwesomeCVTexGenerator import AwesomeCVTexGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='cv_blueprint_json_filepath', type=str)
    parser.add_argument('-n', '--name', type=str, default=None)
    parser.add_argument('-p', '--position', type=str, default=None)
    parser.add_argument('-a', '--address', type=str, default=None)
    parser.add_argument('-m', '--mobile', type=str, default=None)
    parser.add_argument('-e', '--email', type=str, default=None)
    parser.add_argument('-l', '--linkedin', type=str, default=None)
    args = parser.parse_args()

    with open(args.cv_blueprint_json_filepath) as cv:
        cv = json.load(cv)
    
    AwesomeCVTexGenerator.generate_cv(cv, args)

    process = subprocess.Popen('cmd /k "xelatex '+args.cv_blueprint_json_filepath.replace('.json', '.tex'), cwd='tex')
    process.wait()