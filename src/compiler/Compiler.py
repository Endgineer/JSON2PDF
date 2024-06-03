import errorhandler
import subprocess
import logging
import sys
import os

from compiler.components.Flags import Flags
from lexer.Lexer import Lexer
from parser.Parser import Parser
from semanter.Semanter import Semanter
from synthesizer.Synthesizer import Synthesizer

class Compiler():
  flags: Flags
  lexer: Lexer
  parser: Parser
  semanter: Semanter
  synthesizer: Synthesizer

  def __init__(self, args):
    if not os.path.isfile(f'{args.file_path}.json'):
      logging.getLogger('COMPILER').critical(f'The path "{args.file_path}.json" does not point to an existing file.')
      sys.exit()
    
    self.flags = Flags(args)
    self.lexer = None
    self.parser = None
    self.semanter = None
    self.synthesizer = None

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def compile(self, error_handler: errorhandler.ErrorHandler, test_mode: bool = False) -> None:
    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.filename}.json" - Generating typesetting markup...')

    self.lexer = Lexer(f'{self.flags.filepath}.json')
    self.parser = Parser(self.lexer)
    self.semanter = Semanter(self.parser)
    self.synthesizer = Synthesizer(self.semanter)

    self.synthesizer.synthesize(self.flags.anonymize)

    if error_handler.fired or test_mode: sys.exit()

    with open(f'{self.flags.filename}.tex', 'w', encoding='utf-8') as file:
      file.write(self.flags.wrap(self.synthesizer.synthesizer_ctx))
    
    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.filename}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.xdv'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate auxiliary references. See "{self.flags.filename}.log".')
      sys.exit()

    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.filename}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.pdf'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate portable document. See "{self.flags.filename}.log".')
      sys.exit()