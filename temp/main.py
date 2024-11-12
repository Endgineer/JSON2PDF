from boot.ArgParser import ArgParser
from boot.PhaseLogger import PhaseLogger

if __name__ == '__main__':
  args = ArgParser('5.0.0')
  with PhaseLogger(args.json_path, args.abort, args.debug) as logger:
    pass
