import subprocess
import logging
import os

from lexer.Lexer import Lexer

class Compiler():
  file_path: str
  lexer: Lexer
  
  def __init__(self, file_path):
    if not os.path.isfile(f'{file_path}.json'):
      logging.getLogger('COMPILER').critical(f'The path "{file_path}.json" does not point to an existing file.')
      exit()
    
    self.file_path = file_path
    self.lexer = Lexer(f'{self.file_path}.json').__enter__()

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.lexer.__exit__(None, None, None)

  def compile(self) -> None:
    logging.getLogger('COMPILER').info(f'Compiling "{self.file_path}.json" - Generating typesetting markup...')

    while self.lexer.next() != None:
      pass

    if not os.path.isfile(f'{self.file_path}.tex'): exit()
    
    logging.getLogger('COMPILER').info(f'Compiling "{self.file_path}.json" - Generating auxiliary references...')
    subprocess.call([f'xelatex', '-halt-on-error', '-no-pdf', f'{self.file_path}.tex'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.file_path}.pdf'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate auxiliary references. See "{self.file_path}.log".')
      exit()

    logging.getLogger('COMPILER').info(f'Compiling "{self.file_path}.json" - Generating portable document...')
    subprocess.call([f'xelatex', '-halt-on-error', f'{self.file_path}.tex'], stdout=subprocess.DEVNULL)

    if not os.path.isfile(f'{self.file_path}.pdf'):
      logging.getLogger('COMPILER').critical(f'Xelatex failed to generate portable document. See "{self.file_path}.log".')
      exit()