class SemanticVersion:
  major: int
  minor: int
  patch: int

  def __init__(self, version: str) -> None:
    self.major, self.minor, self.patch = map(int, version.split('.'))
  
  def as_tuple(self) -> tuple[int, int, int]:
    return (self.major, self.minor, self.patch)
  
  def is_older_than(self, version: str) -> bool:
    return self.as_tuple() < SemanticVersion(version).as_tuple()
