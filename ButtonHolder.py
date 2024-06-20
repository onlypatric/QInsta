from comps import Button
class ButtonHolder:
    start:Button
    pause:Button
    stop:Button
    export:Button
    logout:Button
    skipNextUser:Button
    skipNext10Users:Button
    def __init__(self, start:Button, pause:Button, stop:Button, export:Button, logout:Button, skipNextUser:Button, skipNext10Users:Button):
        self.start = start
        self.pause = pause
        self.stop = stop
        self.export = export
        self.logout = logout
        self.skipNextUser = skipNextUser
        self.skipNext10Users = skipNext10Users
    def enableAll(self):
        self.start.enabled(True).update()
        self.pause.enabled(True).update()
        self.stop.enabled(True).update()
        self.export.enabled(True).update()
        self.logout.enabled(True).update()
        self.skipNextUser.enabled(True).update()
        self.skipNext10Users.enabled(True).update()
    def disableAll(self):
        self.start.enabled(False).update()
        self.pause.enabled(False).update()
        self.stop.enabled(False).update()
        self.export.enabled(False).update()
        self.logout.enabled(False).update()
        self.skipNextUser.enabled(False).update()
        self.skipNext10Users.enabled(False).update()