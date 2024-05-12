import typing

from compiler.units.Token import Token

T = typing.TypeVar('T')
U = typing.TypeVar('U')

class SyntacticTypes:
  TupleList = list[tuple[T, U]]
  StringToken = Token
  StringTokenPair = tuple[StringToken, StringToken]
  StringTokensList = list[StringToken]
  ItemProperty = tuple[StringToken, StringToken | StringTokensList | TupleList[StringToken, StringToken]]
  Item = list[ItemProperty]
  RefOrItem = StringToken | Item
  Section = tuple[StringToken, list[RefOrItem]]
  ReferencedItem = tuple[StringToken, Item]
  ReferencedItemsList = list[ReferencedItem]
  SectionsList = list[Section]