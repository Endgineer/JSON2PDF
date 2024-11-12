from boot.ArgParser import ArgParser
from boot.PhaseLogger import PhaseLogger
from objects.TexDocument import TexDocument

class CompileManager:
  argparser: ArgParser
  phaselogger: PhaseLogger
  texdocuments: list[TexDocument]

  def __init__(self, argparser: ArgParser, phaselogger: PhaseLogger) -> None:
    dbglog_path = argparser.json_path.with_suffix('.dbg.log')
    if not argparser.debug:
      dbglog_path.unlink(True)
    
    self.texdocuments = list()

    #! BODY OCCURS HERE

    if not argparser.debug:
      for texdoc in self.texdocuments:
        argparser.json_path.with_suffix(f'.{texdoc.identifier.name}.aux').unlink(True)
        argparser.json_path.with_suffix(f'.{texdoc.identifier.name}.log').unlink(True)
        argparser.json_path.with_suffix(f'.{texdoc.identifier.name}.tex').unlink(True)
        argparser.json_path.with_suffix(f'.{texdoc.identifier.name}.xdv').unlink(True)
