import errorhandler
import subprocess
import logging
import os

from compiler.components.Flags import Flags
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

  def __init__(self, args, root: Nonterminal):
    assert root.primordial_root

    self.flags = None
    self.lexer = None
    self.parser = None
    self.semanter = None
    self.synthesizer = None
    
    filebasepath = args.cvjson if root is CVROOT else args.cljson
    if not os.path.isfile(f'{filebasepath}.json'):
      logging.getLogger('COMPILER').critical(f'The path "{filebasepath}.json" does not point to an existing file.')
      return
    
    self.flags = Flags(args, root)

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def compile(self, error_handler: errorhandler.ErrorHandler, interrupt: bool = False) -> None:
    if self.flags is None: return
    DOCTYPE = str(self.flags.root)[:2]

    logging.getLogger('COMPILER').info(f'Compiling {DOCTYPE} "{self.flags.filename}.json" - Generating typesetting markup...')

    self.lexer = Lexer(f'{self.flags.filepath}.json')
    self.parser = Parser(self.lexer, self.flags.root)
    self.semanter = Semanter(self.parser, self.flags)
    self.synthesizer = Synthesizer(self.semanter, self.flags)

    self.synthesizer.synthesize(self.flags.anonymize, self.flags.bolded)

    if interrupt:
      logging.getLogger('COMPILER').critical(f'Compiling {DOCTYPE} "{self.flags.filename}.json" - INTERRUPT')

    if error_handler.fired: return

    with open(f'{self.flags.filename}.tex', 'w', encoding='utf-8') as file:
      file.write(self.flags.wrap(self.synthesizer.synthesizer_ctx))
    
    logging.getLogger('COMPILER').info(f'Compiling {DOCTYPE} "{self.flags.filename}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.xdv'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate auxiliary references. See "{self.flags.filename}.log".')
      return

    logging.getLogger('COMPILER').info(f'Compiling {DOCTYPE} "{self.flags.filename}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{self.flags.filename}.tex'], stdout=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.filename}.pdf'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate portable document. See "{self.flags.filename}.log".')
      return