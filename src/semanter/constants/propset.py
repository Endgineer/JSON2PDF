from compiler.units.Item import Item

STRS = { 'paragraph', 'category', 'content', 'title', 'subtitle', 'btag', 'ttag', 'ltag', 'rtag' }
LISTS = { 'details' }
DICTS = { 'labels' }

CVGLOBALS_REQUIRED = set()
CVGLOBALS_OPTIONAL = { 'labels' }

CVPARAGRAPH_REQUIRED = CVGLOBALS_REQUIRED.union({ 'paragraph' })
CVPARAGRAPH_OPTIONAL = CVGLOBALS_OPTIONAL.union(set())
CVPARAGRAPH = set.union(CVPARAGRAPH_REQUIRED, CVPARAGRAPH_OPTIONAL)

CVSKILLS_REQUIRED = CVGLOBALS_REQUIRED.union({ 'category', 'content' })
CVSKILLS_OPTIONAL = CVGLOBALS_OPTIONAL.union(set())
CVSKILLS = set.union(CVSKILLS_REQUIRED, CVSKILLS_OPTIONAL)

CVENTRIES_REQUIRED = CVGLOBALS_REQUIRED.union({ 'title', 'subtitle', 'btag', 'ttag' })
CVENTRIES_OPTIONAL = CVGLOBALS_OPTIONAL.union({ 'details' })
CVENTRIES = set.union(CVENTRIES_REQUIRED, CVENTRIES_OPTIONAL)

CVHONORS_REQUIRED = CVGLOBALS_REQUIRED.union({ 'title', 'subtitle', 'ltag', 'rtag' })
CVHONORS_OPTIONAL = CVGLOBALS_OPTIONAL.union(set())
CVHONORS = set.union(CVHONORS_REQUIRED, CVHONORS_OPTIONAL)

ALL_REQUIRED = set.union(CVPARAGRAPH_REQUIRED, CVSKILLS_REQUIRED, CVENTRIES_REQUIRED, CVHONORS_REQUIRED)
ALL_OPTIONAL = set.union(CVPARAGRAPH_OPTIONAL, CVSKILLS_OPTIONAL, CVENTRIES_OPTIONAL, CVHONORS_OPTIONAL)
ALL = set.union(ALL_REQUIRED, ALL_OPTIONAL)

def prop_similarity_coefficients(props: set[str]) -> dict[Item.Kind, float]:
  '''
  Returns the Jaccard similarity coefficient of the 'props' set against each prop set type. A perfect similarity with a set type implies that 'props':
  \n* Contains all required props of that set type
  \n* May or may not contain any optional props of that set type
  \n* Does not contain any other prop irrelevant to that set type
  '''
  return {
    Item.Kind.CVPARAGRAPH: float(len(CVPARAGRAPH_REQUIRED.intersection(props - CVPARAGRAPH_OPTIONAL))) / float(len(CVPARAGRAPH_REQUIRED.union(props - CVPARAGRAPH_OPTIONAL))),
    Item.Kind.CVSKILL: float(len(CVSKILLS_REQUIRED.intersection(props - CVSKILLS_OPTIONAL))) / float(len(CVSKILLS_REQUIRED.union(props - CVSKILLS_OPTIONAL))),
    Item.Kind.CVENTRY: float(len(CVENTRIES_REQUIRED.intersection(props - CVENTRIES_OPTIONAL))) / float(len(CVENTRIES_REQUIRED.union(props - CVENTRIES_OPTIONAL))),
    Item.Kind.CVHONOR: float(len(CVHONORS_REQUIRED.intersection(props - CVHONORS_OPTIONAL))) / float(len(CVHONORS_REQUIRED.union(props - CVHONORS_OPTIONAL))),
  }