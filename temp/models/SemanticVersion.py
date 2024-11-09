class SemanticVersion:
  major: int
  minor: int
  patch: int

  def __init__(self, version: str) -> None:
    major, minor, patch = version.split('.')
    self.major = int(major)
    self.minor = int(minor)
    self.patch = int(patch)
  
  def is_older_than(self, version: str) -> bool:
    other = SemanticVersion(version)
    return other.major > self.major or other.minor > self.minor or other.patch > self.patch
