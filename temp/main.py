from boot.ArgParser import ArgParser
from boot.PhaseLogger import PhaseLogger

if __name__ == '__main__':
  args = ArgParser()
  logger = PhaseLogger(args.json, args.abort, args.debug)
