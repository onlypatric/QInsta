from appdirs import user_data_dir

from datetime import datetime
import os
from uuid import getnode
from typing import Dict, List, Tuple,Union
from extracomps.ButtonHolder import ButtonHolder
from extracomps.Tiles import StringTile, Tile, MiniTile
from comps import *
from extracomps.ConsoleList import ConsoleList
from PyQt6.QtWidgets import QApplication, QStyleFactory, QAbstractItemView, QMessageBox,QInputDialog
from PyQt6.QtGui import QIntValidator
import sys
import json
from utils.ExtractionParams import ExtractionParams, TargetType
from utils.configLoader import open_config
import re
from extracomps.ConsoleWriter import ConsoleWriter, Incrementer
from utils.instaProcess import ExtractorCore, InstaProcess, License
def obtain_unique_code() -> str:
    return hex(getnode()).upper()
def matchTo(selection:int, values:List|Tuple) -> str:
    if selection >= len(values):
        return ""
    return values[selection]
class FormField(Vertical):
    def __init__(self, label:str,oftype=int):
        super().__init__()
        self.field = Field()
        if oftype==int:
            self.field.setValidator(QIntValidator())
        self.oftype=oftype
        self.add(Text(label,Text.Type.P3),self.field)
    def get(self) -> str:
        if self.oftype==int:
            if self.field.text()=="":
                return 0
            return int(self.field.text())
        return self.field.text()
    def set(self, value:str):
        self.field.set(value)
