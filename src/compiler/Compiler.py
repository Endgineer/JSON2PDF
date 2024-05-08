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
    self.lexer = None

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def compile(self, error_handler: errorhandler.ErrorHandler) -> None:
    logging.getLogger('COMPILER').info(f'Compiling "{self.flags.filename}.json" - Generating typesetting markup...')

    self.lexer = Lexer(f'{self.flags.filepath}.json')

    while self.lexer.scan() != None: pass

    if error_handler.fired: sys.exit()

    with open(f'{self.flags.filename}.tex', 'w') as file:
      file.write(self.flags.wrap(''))
    
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