from synthesizer.components.SynthesizerContext import SynthesizerContext

from semanter.Semanter import Semanter

class Synthesizer:
  synthesizer_ctx: SynthesizerContext

  def __init__(self, semanter: Semanter):
    self.synthesizer_ctx = SynthesizerContext(semanter)
  
  def synthesize(self, anonymize: bool) -> None:
    self.synthesizer_ctx.build()

    self.synthesizer_ctx.invocations(anonymize)

    self.synthesizer_ctx.dictify()