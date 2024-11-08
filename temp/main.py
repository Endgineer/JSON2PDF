import argparse

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser()

  arg_parser.add_argument('json', type=str)
  arg_parser.add_argument('--update', action=argparse.BooleanOptionalAction, default=False)

  arg_parser.add_argument('-n', '--name', type=str, default=None)
  arg_parser.add_argument('-p', '--position', nargs='*', type=str, default=None)
  arg_parser.add_argument('-a', '--address', type=str, default=None)
  arg_parser.add_argument('-m', '--mobile', type=str, default=None)
  arg_parser.add_argument('-e', '--email', type=str, default=None)
  arg_parser.add_argument('-l', '--linkedin', type=str, default=None)
  arg_parser.add_argument('-g', '--github', type=str, default=None)
  arg_parser.add_argument('-c', '--color', type=str, default=None)
  arg_parser.add_argument('-w', '--website', type=str, default=None)
  
  arg_parser.add_argument('--header', action=argparse.BooleanOptionalAction, default=True)
  arg_parser.add_argument('--footer', action=argparse.BooleanOptionalAction, default=True)
  
  arg_parser.add_argument('--spaced', action=argparse.BooleanOptionalAction, default=True)
  arg_parser.add_argument('--darken', action=argparse.BooleanOptionalAction, default=True)

  arg_parser.add_argument('--anon', action=argparse.BooleanOptionalAction, default=False)
  arg_parser.add_argument('--bold', action=argparse.BooleanOptionalAction, default=False)
  
  arg_parser.add_argument('--debug', action=argparse.BooleanOptionalAction, default=False)
  arg_parser.add_argument('--abort', action=argparse.BooleanOptionalAction, default=False)
  
  args = arg_parser.parse_args()
