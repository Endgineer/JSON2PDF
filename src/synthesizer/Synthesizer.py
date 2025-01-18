from compiler.logger.PhaseLogger import PhaseLogger
from synthesizer.components.SynthesizerContext import SynthesizerContext

from semanter.Semanter import Semanter
from compiler.components.Flags import Flags

class Synthesizer:
  synthesizer_ctx: SynthesizerContext

  def __init__(self, semanter: Semanter, flags: Flags, logger: PhaseLogger):
    self.synthesizer_ctx = SynthesizerContext(semanter, flags, logger)
  
  def synthesize(self, anonymize: bool, bolded: bool) -> None:
    self.synthesizer_ctx.build()

    self.synthesizer_ctx.invocations(anonymize, bolded)

    self.synthesizer_ctx.dictify()