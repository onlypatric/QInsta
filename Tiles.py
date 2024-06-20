from typing import Self
from comps import *
from comps.Elements import Style

class Tile(Vertical):
    def __init__(self, title: str):
        super().__init__()
        self.counter = 0
        self.set_style(Style().backgroundColor("#a69567").borderRadius(
            "10px").margin("5px"))
        self.title = Heading(title).align(Qt.AlignmentFlag.AlignCenter).set_style(
            Heading.Type.H4.value.padding("5px"))
        self.counter_label = Heading("0").align(
            Qt.AlignmentFlag.AlignCenter).set_style(Heading.Type.H2.value.padding("5px"))
        self.add(self.title, self.counter_label).expandMin().id(title)

    def increment(self) -> Self:
        self.counter += 1
        self.counter_label.set(str(self.counter))
        return self
    inc = increment

    def set(self, value) -> Self:
        self.counter = value
        self.counter_label.set(str(self.counter))
        return self

    def get(self):
        return self.counter


class MiniTile(Tile):
    def __init__(self, title: str):
        super().__init__(title)
        self.title.set_style(Heading.Type.H5.value.padding("5px"))
        self.counter_label.set_style(
            Heading.Type.H3.value.fontWeight("bold").padding("5px"))


class StringTile(Vertical):
    def __init__(self, title: str):
        super().__init__()
        self.set_style(Style().backgroundColor("#a69567").borderRadius(
            "10px").margin("5px"))
        self.title = Heading(title).align(Qt.AlignmentFlag.AlignCenter).set_style(
            Heading.Type.H4.value.padding("5px"))
        self.counter_label = Heading("").align(
            Qt.AlignmentFlag.AlignCenter).set_style(Heading.Type.H2.value.padding("5px"))
        self.add(self.title, self.counter_label).expandMin()

    def set(self, value) -> Self:
        self.counter_label.set(value)
        return self

    def get(self):
        return self.counter_label.text()


class TileObtainer:
    def obtainInt(id: str) -> Tile:
        return Finder.get(id)

    def obtainStr(id: str) -> StringTile:
        return Finder.get(id)
