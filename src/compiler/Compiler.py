import subprocess
import logging
import os

from compiler.components.Flags import Flags
from compiler.logger.PhaseLogger import *
from lexer.Lexer import Lexer
from parser.Parser import Parser
from semanter.Semanter import Semanter
from synthesizer.Synthesizer import Synthesizer
from parser.constants.grammar import *

class Compiler():
  flags: Flags
  lexer: Lexer
  parser: Parser
  semanter: Semanter
  synthesizer: Synthesizer

  def __init__(self, args):
    self.flags = Flags(args)
    self.lexer = None
    self.parser = None
    self.semanter = None
    self.synthesizer = None

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def compile(self, args) -> None:
    phase_logger = PhaseLogger(args.path, args.abort, args.debug)
    
    phase_logger.log(None, Phase.COMPILE, logging.INFO, f'Compiling "{self.flags.filename}.json" - Generating typesetting markup...')

    self.lexer = Lexer(f'{self.flags.filepath}.json', phase_logger)
    self.parser = Parser(self.lexer, phase_logger)
    self.semanter = Semanter(self.parser, self.flags, phase_logger)
    self.synthesizer = Synthesizer(self.semanter, self.flags, phase_logger)

    self.synthesizer.synthesize(self.flags.anonymize, self.flags.bolded)

    if all(phase_logger.abort):
      phase_logger.log(None, Phase.COMPILE, logging.CRITICAL, f'Compiling "{self.flags.filename}.json" - INTERRUPT')

    if any(phase_logger.abort): return

    with open(f'{self.flags.filename}.tex', 'w', encoding='utf-8') as file:
      file.write(self.flags.wrap(self.synthesizer.synthesizer_ctx))
    
    phase_logger.log(None, Phase.COMPILE, logging.INFO, f'Compiling "{self.flags.filename}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.xdv'):
      phase_logger.log(None, Phase.COMPILE, logging.CRITICAL, f'Xelatex failed to generate auxiliary references. See "{self.flags.filename}.log".')
      return

    phase_logger.log(None, Phase.COMPILE, logging.INFO, f'Compiling "{self.flags.filename}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.pdf'):
      phase_logger.log(None, Phase.COMPILE, logging.CRITICAL, f'Xelatex failed to generate portable document. See "{self.flags.filename}.log".')
      return