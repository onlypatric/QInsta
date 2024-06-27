import json
import os
from comps.Elements import Finder
from PyQt6.QtWidgets import QFileDialog


class Configured:
    def saveConfiguration(self):
        text_conf = []
        os.system("clear")
        for text in Finder.get("q-message").get().split("{separator}"):
            if text.startswith("\n"):
                text = text[1:]
            text_conf.append(text)
        text_comm_conf = []
        for text in Finder.get("q-comment").get().split("{separator}"):
            if text.startswith("\n"):
                text = text[1:]
            text_comm_conf.append(text)
        configuration_dict = {
            "user_list": Finder.get("q-currentUserList").get(),
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
            }
        }
        # ask the user where to save the configuration
        path, _ = QFileDialog.getSaveFileName(
            self, "Save configuration", "", "qinsta (*.qinsta)")
        if path:
            with open(path, "w") as f:
                json.dump(configuration_dict, f, indent=4)

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
        Finder.get("q-onlytoverified").set(False)
        Finder.get("q-onlytononverified").set(False)
        Finder.get("q-sendtoall").set(True)
        Finder.get("q-iphone").set(False)
        Finder.get("q-android").set(True)
        Finder.get("q-deviceagentorder").set(False)
        self.update()

    def load_config(self):
        self.openConfiguration()
