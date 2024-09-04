from comps import Button
class ButtonHolder:
    start:Button
    stop:Button
    export:Button
    logout:Button
    skipNextUser:Button
    skipNext10Users:Button
    def __init__(self, start:Button, stop:Button, export:Button, logout:Button):
        self.start = start
        self.stop = stop
        self.export = export
        self.logout = logout
    def enableAll(self):
        self.start.enabled(False).update()
        self.stop.enabled(True).update()
        self.export.enabled(False).update()
        self.logout.enabled(True).update()
    def disableAll(self):
        self.start.enabled(True).update()
        self.stop.enabled(False).update()
        self.export.enabled(False).update()
        self.logout.enabled(False).update()