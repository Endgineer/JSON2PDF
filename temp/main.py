from boot.ArgParser import ArgParser
from boot.PhaseLogger import PhaseLogger

if __name__ == '__main__':
  args = ArgParser('5.0.0')
  logger = PhaseLogger(args.json, args.abort, args.debug)
