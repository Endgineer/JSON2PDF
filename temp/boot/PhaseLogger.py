import logging
import pathlib

from enums.Phase import Phase
from enums.Document import Document

class PhaseLogger:
  abort: list[bool]
  loggers: list[logging.Logger]

  def __init__(self, jsonpath: pathlib.Path, abort: bool, debug: bool) -> None:
    self.abort = list()
    for _ in Document:
      self.abort.append(abort)
    
    handler = logging.FileHandler(filename=f'{jsonpath.with_suffix(".dbg.log")}', encoding='utf-8') if debug else logging.StreamHandler()
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
        logger.removeHandler(handler)
    logging.shutdown()
  
  def log(self, document: Document, phase: Phase, level: int, message: str) -> None:
    if level >= logging.ERROR:
      self.abort[document.value] = True
    self.loggers[phase.value].log(level, message)
  
  def cv_compile_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.COMPILE, logging.DEBUG, message)

  def cv_compile_info(self, message: str) -> None:
    self.log(Document.CV, Phase.COMPILE, logging.INFO, message)

  def cv_compile_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.COMPILE, logging.WARN, message)

  def cv_compile_error(self, message: str) -> None:
    self.log(Document.CV, Phase.COMPILE, logging.ERROR, message)

  def cv_compile_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.COMPILE, logging.CRITICAL, message)

  def cv_lexical_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.LEXICAL, logging.DEBUG, message)

  def cv_lexical_info(self, message: str) -> None:
    self.log(Document.CV, Phase.LEXICAL, logging.INFO, message)

  def cv_lexical_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.LEXICAL, logging.WARN, message)

  def cv_lexical_error(self, message: str) -> None:
    self.log(Document.CV, Phase.LEXICAL, logging.ERROR, message)

  def cv_lexical_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.LEXICAL, logging.CRITICAL, message)

  def cv_syntax_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTAX, logging.DEBUG, message)

  def cv_syntax_info(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTAX, logging.INFO, message)

  def cv_syntax_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTAX, logging.WARN, message)

  def cv_syntax_error(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTAX, logging.ERROR, message)

  def cv_syntax_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTAX, logging.CRITICAL, message)

  def cv_semantic_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.SEMANTIC, logging.DEBUG, message)

  def cv_semantic_info(self, message: str) -> None:
    self.log(Document.CV, Phase.SEMANTIC, logging.INFO, message)

  def cv_semantic_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.SEMANTIC, logging.WARN, message)

  def cv_semantic_error(self, message: str) -> None:
    self.log(Document.CV, Phase.SEMANTIC, logging.ERROR, message)

  def cv_semantic_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.SEMANTIC, logging.CRITICAL, message)

  def cv_linking_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.LINKING, logging.DEBUG, message)

  def cv_linking_info(self, message: str) -> None:
    self.log(Document.CV, Phase.LINKING, logging.INFO, message)

  def cv_linking_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.LINKING, logging.WARN, message)

  def cv_linking_error(self, message: str) -> None:
    self.log(Document.CV, Phase.LINKING, logging.ERROR, message)

  def cv_linking_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.LINKING, logging.CRITICAL, message)

  def cv_synthesis_debug(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTHESIS, logging.DEBUG, message)

  def cv_synthesis_info(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTHESIS, logging.INFO, message)

  def cv_synthesis_warn(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTHESIS, logging.WARN, message)

  def cv_synthesis_error(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTHESIS, logging.ERROR, message)

  def cv_synthesis_critical(self, message: str) -> None:
    self.log(Document.CV, Phase.SYNTHESIS, logging.CRITICAL, message)

  def cl_compile_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.COMPILE, logging.DEBUG, message)

  def cl_compile_info(self, message: str) -> None:
    self.log(Document.CL, Phase.COMPILE, logging.INFO, message)

  def cl_compile_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.COMPILE, logging.WARN, message)

  def cl_compile_error(self, message: str) -> None:
    self.log(Document.CL, Phase.COMPILE, logging.ERROR, message)

  def cl_compile_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.COMPILE, logging.CRITICAL, message)

  def cl_lexical_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.LEXICAL, logging.DEBUG, message)

  def cl_lexical_info(self, message: str) -> None:
    self.log(Document.CL, Phase.LEXICAL, logging.INFO, message)

  def cl_lexical_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.LEXICAL, logging.WARN, message)

  def cl_lexical_error(self, message: str) -> None:
    self.log(Document.CL, Phase.LEXICAL, logging.ERROR, message)

  def cl_lexical_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.LEXICAL, logging.CRITICAL, message)

  def cl_syntax_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTAX, logging.DEBUG, message)

  def cl_syntax_info(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTAX, logging.INFO, message)

  def cl_syntax_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTAX, logging.WARN, message)

  def cl_syntax_error(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTAX, logging.ERROR, message)

  def cl_syntax_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTAX, logging.CRITICAL, message)

  def cl_semantic_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.SEMANTIC, logging.DEBUG, message)

  def cl_semantic_info(self, message: str) -> None:
    self.log(Document.CL, Phase.SEMANTIC, logging.INFO, message)

  def cl_semantic_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.SEMANTIC, logging.WARN, message)

  def cl_semantic_error(self, message: str) -> None:
    self.log(Document.CL, Phase.SEMANTIC, logging.ERROR, message)

  def cl_semantic_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.SEMANTIC, logging.CRITICAL, message)

  def cl_linking_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.LINKING, logging.DEBUG, message)

  def cl_linking_info(self, message: str) -> None:
    self.log(Document.CL, Phase.LINKING, logging.INFO, message)

  def cl_linking_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.LINKING, logging.WARN, message)

  def cl_linking_error(self, message: str) -> None:
    self.log(Document.CL, Phase.LINKING, logging.ERROR, message)

  def cl_linking_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.LINKING, logging.CRITICAL, message)

  def cl_synthesis_debug(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTHESIS, logging.DEBUG, message)

  def cl_synthesis_info(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTHESIS, logging.INFO, message)

  def cl_synthesis_warn(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTHESIS, logging.WARN, message)

  def cl_synthesis_error(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTHESIS, logging.ERROR, message)

  def cl_synthesis_critical(self, message: str) -> None:
    self.log(Document.CL, Phase.SYNTHESIS, logging.CRITICAL, message)
