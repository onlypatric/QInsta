from datetime import datetime
from enum import Enum
from PyQt6.QtWidgets import QMessageBox
from comps import *
from comps.Elements import Style
class ConsoleList(Vertical):
    col = {
        0: "#0366fc",
        1: "#82ab67",
        2: "#a69567",
        3: "#c94242",
        4: "#cf48b4",
        5: ""
    }
    class Type(Enum):
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        CRITICAL = 4
        ANY = 5

    def __init__(self,minLevel:int=1):
        super().__init__()
        self.console_list_widget = ListWidget()
        self.add(self.console_list_widget)
        self.minLevel = minLevel

    def emit(self, message: str, type: "ConsoleList.Type" = Type.INFO, dt: bool = True):
        #if self.minLevel < type.value:
        #    return self
        if self.console_list_widget.count() > 49:
            self.console_list_widget.remove(0)
        self.console_list_widget.add(
            Horizontal(
                Text(message).wrap(True),
                Spacer(),
                Text(
                    type.name+" at "+datetime.now().strftime("%T") if dt else ""
                ).set_style(
                    Style()
                    .fontFamily("Courier New")
                    .fontWeight("bold")
                )
            ).set_style(
                Style().backgroundColor(self.col[type.value])
            )
        )
        self.console_list_widget.update()
        if type == ConsoleList.Type.CRITICAL:
            QMessageBox.critical(self, "Critical error", message)
        return self
    def clear(self):
        self.console_list_widget.clear()
        return self