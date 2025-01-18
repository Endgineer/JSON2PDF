import logging
import pathlib
import enum

class Phase(enum.Enum):
  COMPILE = 0
  LEXICAL = 1
  SYNTAX = 2
  SEMANTIC = 3
  LINK = 4
  SYNTHESIS = 5

class Document(enum.Enum):
  CV = 0
  CL = 1

class PhaseLogger:
  abort: list[bool]
  loggers: list[logging.Logger]

  def __init__(self, path: str, abort: bool, debug: bool) -> None:
    self.abort = list()
    for _ in Document:
      self.abort.append(abort)

    handler = logging.FileHandler(pathlib.Path(pathlib.Path(path).name).with_suffix('.dbg.log'), 'w', 'utf-8') if debug else logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(name)s %(levelname)s]: %(message)s'))

    self.loggers = list()
    for phase in Phase:
      self.loggers.append(logging.getLogger(phase.name))
      self.loggers[-1].setLevel(logging.DEBUG if debug else logging.INFO)
      self.loggers[-1].addHandler(handler)

  def __enter__(self):
    return self

  def __exit__(self, exception_type, exception_value, exception_traceback):
    for logger in self.loggers:
      for handler in logger.handlers:
        handler.close()
      logger.handlers.clear()
    logging.shutdown()

  def log(self, document: Document | None, phase: Phase, level: int, message: str) -> None:
    if level >= logging.ERROR:
      if document is None:
        for i in range(len(self.abort)):
          self.abort[i] = True
      else:
        self.abort[document.value] = True
    self.loggers[phase.value].log(level, message)
