import pylatex

from semanter.constants.propset import *
from compiler.units.Item import Item

def generate_from_tree(synthesizer_ctx) -> str:
  return ''.join([(
    f'%-------------------------------------------------------------------------------\n'
    f'%\tSECTION TITLE\n'
    f'%-------------------------------------------------------------------------------\n'
    f'\\cvsection{{{pylatex.escape_latex(section)}}}\n'
    f'\n'
    f'\n'
    f'%-------------------------------------------------------------------------------\n'
    f'%\tCONTENT\n'
    f'%-------------------------------------------------------------------------------\n'
    f'\\begin{{{synthesizer_ctx.semanter.semanter_ctx.registry[section].name.lower()}}}\n'
    f'\n'
    f'{generate_from_items(synthesizer_ctx.semanter.semanter_ctx.registry[section], items)}'
    f'\\end{{{synthesizer_ctx.semanter.semanter_ctx.registry[section].name.lower()}}}\n'
    f'\n'
  ) for section, items in synthesizer_ctx.tree.items()])

def generate_from_items(itemlist_type: Item.Kind, items: list[dict[str, str | list[str] | dict[str, str]]]) -> str:
  return ''.join([generate_from_item(itemlist_type, item) for item in items])

def generate_from_item(item_type: Item.Kind, item: dict[str, str | list[str] | dict[str, str]]) -> str:
  match(item_type):
    case Item.Kind.CVPARAGRAPH:
      return (
        f'{pylatex.escape_latex(item[PARAGRAPH]) if PARAGRAPH in item else ""}\n'
        f'\n'
      )
    case Item.Kind.CVSKILLS:
      return (
        f'\\cvskill\n'
        f'\t{{{pylatex.escape_latex(item[CATEGORY]) if CATEGORY in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[CONTENT]) if CONTENT in item else ""}}}\n'
        f'\n'
      )
    case Item.Kind.CVENTRIES:
      return (
        f'\\cventry\n'
        f'\t{{{pylatex.escape_latex(item[SUBTITLE]) if SUBTITLE in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[TITLE]) if TITLE in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[TTAG]) if TTAG in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[BTAG]) if BTAG in item else ""}}}\n'
        f'\t{{{generate_from_points(item[DETAILS]) if DETAILS in item else ""}}}\n'
        f'\n'
      )
    case Item.Kind.CVHONORS:
      return (
        f'\\cvhonor\n'
        f'\t{{{pylatex.escape_latex(item[TITLE]) if TITLE in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[SUBTITLE]) if SUBTITLE in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[RTAG]) if RTAG in item else ""}}}\n'
        f'\t{{{pylatex.escape_latex(item[LTAG]) if LTAG in item else ""}}}\n'
        f'\n'
      )

def generate_from_points(points: list[str]) -> str:
  return "\n\t\t\\begin{cvitems}"+"".join(["\n\t\t\t\\item{"+pylatex.escape_latex(point)+"}" for point in points])+"\n\t\t\\end{cvitems}\n\t"