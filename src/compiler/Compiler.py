import errorhandler
import subprocess
import logging
import sys
import os

from compiler.components.Flags import Flags
from lexer.Lexer import Lexer

class Compiler():
  flags: Flags
  lexer: Lexer

  def __init__(self, args):
    if not os.path.isfile(f'{args.file_path}.json'):
      logging.getLogger('COMPILER').critical(f'The path "{args.file_path}.json" does not point to an existing file.')
      sys.exit()
    
    self.flags = Flags(args)
    self.lexer = Lexer(f'{self.flags.file_path}.json').__enter__()

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.lexer.__exit__(None, None, None)

  def compile(self, error_handler: errorhandler.ErrorHandler) -> None:
    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.file_path}.json" - Generating typesetting markup...')

    while self.lexer.next() != None:
      pass

    if error_handler.fired: sys.exit()

    with open(f'{self.flags.file_path}.tex', 'w') as file:
      file.write(self.flags.wrap('decorated abstract syntax tree repr goes here'))
    
    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.file_path}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{self.flags.file_path}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.file_path}.xdv'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate auxiliary references. See "{self.flags.file_path}.log".')
      sys.exit()

    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.file_path}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{self.flags.file_path}.tex'], stdout=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.flags.file_path}.pdf'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate portable document. See "{self.flags.file_path}.log".')
      sys.exit()