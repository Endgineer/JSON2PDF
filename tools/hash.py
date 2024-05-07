import argparse
import hashlib

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(dest='exe_path', type=str)
  args = parser.parse_args()

  with open(f'{args.exe_path}.exe', 'rb') as file:
    print(hashlib.sha512(file.read()).hexdigest())