class ListBox(Vertical):
    def __init__(self,title:str="",on_add:Callable[[ListWidget],None]|None=None):
        super().__init__()
        self.set_name("ListBox")
        self.list = ListWidget()
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.add(GroupBox(
            (
                self.list,
                [Button("Open").action(self.open),Button("Export").action(self.export),Spacer(),Button("+").action(lambda:on_add(self.list) if on_add is not None else None),Button("-")]
            ),
            title
        ).expand(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    def open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All Files (*)")
        if path and os.path.isfile(path) or os.path.islink(path):
            with open(path, "r") as file:
                for line in file:
                    self.list.add(line.strip())
    def get(self) -> List[str]:
        return [self.list.item(i).text() for i in range(self.list.count())]
    def set(self, values:List[str]):
        self.list.clear()
        for value in values:
            self.list.add(value)
    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Select destination", "", "Plain text file (*.txt);;All files (*.*)")
        if path:
            with open(path, "w") as file:
                for index in range(self.list.count()):
                    item = self.list.item(index)
                    if item is not None:
                        file.write(item.text()+"\n")

class SendingValidator(Vertical):
    def __init__(self,text:str) -> None:
        super().__init__()
        self.set_name("SendingValidator")
        self.frequency  = SpinBox().minV(1).maxV(1000000)
        self.min1       = SpinBox().minV(0).maxV(1000000)
        self.max1       = SpinBox().minV(0).maxV(1000000)
        self.min2       = SpinBox().minV(0).maxV(1000000)
        self.max2       = SpinBox().minV(0).maxV(1000000)
        self.add(GroupBox(
            Horizontal(
                (
                    Text("Frequency ",Text.Type.P3),
                    self.frequency,
                    Text("min followers at", Text.Type.P3),
                    self.min1,
                    Text("max followers at", Text.Type.P3),
                    self.max1,
                    Spacer()
                ),
                (
                    Text("min media count ", Text.Type.P3),
                    self.min2,
                    Text("max media count ", Text.Type.P3),
                    self.max2,
                    Spacer()
                )
            ),
            text
        ))
    def get(self) -> Dict[str,int]:
        return {
            "frequency": self.frequency.value(),
            "minfollowers": self.min1.value(),
            "maxfollowers": self.max1.value(),
            "minmedia": self.min2.value(),
            "maxmedia": self.max2.value()
        }
    def set(self, c:Dict[str,int]):
        self.frequency.setValue(c["frequency"])
        self.min1.setValue(c["minfollowers"])
        self.max1.setValue(c["maxfollowers"])
        self.min2.setValue(c["minmedia"])
        self.max2.setValue(c["maxmedia"])


class Configured:
    def get_conf_dict(self) -> Dict[str,Union[str,int,Dict[str,Union[str,int,dict]]]]:
        text_conf = []
        for text in Finder.get("q-message").get().split("{separator}"):
            if text.startswith("\n"):
                text = text[1:]
            text_conf.append(text)
        text_comm_conf = []
        for text in Finder.get("q-comment").get().split("{separator}"):
            if text.startswith("\n"):
                text = text[1:]
            text_comm_conf.append(text)
        return {
            "user_list": Finder.get("q-currentUserList").get(),
            "parallel": Finder.get("q-parallel").get(),
            "accounts_list": Finder.get("q-currentAccsList").get(),
            "exportType": Finder.get("q-exportType").get(),
            "usersforeachaccount": Finder.get("q-usersforeachaccount").get(),
            "proxies": Finder.get("proxy").get(),
            "message": {
                "enabled": Finder.get("q-enablemsg").get(),
                "text": text_conf,
                "enabled_filters": Finder.get("q-enablemessagefilters").get(),
                "filters": Finder.get("q-messagefilters").get(),
                "timebeforemessage": Finder.get("q-timebeforemessage").get(),
                "timeaftermessage": Finder.get("q-timeaftermessage").get()
            },
            "comment": {
                "enabled": Finder.get("q-enablecomment").get(),
                "text": text_comm_conf,
                "enabled_filters": Finder.get("q-enablecommentfilters").get(),
                "filters": Finder.get("q-commentsfilter").get(),
                "timebeforecomment": Finder.get("q-timebeforecomment").get(),
                "timeaftercomment": Finder.get("q-timeaftercomment").get(),
            },
            "like": {
                "enabled": Finder.get("q-enablelike").get(),
                "enabled_filters": Finder.get("q-enablelike").get(),
                "filters": Finder.get("q-likefilter").get(),
                "timebeforelike": Finder.get("q-timebeforelike").get(),
                "timeafterlike": Finder.get("q-timeafterlike").get()
            },
            "follow": {
                "enabled": Finder.get("q-enablefollow").get(),
                "enabled_filters": Finder.get("q-enablefollow").get(),
                "filters": Finder.get("q-followfilter").get(),
                "timebeforefollow": Finder.get("q-timebeforefollow").get(),
                "timeafterfollow": Finder.get("q-timeafterfollow").get()
            },
            "otherTimings": {
                "loadinguser": {
                    "before": Finder.get("q-timebeforeloadinguser").get(),
                    "after": Finder.get("q-timeafterloadinguser").get()
                },
                "accounttask": {
                    "before": Finder.get("q-timebeforeendingaccounttask").get(),
                    "after": Finder.get("q-timeafterendingaccounttask").get()
                },
                "blockban": {
                    "block": Finder.get("q-timeafterbeingblocked").get(),
                    "ban": Finder.get("q-timeafterbeingbanned").get()
                },
                "logout": {
                    "before": Finder.get("q-timebeforelogout").get(),
                    "after": Finder.get("q-timeafterlogout").get()
                }
            },
            "saveParams": {
                "toJson": Finder.get("q-userDataToJSON").get(),
                "toCSV": Finder.get("q-userDataToCSV").get(),
                "blocks": Finder.get("q-saveBlocksRecord").get(),
                "bans": Finder.get("q-saveBansRecord").get(),
                "twiceAttempt": Finder.get("q-twiceAttempt").get(),
                "askForCode": Finder.get("q-askForCode").get(),
                "saveCookies": Finder.get("q-saveCookies").get(),
                "saveSession": Finder.get("q-saveSession").get()
            },
            "sendingParams": {
                "onlytoverified": Finder.get("q-onlytoverified").get(),
                "onlytononverified": Finder.get("q-onlytononverified").get(),
                "sendtoall": Finder.get("q-sendtoall").get()
            },
            "device": {
                "userAgent": {
                    "iphone": Finder.get("q-iphone").get(),
                    "android": Finder.get("q-android").get()
                },
                "userAgentOrder": Finder.get("q-deviceagentorder").get()
            },
            "timebeforelogin": Finder.get("q-timebeforelogin").get(),
            "timeafterlogin": Finder.get("q-timeafterlogin").get(),
            "randomActions": Finder.get("q-randomActions").get(),
            "loginActions":Finder.get("q-loginActions").get(),
            "downloadEmail": Finder.get("q-downloadEmail").get(),
        }
    def saveConfiguration(self):
        os.system("clear")

        # ask the user where to save the configuration
        path, _ = QFileDialog.getSaveFileName(
            self, "Save configuration", "", "qinsta (*.qinsta)")
        if path:
            with open(path, "w") as f:
                json.dump(self.get_conf_dict(), f, indent=4)

    def openConfiguration(self):
        # ask for file
        path, _ = QFileDialog.getOpenFileName(
            self, "Open configuration", "", "qinsta (*.qinsta)")
        if path:
            self.path = path
            with open(path, "r") as f:
                configuration_dict = json.load(f)
            # set the configuration values
            Finder.get(
                "q-currentUserList").set(configuration_dict["user_list"])
            Finder.get(
                "q-parallel").set(configuration_dict["parallel"])
            Finder.get(
                "q-currentAccsList").set(configuration_dict["accounts_list"])
            Finder.get("q-exportType").set(configuration_dict["exportType"])
            Finder.get("proxy").set(configuration_dict["proxies"])
            Finder.get(
                "q-usersforeachaccount").set(configuration_dict["usersforeachaccount"])
            Finder.get(
                "q-enablemsg").set(configuration_dict["message"]["enabled"])
            Finder.get(
                "q-message").set("{separator}".join(configuration_dict["message"]["text"]))
            Finder.get(
                "q-enablecomment").set(configuration_dict["comment"]["enabled"])
            Finder.get(
                "q-comment").set("{separator}".join(configuration_dict["comment"]["text"]))
            Finder.get(
                "q-enablelike").set(configuration_dict["like"]["enabled"])
            Finder.get(
                "q-enablefollow").set(configuration_dict["follow"]["enabled"])
            Finder.get(
                "q-enablemessagefilters").set(configuration_dict["message"]["enabled_filters"])
            Finder.get(
                "q-enablecommentfilters").set(configuration_dict["comment"]["enabled_filters"])
            Finder.get(
                "q-enablelike").set(configuration_dict["like"]["enabled_filters"])
            Finder.get(
                "q-enablefollow").set(configuration_dict["follow"]["enabled_filters"])
            Finder.get(
                "q-messagefilters").set(configuration_dict["message"]["filters"])
            Finder.get(
                "q-commentsfilter").set(configuration_dict["comment"]["filters"])
            Finder.get(
                "q-likefilter").set(configuration_dict["like"]["filters"])
            Finder.get(
                "q-followfilter").set(configuration_dict["follow"]["filters"])
            Finder.get(
                "q-timebeforemessage").set(configuration_dict["message"]["timebeforemessage"])
            Finder.get(
                "q-timeaftermessage").set(configuration_dict["message"]["timeaftermessage"])
            Finder.get(
                "q-timebeforecomment").set(configuration_dict["comment"]["timebeforecomment"])
            Finder.get(
                "q-timeaftercomment").set(configuration_dict["comment"]["timeaftercomment"])
            Finder.get(
                "q-timebeforelike").set(configuration_dict["like"]["timebeforelike"])
            Finder.get(
                "q-timeafterlike").set(configuration_dict["like"]["timeafterlike"])
            Finder.get(
                "q-timebeforefollow").set(configuration_dict["follow"]["timebeforefollow"])
            Finder.get(
                "q-timeafterfollow").set(configuration_dict["follow"]["timeafterfollow"])
            Finder.get("q-timebeforeloadinguser").set(
                configuration_dict["otherTimings"]["loadinguser"]["before"])
            Finder.get(
                "q-timeafterloadinguser").set(configuration_dict["otherTimings"]["loadinguser"]["after"])
            Finder.get("q-timebeforeendingaccounttask").set(
                configuration_dict["otherTimings"]["accounttask"]["before"])
            Finder.get("q-timeafterendingaccounttask").set(
                configuration_dict["otherTimings"]["accounttask"]["after"])
            Finder.get(
                "q-timeafterbeingblocked").set(configuration_dict["otherTimings"]["blockban"]["block"])
            Finder.get(
                "q-timeafterbeingbanned").set(configuration_dict["otherTimings"]["blockban"]["ban"])
            Finder.get(
                "q-timebeforelogout").set(configuration_dict["otherTimings"]["logout"]["before"])
            Finder.get(
                "q-timeafterlogout").set(configuration_dict["otherTimings"]["logout"]["after"])
            Finder.get(
                "q-userDataToJSON").set(configuration_dict["saveParams"]["toJson"])
            Finder.get(
                "q-userDataToCSV").set(configuration_dict["saveParams"]["toCSV"])
            Finder.get(
                "q-saveBlocksRecord").set(configuration_dict["saveParams"]["blocks"])
            Finder.get(
                "q-saveBansRecord").set(configuration_dict["saveParams"]["bans"])
            Finder.get(
                "q-twiceAttempt").set(configuration_dict["saveParams"]["twiceAttempt"])
            Finder.get(
                "q-askForCode").set(configuration_dict["saveParams"]["askForCode"])
            Finder.get(
                "q-saveCookies").set(configuration_dict["saveParams"]["saveCookies"])
            Finder.get(
                "q-saveSession").set(configuration_dict["saveParams"]["saveSession"])
            Finder.get(
                "q-onlytoverified").set(configuration_dict["sendingParams"]["onlytoverified"])
            Finder.get(
                "q-onlytononverified").set(configuration_dict["sendingParams"]["onlytononverified"])
            Finder.get(
                "q-sendtoall").set(configuration_dict["sendingParams"]["sendtoall"])
            Finder.get(
                "q-iphone").set(configuration_dict["device"]["userAgent"]["iphone"])
            Finder.get(
                "q-android").set(configuration_dict["device"]["userAgent"]["android"])
            Finder.get(
                "q-deviceagentorder").set(configuration_dict["device"]["userAgentOrder"])
            # time before and after login
            Finder.get(
                "q-timebeforelogin").set(configuration_dict["timebeforelogin"])
            Finder.get(
                "q-timeafterlogin").set(configuration_dict["timeafterlogin"])
            Finder.get("q-loginActions").set(configuration_dict.get("loginAction",True))
            Finder.get(
                "q-randomActions").set(configuration_dict.get("randomActions",True))
            Finder.get(
                "q-downloadEmail").set(configuration_dict.get("downloadEmail",True))
            self.update()
            Finder.get("currentConfig").set(self.path)

    def clearConfiguration(self):

        Finder.get("q-currentUserList").set("None")
        Finder.get("q-currentAccsList").set("None")
        Finder.get("proxy").set([])
        Finder.get("q-exportType").set(0)
        Finder.get("q-usersforeachaccount").set("0")
        Finder.get("q-enablemsg").set(False)
        Finder.get("q-enablecomment").set(False)
        Finder.get("q-enablelike").set(False)
        Finder.get("q-enablefollow").set(False)
        Finder.get("q-enablemessagefilters").set(False)
        Finder.get("q-enablecommentfilters").set(False)
        Finder.get("q-enablelike").set(False)
        Finder.get("q-enablefollow").set(False)
        Finder.get("q-messagefilters").set(
            {"frequency": 0, "minfollowers": 0, "maxfollowers": 0, "minmedia": 0, "maxmedia": 0})
        Finder.get("q-commentsfilter").set(
            {"frequency": 0, "minfollowers": 0, "maxfollowers": 0, "minmedia": 0, "maxmedia": 0})
        Finder.get("q-likefilter").set({"frequency": 0, "minfollowers": 0,
                                        "maxfollowers": 0, "minmedia": 0, "maxmedia": 0})
        Finder.get("q-followfilter").set({"frequency": 0, "minfollowers": 0,
                                          "maxfollowers": 0, "minmedia": 0, "maxmedia": 0})
        Finder.get("q-timebeforemessage").set("0")
        Finder.get("q-timeaftermessage").set("0")
        Finder.get("q-timebeforecomment").set("0")
        Finder.get("q-timeaftercomment").set("0")
        Finder.get("q-timebeforelike").set("0")
        Finder.get("q-timeafterlike").set("0")
        Finder.get("q-timebeforefollow").set("0")
        Finder.get("q-timeafterfollow").set("0")
        Finder.get("q-timebeforeloadinguser").set("0")
        Finder.get("q-timeafterloadinguser").set("0")
        Finder.get("q-timebeforeendingaccounttask").set("0")
        Finder.get("q-timeafterendingaccounttask").set("0")
        Finder.get("q-timeafterbeingblocked").set("0")
        Finder.get("q-timeafterbeingbanned").set("0")
        Finder.get("q-timebeforelogout").set("0")
        Finder.get("q-timeafterlogout").set("0")
        Finder.get("q-userDataToJSON").set(False)
        Finder.get("q-userDataToCSV").set(False)
        Finder.get("q-saveBlocksRecord").set(False)
        Finder.get("q-saveBansRecord").set(False)
        Finder.get("q-twiceAttempt").set(False)
        Finder.get("q-askForCode").set(False)
        Finder.get("q-saveCookies").set(False)
        Finder.get("q-saveSession").set(False)
        Finder.get("q-loginActions").set(False)
        Finder.get("q-randomActions").set(False)
        Finder.get("q-downloadEmail").set(False)
        Finder.get("q-onlytoverified").set(False)
        Finder.get("q-onlytononverified").set(False)
        Finder.get("q-sendtoall").set(True)
        Finder.get("q-iphone").set(False)
        Finder.get("q-android").set(True)
        Finder.get("q-deviceagentorder").set(False)
        self.update()

    def load_config(self):
        self.openConfiguration()


class MainWindow(Window,Configured):
    def __init__(self):
        super().__init__()
        self.worker = None

        self.deviceType = ButtonGroup()
        self.sendingParams = ButtonGroup()

        welcome_section = (
            Heading("Welcome!"),
            HDivider(),
            Heading("Experience the force of a <u>fully automated software</u>.", hp=Heading.Type.H3),
            Text("Introduction to QInsta"),
            GroupBox(
                (
                    "This software can:",
                    Text("""<ol><li>Send messages to millions of users</li><li>Send comments to millions of users</li><li>Send likes to millions of users</li><li>Send follows to millions of users</li><li>Send medias to millions of users</li><li>Increment your business relevance and revenue</li><li>Download user data for later use</li><li>Export users emails for cold mailing</li><li>Use proxies to avoid blocking and banning</li><li>Use multiple accounts at the same time (not avaiable*)</li><li>Load multiple configurations to spend less time configuring and more time sending</li><li>Blacklist with possibility to clear all, or clear by regex or by name</li><li>Add sending exceptions to avoid sending to people that are not targeted</li><li>Export a full overview of the sending campaign for ease of view</li><li>Usable as service (you can sell messages to other people)</li><li>Ask for 2FA code, to make use of more secure accounts and access methods</li><li>Save cookies for faster logins</li><li>Save network data for quicker responses and less bandwidth usage</li></ol>""", Text.Type.P3),
                    "And so much more..."
                ),
                ""
            ),
            Spacer()
        )
        configure_section = ScrollableContainer(
            Vertical(
                #region TITLE PART
                [Heading("Configure"), Spacer(), Button("Open").action(self.openConfiguration), Button(
                    "Save as").action(self.saveConfiguration), Button("New").action(self.clearConfiguration)],
                # endregion
                #region userlist and accounts list
                GroupBox(
                    (
                        GroupBox(
                            ([Text("Current:"), Text("None").id("q-currentUserList").wrap(True)],
                            [Button("Open").action(self.load_user_list), Spacer(), Button("Export to"), ComboBox(["CSV", "JSON", "EXCEL", "PLAIN TEXT"]).id("q-exportType")],
                            Text("Max amount of parallel accounts"),SpinBox().minV(1).maxV(10).id("q-parallel").enabled(False)),"Accounts list"),
                        GroupBox(
                            ([Text("Current:"), Text("None").id("q-currentAccsList").wrap(True)],
                            [Button("Open").action(self.load_accounts_list), Spacer(), Button("Export to"), ComboBox(["CSV", "JSON", "EXCEL", "PLAIN TEXT"]).id("q-exportType")]
                            ),"Targets list"),

                        ListBox("Proxy list",on_add=self.add_proxy).id("proxy"),
                    ),
                    "Users Accounts and Proxy configuration"
                ),
                #endregion
                GroupBox(
                    (
                        [ # MESSAGES & COMMENTS
                            #region MESSAGES
                            (
                                Horizontal(
                                    Text("Send messages"),
                                    Toggle().id("q-enablemsg").check(True).pl(5).pr(5).setW(35).setH(28),
                                    Spacer()
                                ).align(Qt.AlignmentFlag.AlignTop),
                                MultilineAssistedField("",True,["{username}","{name}","{followers}","{following}","{separator}","{@userprofile}","{reel:link}","{post:link}"],"message").visible("q-enablemsg").id("q-message"),
                                Spacer()
                            ),
                            #endregion
                            #region COMMENTS
                            (
                                Horizontal(Text("Send comments"),Toggle().id("q-enablecomment").check(True).pl(5).pr(5).setW(35).setH(28),Spacer()).align(Qt.AlignmentFlag.AlignTop),
                                MultilineAssistedField("", True, ["{username}", "{name}", "{followers}", "{following}", "{separator}", "{likes}", "{comments}"], "comment").id("q-comment").visible("q-enablecomment"),
                                Spacer()
                            )
                            # endregion
                        ],
                        Vertical(Text("How many users for each account",Text.Type.P3),
                        Field().set_int().id("q-usersforeachaccount")),
                        GroupBox(
                            (
                                [
                                    #region LIKE PARAMS
                                    Vertical(
                                        CheckBox("Send Likes").id("q-enablelike"),
                                        SendingValidator("Likes").id("q-likefilter").link("q-enablelike"),
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    #endregion
                                    # region FOLLOW PARAMS
                                    Vertical(
                                        CheckBox("Send Follows").id("q-enablefollow"),
                                        SendingValidator("Follows").id("q-followfilter").link("q-enablefollow"),
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    #endregion
                                ],
                                [
                                    # region COMMENT PARAMS
                                    Vertical(
                                        CheckBox("enable comment filters").id("q-enablecommentfilters").enableCondition("q-enablecomment"),
                                        SendingValidator("Comments").id("q-commentsfilter").visible("q-enablecomment").link("q-enablecommentfilters"),
                                    ).align(Qt.AlignmentFlag.AlignTop),
                                    # endregion
                                    # region MESSAGE PARAMS
                                    Vertical(
                                        CheckBox("enable message filters").id("q-enablemessagefilters").enableCondition("q-enablemsg"),
                                        SendingValidator("Messages").id("q-messagefilters").visible("q-enablemsg").link("q-enablemessagefilters"),
                                    ).align(Qt.AlignmentFlag.AlignTop)
                                    # endregion
                                ],
                            ),
                            "Single-tap interactions"
                        )
                    ),
                    "Direct user interactions"
                ),
                GroupBox(
                    (
                        GroupBox(
                            [
                                RadioButton("iPhone").id("q-iphone").assign(self.deviceType),
                                RadioButton("Android").id("q-android").assign(self.deviceType).check(True)
                            ],
                            "Device Type"
                        ),
                        [Text("Device agent picking order",Text.Type.P3),ComboBox(["Default device agent","Random device agent"]).id("q-deviceagentorder")]
                    ),
                    "Device configuration"
                ),
                GroupBox(
                    [
                        (
                            FormField("Time before login").id("q-timebeforelogin"),
                            FormField("Time after login").id("q-timeafterlogin"),
                            FormField("Time before message").id("q-timebeforemessage").link("q-enablemsg"),
                            FormField("Time after message").id("q-timeaftermessage").link("q-enablemsg"),
                            FormField("Time before comment").id("q-timebeforecomment").link("q-enablecomment"),
                            FormField("Time after comment").id("q-timeaftercomment").link("q-enablecomment"),
                            FormField("Time before loading user").id("q-timebeforeloadinguser"),
                            FormField("Time after loading user").id("q-timeafterloadinguser"),
                            FormField("Time before ending account task").id("q-timebeforeendingaccounttask"),
                            FormField("Time after ending account task").id("q-timeafterendingaccounttask"),
                            Spacer(),
                        ),
                        HDivider(),
                        (
                            FormField("Time before like").id("q-timebeforelike").link("q-enablelike"),
                            FormField("Time after like").id("q-timeafterlike").link("q-enablelike"),
                            FormField("Time before follow").id("q-timebeforefollow").link("q-enablefollow"),
                            FormField("Time after follow").id("q-timeafterfollow").link("q-enablefollow"),
                            FormField("Time after being blocked").id("q-timeafterbeingblocked"),
                            FormField("Time after being banned").id("q-timeafterbeingbanned"),
                            FormField("Time before logout").id("q-timebeforelogout"),
                            FormField("Time after logout").id("q-timeafterlogout"),
                            Spacer(),
                        )
                    ],
                    "Timings (in seconds)"
                ),
                GroupBox(
                    (
                        [Toggle().id("q-userDataToJSON"), Text("Save user data to JSON",Text.Type.P3),Toggle().id("q-userDataToCSV"),Text("Save user data to CSV",Text.Type.P3)],
                        [Toggle().id("q-saveBlocksRecord"), Text("Save blocks record", Text.Type.P3), Toggle().id("q-saveBansRecord"), Text("Save bans record", Text.Type.P3)],
                        [Toggle().id("q-twiceAttempt"), Text("Attempt twice to login", Text.Type.P3), Toggle().id("q-askForCode"), Text("Ask for manual code input", Text.Type.P3)],
                        [Toggle().id("q-saveCookies").check(True), Text("Save cookies", Text.Type.P3), Toggle().id("q-saveSession").check(True), Text("Save session ID", Text.Type.P3)],
                        [Toggle().id("q-randomActions").check(True), Text("More random actions", Text.Type.P3), Toggle().id("q-loginActions").check(True), Text("Login default actions", Text.Type.P3)],
                        [Toggle().id("q-downloadEmail").check(True), Text("Save user email/data", Text.Type.P3)],
                    ),
                    "Extra configurations"
                ),
                GroupBox([RadioButton("Send only to verified").id("q-onlytoverified").assign(self.sendingParams),RadioButton("Send only to non verified").id("q-onlytononverified").assign(self.sendingParams), RadioButton("Send to all").id("q-sendtoall").assign(self.sendingParams).check(True)],"Extra sending options"),
                Spacer(),
            ).align(Qt.AlignmentFlag.AlignTop)
        ).h(Qt.ScrollBarPolicy.ScrollBarAlwaysOff).v(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        run_section = (
            Heading("Select a script"),
            HDivider(),
            GroupBox([Button("Select").set_icon(QIcon("folder.png")).action(self.load_config), Label("Current"),Spacer(),Label("None").id("currentConfig")], "Load script"),
            GroupBox( 
                (
                    Horizontal(
                        Button("Start").id(
                            "b-start").action(self.start),
                        Button("Stop").id("b-stop").enabled(True),
                        Button("Export...").id("b-export").enabled(True),
                        Button("Logout").id("b-logout").enabled(True)
                    ).expandMin(),
                    Vertical(
                        [Button("Reset counters").action(lambda: Incrementer().resetAll()), Button("Clear blacklist").action(
                            lambda: open(os.path.join(user_data_dir("QInsta", "pstudios", roaming=True if os.name == "nt" else False), "data/blacklist.txt"), "w").close() if os.path.exists(os.path.join(user_data_dir("QInsta", "pstudios", roaming=True if os.name == "nt" else False), "data/blacklist.txt")) else None)],
                        [
                            Tile("Interactions").id("Total"),
                            Tile("Logins").id("Logins")
                        ],
                        [
                            StringTile("Current account in use").id("Account")
                        ],
                        Heading("Overall data",hp=Heading.Type.H2),
                        [
                            MiniTile("DMs").id("DMs"),
                            MiniTile("Comments").id("Comments"),
                            MiniTile("Likes").id("Likes"),
                            MiniTile("Follows").id("Follows")
                        ],
                        [
                            [Tile("Banned").id("Banned")],
                            [MiniTile("Blocked").id("Blocked"),
                            MiniTile("Successful").id("Successful"),]
                        ],
                    ).expandMin(),
                    Heading("Last messages"),
                    ScrollableContainer(
                        ConsoleList(0).id("q-console").setH(500)),
            ),"Task manager")
        )
        extract_section=(
            Heading("Extract data"),
            HDivider(),
            (
                Horizontal(
                    GroupBox([Field().id("e-username")], "Username"),
                    GroupBox([Field().id("e-password")], "Password"),
                ).expandMin(),
                Horizontal(
                    GroupBox([ComboBox(["Followers", "Followings", "Hashtags", "Likes", "Comments"]).id("e-targettype"), Field(
                        "Profile, hashtag or post url").id("e-target")], "Target"),
                    GroupBox([Field().id("e-amount")], "Max amount to extract"),
                ).expandMin(),
                GroupBox([Field().id("e-proxy")], "Proxy"),
                GroupBox([Field().id("e-maxid")], "Last Id"),
                GroupBox([Button("Select folder").action(self.select_extractor_save_folder),Label("None").id("e-folder"),CheckBox("Save extra data file").id("e-saveextra")], "Output file").expandMin(),
                Button("Start script").action(self.start_extraction),
                Text("Output console"),
                ConsoleList().id("e-console")
            ),
        )
        # Creating components using your library
        main_layout = Vertical(
            NavigationBar(
                Heading("QINSTA"),
                NavigationLink("HOME")   .target(welcome_section),
                NavigationLink("SCRIPTS").target(configure_section),
                NavigationLink("RUN")    .target(run_section),
                NavigationLink("EXTRACT").target(extract_section)
            ).id("navbar"),
        ).pl(5).pr(5)

        self.setCentralWidget(main_layout)

        # Setting up the main window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("QInsta")
    def match_targettype(self, target_type):
        if target_type == "Followers":
            return TargetType.FOLLOWERS
        elif target_type == "Followings":
            return TargetType.FOLLOWINGS
        elif target_type == "Hashtags":
            return TargetType.HASHTAGS
        elif target_type == "Likes":
            return TargetType.LIKES
        elif target_type == "Comments":
            return TargetType.COMMENTS
        else:
            return TargetType.PROFILE
    def start_extraction(self):
        if not Finder.get("e-amount").text().isdigit():
            # show the user a warning popup
            message = "amount must be specified"
            QMessageBox.warning(self, "Warning", message)
            return
        ep = ExtractionParams(
            username=Finder.get("e-username").text(),
            password=Finder.get("e-password").text(),
            target_type=self.match_targettype(Finder.get("e-targettype").currentText()),
            target=Finder.get("e-target").text(),
            max_amount=int(Finder.get("e-amount").text()),
            proxy=Finder.get("e-proxy").text(),
            save_user_id=Finder.get("e-saveextra").isChecked(),
            output_path=Finder.get("e-folder").text(),
            max_id=Finder.get("e-maxid").text(),
        )
        self.ec = ExtractorCore(ep, self.eConsoleWrite)
        self.ec.console.connect(self.eConsoleWrite)
        self.ec.start()
    def select_extractor_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            Finder.get("e-folder").setText(folder)
    def increment_total(self):
        Finder.get("Total").increment()
    def increment_logins(self):
        Finder.get("Logins").increment()
    def set_current_account(self, account):
        Finder.get("Account").set(account)
    def increment_dms(self):
        Finder.get("DMs").increment()
    def increment_comments(self):
        Finder.get("Comments").increment()
    def increment_likes(self):
        Finder.get("Likes").increment()
    def increment_follows(self):
        Finder.get("Follows").increment()
    def increment_banned(self):
        Finder.get("Banned").increment()
    def increment_blocked(self):
        Finder.get("Blocked").increment()
    def increment_successful(self):
        Finder.get("Successful").increment()
    def decrease_successful(self):
        Finder.get("Successful").decrease()
    def delete_selected_parameter(self, widget_id):
        idx = Finder.get(widget_id).currentIndex() # type: ignore
        if idx:
            Finder.get(widget_id).remove(idx.row()) # type: ignore
    def consoleWrite(self, message, type):
        Finder.get("q-console").emit(message, type)

    def eConsoleWrite(self, message, type):
        Finder.get("e-console").emit(message, type)
    def start(self):
        try:
            license_location = os.path.join(user_data_dir(
                "QInsta", "pstudios", roaming=True if os.name == "nt" else False), "LICENSE-KEY.txt")
            ConsoleWriter.debug("Opening key at "+license_location)
            if not os.path.exists(license_location):
                if not os.path.exists(user_data_dir(
                    "QInsta", "pstudios", roaming=True if os.name == "nt" else False)):
                    os.makedirs(user_data_dir(
                        "QInsta", "pstudios", roaming=True if os.name == "nt" else False),exist_ok=True)
                # ask the user for a license key
                license_key, ok = QInputDialog.getText(self, "License key", "Enter your license key:")
                if ok:
                    with open(license_location, "w") as f:
                        f.write(license_key)
                    ConsoleWriter.debug("License key saved at "+license_location)
                else:
                    return
        except:
            QMessageBox.critical(self, "Error", "Failed to save license key at "+user_data_dir(
                "QInsta", "pstudios", roaming=True if os.name == "nt" else False))
            return
        path = Finder.get("currentConfig").text()
        use_curr_config = False
        if not os.path.exists(path):
            response = QMessageBox.question(
                self, "Error", "Script not found. Do you want to load the current configuration?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,QMessageBox.StandardButton.Yes)
            if response == QMessageBox.StandardButton.Yes:
                use_curr_config=True
            else:
                return
        elif not os.path.isfile(path) and not use_curr_config:
            response = QMessageBox.question(
                self, "Error", "Selected item is not a file. Do you want to load the current configuration?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if response == QMessageBox.StandardButton.Yes:
                use_curr_config=True
            else:
                return
        config=None
        try:
            if use_curr_config:
                config = open_config("",dct=self.get_conf_dict())
            else:
                config = open_config(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open script: {e}")
            return
        if config:
            try:
                self.worker = InstaProcess(config, ButtonHolder(
                    Finder.get("b-start"),
                    Finder.get("b-stop"),
                    Finder.get("b-export"),
                    Finder.get("b-logout")))
                self.worker.total.connect(self.increment_total)
                self.worker.login.connect(self.increment_logins)
                self.worker.current_account.connect(self.set_current_account)
                self.worker.dms.connect(self.increment_dms)
                self.worker.comment.connect(self.increment_comments)
                self.worker.like.connect(self.increment_likes)
                self.worker.follow.connect(self.increment_follows)
                self.worker.banned.connect(self.increment_banned)
                self.worker.blocked.connect(self.increment_blocked)
                self.worker.successful.connect(self.increment_successful)
                self.worker.dec_successful.connect(self.decrease_successful)
                self.worker.console.connect(self.consoleWrite)
                Finder.get("b-stop").action(lambda:self.worker.stop_process())
                Finder.get("b-logout").action(lambda:self.worker.acc_logout())
                Finder.get("b-export").action(lambda:self.export_command(self.worker.export_logs))
                self.worker.request_input_code.connect(self.ask_user_for_code)
                self.worker.start()
            except Exception as e:
                import traceback
                QMessageBox.critical(self, "Error", f"Failed to start process due to {traceback.format_exc()}")
    def ask_user_for_code(self,for_,challenge_type,code):
        # ask user a string input for the code
        response, ok = QInputDialog.getText(self, "Authentication", f"Enter the {for_} code:", Field.EchoMode.Normal)
        if not ok:
            code.setCode("BAD")
        else:
            code.setCode(response)
    def export_command(self,callable):
        callable(QFileDialog.getExistingDirectory(self, "Select a folder"))
    def add_proxy(self,lst:ListWidget):
        self.win = Vertical()
        self.win.setWindowTitle("Add Proxy")
        connection_type = ComboBox(["HTTP", "HTTPS"])
        field = Field("Proxy IP")
        port = Field("Proxy port")
        username = Field("Proxy username")
        password = Field("Proxy password")
        checkbox = Toggle()
        def voidWin():
            self.win.close()
            self.win.deleteLater()
            self.win = None
            # Check if authentication toggle is enabled
            if checkbox.isChecked():
                auth_part = f"{username.get()}:{password.get()}@"
            else:
                auth_part = ""

            lst.add(f"{connection_type.currentText().lower()}://{auth_part}{field.get()}:{port.get()}")
        self.win.add(
            Heading("Add a new proxy"),
            [connection_type,field,port],
            [checkbox,username.link(checkbox),password.link(checkbox)],
            [Button("OK").action(voidWin), Button("Cancel")]
        ).padding(5)
        self.win.show()
    def load_user_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Plain text (*.txt);;Comma separated values (*.csv);;JSON dictionary (*.json);;Excel XML (>2016) (*.xlsx)")
        if path:
            Finder.get("q-currentUserList").setText(path)

    def load_accounts_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Plain text (*.txt);;Comma separated values (*.csv);;JSON dictionary (*.json);;Excel XML (>2016) (*.xlsx)")
        if path:
            Finder.get("q-currentAccsList").setText(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
