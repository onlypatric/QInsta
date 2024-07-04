from comps.Elements import Finder
from extracomps.Tiles import StringTile, Tile
from extracomps.ConsoleList import ConsoleList

class ConsoleWriter:
    def any(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.ANY).update()
    def debug(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.DEBUG).update()

    def info(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.INFO).update()

    def warning(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.WARNING).update()

    def error(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.ERROR).update()

    def critical(message: str):
        Finder.get("q-console").emit(message, ConsoleList.Type.CRITICAL).update()
    
    def clear():
        Finder.get("q-console").clear()
class Incrementer:
    totalInt: "Tile"
    accountInt: "Tile"
    currUser: "StringTile"
    dms: "Tile"
    comments: "Tile"
    likes: "Tile"
    follows: "Tile"
    banned:"Tile"
    blocked:"Tile"
    successful:"Tile"
    def __init__(self) -> None:
        self.totalInt=Finder.get("Total")
        self.accountInt=Finder.get("Logins")
        self.currUser = Finder.get("Account")
        self.dms = Finder.get("DMs")
        self.comments = Finder.get("Comments")
        self.likes = Finder.get("Likes")
        self.follows = Finder.get("Follows")
        self.banned = Finder.get("Banned")
        self.blocked = Finder.get("Blocked")
        self.successful = Finder.get("Successful")
    def newAccount(self):
        self.accountInt.set(0)
        self.currUser.set("")
    def resetAll(self):
        self.totalInt.set(0)
        self.accountInt.set(0)
        self.currUser.set("")
        self.dms.set(0)
        self.comments.set(0)
        self.likes.set(0)
        self.follows.set(0)
        self.banned.set(0)
        self.blocked.set(0)
        self.successful.set(0)
    def interactions(self):
        self.totalInt.inc()
        self.accountInt.inc()
    def dm(self):
        self.dms.inc()
    def comment(self):
        self.comments.inc()
    def like(self):
        self.likes.inc()
    def follow(self):
        self.follows.inc()
    def ban(self):
        self.banned.inc()
    def block(self):
        self.blocked.inc()
    def success(self):
        self.successful.inc()