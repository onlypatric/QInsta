from datetime import datetime
from enum import Enum
import os
from pathlib import Path
import re
from threading import Thread,Lock
import time
from typing import Dict, List, Tuple
from instagrapi import Client,exceptions,types
from PyQt6.QtCore import QThread, pyqtSignal,pyqtSlot
from extracomps.ButtonHolder import ButtonHolder
from utils.configLoader import Config,Filters
from extracomps.ConsoleWriter import ConsoleWriter
from extracomps.ConsoleList import ConsoleList
import pandas as pd
import json
from appdata import AppDataPaths
import random
import json

TEST_MODE = True

class License(Enum):
    basic=0
    advanced=1
    pro=2
    unlimited=3

class LogRegister:
    def __init__(self,name:str) -> None:
        self.name = name
        self.content = []
    def log(self,text:str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content.append(date+"|"+text)
    def obtain(self) -> List[str]:
        t = self.content
        self.content = []
        return t
    def export(self, path:str) -> None:
        with open(path, "a") as file:
            for line in self.content:
                file.write(line+"\n")
        # clear the logs
        self.content.clear()
class Code:
    def __init__(self) -> None:
        self.code = None
    def setCode(self,code:str):
        self.code = code
    def obtainCode(self):
        t = self.code
        self.code = None
        if t == "BAD":
            return "".join([random.choice("1234567890") for i in range(6)])
        return t
class Readables:
    def read_accounts_list_xlsx(self) -> Tuple[bool, List[Dict[str, str]]]:
        try:
            content = pd.read_excel(self.config.user_list)
            # check if username and password columns exist
            if "username" not in content.columns or "password" not in content.columns:
                return False, []
            user_list = [
                {
                    "username": username,
                    "password": password
                }
                for username, password in zip(content["username"], content["password"])
            ]
            return True, user_list
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_accounts_list_csv(self) -> Tuple[bool, List[Dict[str, str]]]:
        try:
            content = pd.read_csv(self.config.user_list)
            # check if username and password columns exist
            if "username" not in content.columns or "password" not in content.columns:
                return False, []
            user_list = [
                {
                    "username": username,
                    "password": password
                }
                for username, password in zip(content["username"], content["password"])
            ]
            return True, user_list
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_accounts_list_txt(self) -> Tuple[bool, List[Dict[str, str]]]:
        try:
            with open(self.config.user_list, "r") as file:
                sep = None
                content = file.read()
                # check if separator is : or ; or , or . or /
                if ":" in content:
                    sep = ":"
                elif ";" in content:
                    sep = ";"
                elif "," in content:
                    sep = ","
                elif "." in content:
                    sep = "."
                elif "/" in content:
                    sep = "/"
                if sep is None:
                    return False, []
                user_list = []
                for line in content.splitlines():
                    user_list.append(
                        {
                            "username": line.split(sep)[0],
                            "password": line.split(sep)[1]
                        }
                    )
                return True, user_list
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_accounts_list_json(self) -> Tuple[bool, List[Dict[str, str]]]:
        try:
            with open(self.config.user_list, "r") as file:
                content = json.load(file)
                # check if username and password columns exist
                if "username" not in content[0] or "password" not in content[0]:
                    return False, []
                return True, content
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_target_list_json(self) -> Tuple[bool, List[str]]:
        try:
            with open(self.config.accounts_list, "r") as file:
                content = json.load(file)
                # check if username and password columns exist
                if "username" in content:
                    return False, content["username"]
                elif "userid" in content:
                    return True, content["userid"]
                return False, []
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_target_list_csv(self) -> Tuple[bool, List[str]]:
        try:
            content = pd.read_csv(self.config.accounts_list)
            # check if username and password columns exist
            if "username" in content.columns:
                return True, content["username"]
            elif "userid" in content.columns:
                return True, content["userid"]
            return False, []
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_target_list_excel(self) -> Tuple[bool, List[str]]:
        try:
            content = pd.read_excel(self.config.accounts_list)
            # check if username and password columns exist
            if "username" in content.columns:
                return True, content["username"]
            elif "userid" in content.columns:
                return True, content["userid"]
            return False, []
        except:
            self.critical("Failed to read user file!")
            return False, []

    def read_target_list_txt(self) -> Tuple[bool, List[str]]:
        try:
            with open(self.config.accounts_list, "r") as file:
                return True, file.read().splitlines()
        except:
            self.critical("Failed to read user file!")
            return False, []
class ConsoleConnected:
    console = pyqtSignal(str, ConsoleList.Type)
    # region CONSOLE OUT

    def debug(self, m: str):
        self.console.emit(m, ConsoleList.Type.DEBUG)

    def info(self, m: str):
        self.console.emit(m, ConsoleList.Type.INFO)

    def warning(self, m: str):
        self.console.emit(m, ConsoleList.Type.WARNING)

    def error(self, m: str):
        self.console.emit(m, ConsoleList.Type.ERROR)

    def critical(self, m: str):
        self.console.emit(m, ConsoleList.Type.CRITICAL)
    # endregion
class InstaProcess(QThread, Readables, ConsoleConnected):
    started = pyqtSignal()
    paused = pyqtSignal()
    finished = pyqtSignal()
    request_input_code = pyqtSignal(str,str,Code)
    log_output_signal = pyqtSignal(
        LogRegister, LogRegister, LogRegister, LogRegister, LogRegister)
    pause = False
    stop = False
    code = None
    def __init__(self, config:Config,licenseType:License,buttons:ButtonHolder):
        super().__init__()
        self.code = Code()
        self.licenseType=licenseType
        self.config = config
        self.accepted = None
        self.buttons = buttons
        self.appdata = AppDataPaths()
        self.logins = LogRegister("Login")
        self.messages = LogRegister("Messages")
        self.comments = LogRegister("Comments")
        self.likes = LogRegister("Likes")
        self.follows = LogRegister("Follows")
        self.all = LogRegister("All")
        self.config_path = self.appdata.get_config_path("QInsta",create=True)
        self.cookiepath = os.path.join(self.config_path, "Cookies")
        self.log_path = os.path.join(self.config_path, "logs")
        os.makedirs(self.config_path,exist_ok=True)
        os.makedirs(self.cookiepath, exist_ok=True)
    def run(self):
        ConsoleWriter.clear()
        valid_extensions = [".txt",".csv",".json",".xlsx"]
        self.parsedUserList=None
        # region ACCOUNTS
        self.info("Opening accounts file...")
        if not self.config.user_list.exists():
            self.critical("Accounts file not found!")
            return
        elif not self.config.user_list.is_file():
            self.critical("Accounts file is not a file!")
            return
        elif not self.config.user_list.suffix in valid_extensions:
            self.critical("Accounts file is not a valid file!")
            return
        if self.config.user_list.suffix == ".xlsx" or self.config.user_list.suffix == ".csv":
            self.info("Reading Excel user file...")
            ok,self.parsedUserList = self.read_accounts_list_xlsx() if self.config.user_list.suffix == ".xlsx" else self.read_accounts_list_csv()
            if not ok:
                self.critical(f"Could not find username and password column in {self.config.user_list}")
                return
        elif self.config.user_list.suffix == ".txt":
            self.info("Reading Text user file...")
            ok,self.parsedUserList = self.read_accounts_list_txt()
            if not ok:
                self.critical(f"Could not find username and password column in {self.config.user_list}")
                return
        elif self.config.user_list.suffix == ".json":
            self.info("Reading Json user file...")
            ok,self.parsedUserList = self.read_accounts_list_json()
            if not ok:
                self.critical(f"Could not find username and password column in {self.config.user_list}")
                return
        if self.parsedUserList is None:
            self.critical("Invalid file type!")
            return
        # endregion
        self.info(f"Loading {len(self.parsedUserList)} accounts from account list")
        self.parsedTargetList = None
        # region TARGETS
        self.info("Opening target file...")
        if not self.config.accounts_list.exists():
            self.critical("Target file not found!")
            return
        elif not self.config.accounts_list.is_file():
            self.critical("Target file is not a file!")
            return
        elif not self.config.accounts_list.suffix in valid_extensions:
            self.critical("Target file is not a valid file!")
            return
        if self.config.accounts_list.suffix == ".xlsx" or self.config.accounts_list.suffix == ".csv":
            self.info("Reading Excel target file...")
            ok,self.parsedTargetList = self.read_target_list_excel() if self.config.accounts_list.suffix == ".xlsx" else self.read_target_list_csv()
            if not ok:
                self.critical(f"Could not find username username or userid column in {self.config.accounts_list}")
                return
        elif self.config.accounts_list.suffix == ".txt":
            self.info("Reading Text target file...")
            ok,self.parsedTargetList = self.read_target_list_txt()
            if not ok:
                self.critical(f"Could not find username or userid column in {self.config.accounts_list}")
                return
        elif self.config.accounts_list.suffix == ".json":
            self.info("Reading Json target file...")
            ok,self.parsedTargetList = self.read_target_list_json()
            if not ok:
                self.critical(f"Could not find username or userid column in {self.config.accounts_list}")
                return
        if not self.parsedTargetList:
            self.critical("Invalid file type!")
            return
        #endregion
        self.info(f"Loading {len(self.parsedTargetList)} targets from target list")
        # show how many proxies were found if > 0
        if len(self.config.proxies) > 0:
            self.info(f"Found {len(self.config.proxies)} proxies")
        else:
            self.info("Proxy mode off, no proxies found")
        # check if message mode is enabled
        if self.config.message.enabled:
            self.info(f"DM mode enabled with filters {'ON' if self.config.message.enabled_filters else 'OFF'}")
        else:
            self.info(f"DM mode disabled")
        # check if comment mode is enabled
        if self.config.comment.enabled:
            self.info(f"Comment mode enabled with filters {'ON' if self.config.comment.enabled_filters else 'OFF'}")
        else:
            self.info(f"Comment mode disabled")
        # check if like mode is enabled
        if self.config.like.enabled:
            self.info(f"Like mode enabled with filters {'ON' if self.config.like.enabled_filters else 'OFF'}")
        else:
            self.info(f"Like mode disabled")
        # check if follow mode is enabled
        if self.config.follow.enabled:
            self.info(f"Follow mode enabled with filters {'ON' if self.config.follow.enabled_filters else 'OFF'}")
        else:
            self.info(f"Follow mode disabled")
        
        # check saveParams
        if self.config.saveParams.to_json:
            self.info("Saving user data to json file")
        if self.config.saveParams.to_csv:
            self.info("Saving user data to csv file")
        if self.config.saveParams.blocks:
            self.info("Saving blocked accounts to csv")
        if self.config.saveParams.bans:
            self.info("Saving banned accounts to csv")
        if self.config.saveParams.twice_attempt:
            self.info("If any login is failed, the software will attempt a second login")
        if self.config.saveParams.ask_for_code:
            self.info("The software will ask for 2FA code if needed")
        if self.config.saveParams.save_cookies:
            self.info("The software will save cookies to a file")
        if self.config.saveParams.save_session:
            self.info("The software will save SessionID to a file")
        
        if self.config.sendingParams.onlytoverified:
            self.info("The software will only send messages to verified accounts")
        elif self.config.sendingParams.onlytononverified:
            self.info("The software will only send messages to non-verified accounts")
        else:
            self.info("The software will send messages to all accounts")
        
        self.info("Device settings are not yet supported...")
        
        self.started.emit()
        self.info("Starting script.")

        self.stop = False
        self.logout = False
        self.pc = ProcessCore(self.parsedUserList, self.parsedTargetList, self.config, self, self.appdata, self.cookiepath, False)
        self.buttons.enableAll()
        self.pc.run()
        self.buttons.disableAll()

    def obtain_code(self, for_:str, challenge_type:str):
        self.info(f"Asking verification code for {challenge_type}")
        self.request_input_code.emit(for_,str(challenge_type),self.code)
        while self.code.code is None:
            time.sleep(0.5)
        return self.code.obtainCode()
    @pyqtSlot()
    def stop_process(self):
        self.stop = True
    @pyqtSlot()
    def acc_logout(self):
        self.logout = True
    @pyqtSlot(str)
    def export_logs(self,dir:str):
        # create 5 files, for each log type with the current date
        if dir == "" or dir is None:
            return
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logins.export(f"{dir}/logins_{date}.txt")
        self.messages.export(f"{dir}/messages_{date}.txt")
        self.comments.export(f"{dir}/comments_{date}.txt")
        self.likes.export(f"{dir}/likes_{date}.txt")
        self.follows.export(f"{dir}/follows_{date}.txt")
class ProcessUtils:
    cookiepath:str
    config:Config
    userlist:List[Dict[str,str]]
    targetlist:List[str]

    def process_strings(first_string):
        # Step 1: Extract and save the first string, then append it to the end of the array

        # Step 2: Define a function to handle the patterns
        def handle_patterns(s):
            # Find all occurrences of the patterns
            patterns = re.findall(r'{@[\w.]+}|{reel:[^}]+}|{post:[^}]+}', s)

            resolved_strings = []

            last_index = 0
            for pattern in patterns:
                start_index = s.find(pattern, last_index)
                end_index = start_index + len(pattern)

                # Split the string at the pattern
                before_pattern = s[last_index:start_index]
                after_pattern = s[end_index:]

                # Extract the content within the curly braces
                content = pattern[1:-1]  # Remove the surrounding braces

                # Append the parts to the resolved strings array
                resolved_strings.append(before_pattern)
                resolved_strings.append(content)

                # Update the last_index
                last_index = end_index

            # Append the remaining part of the string
            resolved_strings.append(s[last_index:])

            return resolved_strings

        # Step 3: Process the first string
        resolved_array = handle_patterns(first_string)

        return resolved_array

    def check_cookies_exist(self, username: str) -> bool:
        return os.path.exists(os.path.join(self.cookiepath, f"{username}.json"))

    def get_cookies(self, username: str) -> Dict[str, str]:
        if not self.check_cookies_exist(username):
            return None
        with open(os.path.join(self.cookiepath, f"{username}.json"), "r") as file:
            return json.load(file)
    def remove_cookies(self, username: str):
        if not self.check_cookies_exist(username):
            return
        os.remove(os.path.join(self.cookiepath, f"{username}.json"))

    def maskPassword(self, password: str) -> str:
        return password[0]+("*"*(len(password)-2))+password[-1]

    def filter_check(self, filter: Filters, user_info: types.User) -> bool:
        if filter.minfollowers > user_info.follower_count:
            return False
        if filter.maxfollowers < user_info.follower_count:
            return False
        if filter.minmedia > user_info.media_count:
            return False
        if filter.maxmedia < user_info.media_count:
            return False
        return True

    def acquire_user(self) -> Dict[str, str]:
        if len(self.userlist) > 0:
            user = self.userlist.pop(0)
            self.userlist.append(user)
            return user
        return None

    def target_size(self) -> int:
        return len(self.targetlist)

    def acquire_target(self) -> str:
        if len(self.targetlist) > 0:
            target = self.targetlist.pop(0)
            return target
        return None

    def acquire_message(self) -> List[str]:
        if len(self.config.message.text) > 0:
            message = self.config.message.text.pop(0)
            self.config.message.text.append(message)
            return ProcessUtils.process_strings(message)
        return None

    def acquire_comment(self) -> str:
        if len(self.config.comment.text) > 0:
            comment = self.config.comment.text.pop(0)
            self.config.comment.text.append(comment)
            return comment
        return None

    def acquire_proxy(self) -> str:
        if len(self.config.proxies) > 0:
            proxy = self.config.proxies.pop(0)
            self.config.proxies.append(proxy)
            return proxy
        return None
class InstaCore:
    config:Config
    parent:InstaProcess
    testmode:bool

    class AnyStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
    class MessageStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
    class CommentStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
    class LoginStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        BAD_PASSWORD = 2
        BAD_USERNAME = 3
        BAD_PROXY = 4
        LOGIN_REQUIRED = 5
    class MediaStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
        NONE_AVAIABLE = 7

    class UserStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
    def logLogin(self, status: LoginStatus, username: str = None, password: str = None):
        self.parent.logins.log(f"LOGIN FOR {username}:{self.maskPassword(password)} | STATUS -> {status}")
        self.parent.all.log(f"LOGIN FOR {username}:{self.maskPassword(password)} | STATUS -> {status}")
    def logMessage(self, status: MessageStatus, username: str = None):
        self.parent.messages.log(f"MESSAGE FOR {username} | MESSAGE | STATUS -> {status}")
        self.parent.all.log(f"MESSAGE FOR {username} | MESSAGE | STATUS -> {status}")
    def logComment(self, status: CommentStatus, username: str = None):
        self.parent.comments.log(f"COMMENT FOR {username} | COMMENT | STATUS -> {status}")
        self.parent.all.log(f"COMMENT FOR {username} | COMMENT | STATUS -> {status}")
    def logLike(self, status: MediaStatus, username: str = None):
        self.parent.likes.log(f"LIKE FOR {username} | LIKE | STATUS -> {status}")
        self.parent.all.log(f"LIKE FOR {username} | LIKE | STATUS -> {status}")
    def logFollow(self, status: UserStatus, username: str = None):
        self.parent.follows.log(f"FOLLOW FOR {username} | FOLLOW | STATUS -> {status}")
        self.parent.all.log(f"FOLLOW FOR {username} | FOLLOW | STATUS -> {status}")
    def anyLog(self, status:AnyStatus, text:str):
        self.parent.all.log(f"{text} | STATUS -> {status}")
    def message(self, client: Client, msgcollection: List[str], user_info: types.User) -> MessageStatus:
        if self.testmode:return self.MessageStatus.OK
        time.sleep(self.config.message.timebeforemessage)
        for msg in msgcollection:
            if msg.startswith("@"):
                try:
                    client.direct_profile_share(client.user_info_by_username(
                        msg.replace("@", "")).pk, user_info.pk)
                except exceptions.UserNotFound:
                    return self.MessageStatus.USER_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
            elif msg.startswith("reel:"):
                try:
                    client.direct_media_share(client.media_info(
                        client.media_pk_from_url(msg.replace("reel:", ""))).id, user_info.pk)
                except exceptions.MediaNotFound:
                    return self.MessageStatus.MEDIA_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
            elif msg.startswith("post:"):
                try:
                    client.direct_media_share(client.media_info(
                        client.media_pk_from_url(msg.replace("post:", ""))).id, user_info.pk)
                except exceptions.MediaNotFound:
                    return self.MessageStatus.MEDIA_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
            else:
                try:
                    client.direct_send(msg.replace("{username}", user_info.username).replace(
                        "{name}", user_info.full_name).replace("{followers}", user_info.follower_count).replace("{following}", user_info.following_count), user_info.pk)
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
        time.sleep(self.config.message.timeaftermessage)
        return self.MessageStatus.OK

    def likeAction(self, client: Client, user_info: types.User, user_media: types.Media):
        if self.testmode:return self.MediaStatus.OK
        try:
            if self.config.like.enabled_filters:
                if self.filter_check(self.config.like.filters, user_info):
                    time.sleep(self.config.like.timebefore)
                    client.media_like(user_media.id)
                    time.sleep(self.config.like.timeafter)
                    return self.MediaStatus.OK
            else:
                time.sleep(self.config.like.timebefore)
                client.media_like(user_media.id)
                time.sleep(self.config.like.timeafter)
                return self.MediaStatus.OK
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception:
            return self.MediaStatus.GENERAL_ERROR

    def commentAction(self, client: Client, userinfo: types.User, user_media: types.Media):
        if self.testmode:return self.MediaStatus.OK
        cmt = self.acquire_comment()
        try:
            if self.config.comment.enabled_filters:
                if self.filter_check(self.config.comment.filters, userinfo):
                    time.sleep(self.config.comment.timebeforecomment)
                    client.media_comment(user_media.id, cmt.replace("{username}", userinfo.username).replace(
                        "{name}", userinfo.full_name).replace("{followers}", userinfo.follower_count).replace("{following}", userinfo.following_count).replace("{likes}", user_media.like_count).replace("{comments}", user_media.comment_count))
                    time.sleep(self.config.comment.timeaftercomment)
                return self.MediaStatus.OK
            else:
                time.sleep(self.config.comment.timebeforecomment)
                client.media_comment(user_media.id, cmt)
                time.sleep(self.config.comment.timeaftercomment)
                return self.MediaStatus.OK
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception:
            return self.MediaStatus.GENERAL_ERROR

    def followAction(self, client: Client, user_info: types.User):
        if self.testmode:return self.UserStatus.OK
        try:
            if self.config.follow.enabled_filters:
                if self.filter_check(self.config.follow.filters, user_info):
                    time.sleep(self.config.follow.timebefore)
                    client.user_follow(user_info.pk)
                    time.sleep(self.config.follow.timeafter)
                    return self.UserStatus.OK
            else:
                time.sleep(self.config.follow.timebefore)
                client.user_follow(user_info.pk)
                time.sleep(self.config.follow.timeafter)
                return self.UserStatus.OK
            return self.UserStatus.OK
        except exceptions.UserNotFound:
            return self.UserStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.UserStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return self.UserStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.UserStatus.BANNED
        except Exception:
            return self.UserStatus.GENERAL_ERROR

    def get_user_info(self, client: Client, target: str) -> types.User | UserStatus:
        if self.testmode:return types.User(pk="123", username=target, full_name=target, is_private=True, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"),is_verified=random.random()>0.50,media_count=random.randint(0,100),follower_count=random.randint(0,10000),following_count=random.randint(0,1000),is_business=False)
        try:
            self.out.info(f"Loading target {target}")
            if target.isnumeric():
                self.out.info(f"target {target} is a UserID")
                return client.user_info(target)
            self.out.info(f"opening {target} page")
            return client.user_info_by_username(target)
        except exceptions.UserNotFound:
            return self.UserStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.UserStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return self.UserStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.UserStatus.BANNED
        except Exception as e:
            return self.UserStatus.GENERAL_ERROR

    def get_media_info(self, client: Client, target: types.User) -> types.Media | MediaStatus:
        if self.testmode:
            return types.Media(id="123", user=types.UserShort(pk=target.pk, username=target.username, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"), is_verified=random.random() > 0.50,is_private=random.random()>0.50), code="ABC123", taken_at=datetime.now(), like_count=random.randint(0, 1000), comment_count=random.randint(0, 100),pk=800,media_type=1,caption_text="",usertags=[],sponsor_tags=[])
        try:
            if target.media_count<1:
                return self.MediaStatus.NONE_AVAIABLE
            self.out.info(f"Loading media from {target}")
            return client.user_medias(target.pk, amount=1)[0]
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception as e:
            return self.MediaStatus.GENERAL_ERROR
    def login(self, client: Client,attempt_twice:bool=True,user:Dict[str,str]=None) -> LoginStatus:
        if user is not None:
            credentials = user
        else:
            credentials = self.acquire_user()
        self.out.info(f"Logging in to {credentials['username']}")
        if self.testmode:return self.LoginStatus.OK
        try:
            if self.check_cookies_exist(credentials["username"]):
                self.out.info("Found cookies for "+credentials["username"])
                cookies = self.get_cookies(credentials["username"])
                client.set_settings(cookies)
                try:
                    client.new_feed_exist()
                except:
                    try:client.logout()
                    except:pass
                    if attempt_twice:
                        self.out.warning("Failed to login, removing cookies and trying again...")
                        self.remove_cookies(credentials["username"])
                        return self.login(client, False, credentials)
                return self.LoginStatus.OK
            client.login(credentials["username"], credentials["password"])
            return self.LoginStatus.OK
        except exceptions.UserNotFound:
            return self.LoginStatus.BAD_USERNAME
        except exceptions.BadPassword:
            return self.LoginStatus.BAD_PASSWORD
        except exceptions.LoginRequired:
            return self.LoginStatus.LOGIN_REQUIRED
        except Exception as e:
            return self.LoginStatus.GENERAL_ERROR
class ProcessCore(ProcessUtils,InstaCore):
    userlist: List[Dict[str, str]]
    targetlist = List[str]
    config:Config
    out: ConsoleConnected
    testmode:bool = TEST_MODE

    def __init__(self, userlist, target, config, out: ConsoleConnected|InstaProcess, path:AppDataPaths,cookie_path:str, testMode: bool = False,parent:InstaProcess=None) -> None:
        self.userlist = userlist
        self.targetlist = target
        self.config = config
        self.out = out
        self.testMode = testMode
        self.path = path
        self.cookiepath = cookie_path
        self.parent=out
    
    def new_client(self) -> Client:
        proxy = None
        client = Client()
        client.challenge_code_handler = self.parent.obtain_code
        proxy = self.acquire_proxy()
        if proxy:
            self.out.info("Using proxy "+proxy)
            client.set_proxy(proxy)
        self.out.info("Initalized new Instagram Instance")
        return client
    def save_cookies(self, client: Client, username: str):
        if not os.path.exists(self.cookiepath):
            os.makedirs(self.cookiepath)
        client.dump_settings(os.path.join(self.cookiepath, f"{username}.json"))
    def run(self):
        print("Starting")
        while self.target_size()>0:
            print("Creating client")
            client = self.new_client()
            print("Logging in")
            status = self.login(client,attempt_twice=self.config.saveParams.twice_attempt)
            print("Logged in")
            if status != self.LoginStatus.OK:
                self.out.error(f"Failed to login status -> {status}")
                continue
            if self.config.saveParams.save_cookies or self.config.saveParams.save_session:
                self.save_cookies(client, client.username)
            print("Saved cookies")
            i = 0
            while i < self.config.usersforeachaccount:
                print("Starting loop")
                target = self.acquire_target()
                if target is None:
                    self.out.info(f"All targets have been interacted with")
                    self.out.info("Stopping process...")
                    break
                user_info = self.get_user_info(client, target)
                if isinstance(user_info, self.UserStatus):
                    self.anyLog(user_info, target)
                    match user_info:
                        case self.UserStatus.USER_NOT_FOUND:
                            self.out.error(f"User {target} not found")
                            continue
                        case self.UserStatus.UNREACHABLE:
                            self.out.error(f"User {target} is not reachable")
                            continue
                        case self.UserStatus.BLOCKED:
                            self.out.error(f"Account {client.username} is blocked")
                            break
                        case self.UserStatus.BANNED:
                            self.out.error(f"Account {client.username} is banned")
                            break
                        case self.UserStatus.GENERAL_ERROR:
                            self.out.error(f"Loading user {target} caused an error")
                            break
                else:
                    self.anyLog(self.UserStatus.OK, target)

                i+=1
                if not self.config.sendingParams.sendtoall:
                    if  (self.config.sendingParams.onlytononverified and user_info.is_verified):
                        self.out.info(f"User {target} is verified, skipping...")
                        self.anyLog(self.UserStatus.GENERAL_ERROR, target)
                        i-=1
                        continue
                    elif(self.config.sendingParams.onlytoverified and not user_info.is_verified):
                        self.out.info(f"User {target} is not verified, skipping...")
                        self.anyLog(self.UserStatus.GENERAL_ERROR, target)
                        i-=1
                        continue
                if self.config.message.enabled:
                    if (self.config.message.enabled_filters and self.filter_check(self.config.message.filters, user_info)) or not self.config.message.enabled_filters:
                        status = self.message(client,self.acquire_message(), user_info)
                        self.logMessage(status, target)
                        match status:
                            case self.MediaStatus.OK:
                                self.out.info(f"Message sent to {target}")
                            case self.MediaStatus.USER_NOT_FOUND:
                                self.out.error(f"User {target} not found")
                            case self.MediaStatus.UNREACHABLE:
                                self.out.error(f"User {target} is not reachable")
                            case self.MediaStatus.BLOCKED:
                                self.out.error(f"Account {client.username} is blocked")
                                break
                            case self.MediaStatus.BANNED:
                                self.out.error(f"Account {client.username} is banned")
                                break
                            case self.MediaStatus.GENERAL_ERROR:
                                self.out.error(f"Sending message to {target} caused an error")
                if self.config.follow.enabled:
                    if (self.config.follow.enabled_filters and self.filter_check(self.config.follow.filters, user_info)) or not self.config.follow.enabled_filters:
                        status = self.followAction(client, user_info)
                        self.logFollow(status, target)
                        match status:
                            case self.UserStatus.OK:
                                self.out.info(f"Followed {target}")
                            case self.UserStatus.USER_NOT_FOUND:
                                self.out.error(f"User {target} not found")
                            case self.UserStatus.UNREACHABLE:
                                self.out.error(f"User {target} is not reachable")
                            case self.UserStatus.BLOCKED:
                                self.out.error(f"Account {client.username} is blocked")
                                break
                            case self.UserStatus.BANNED:
                                self.out.error(f"Account {client.username} is banned")
                                break
                            case self.UserStatus.GENERAL_ERROR:
                                self.out.error(f"Following {target} caused an error")
                media_info = self.get_media_info(client, user_info)
                if isinstance(media_info, self.MediaStatus):
                    self.anyLog(media_info, target)
                    match media_info:
                        case self.MediaStatus.NONE_AVAIABLE:
                            self.out.info(f"No media available for {target}")
                        case self.MediaStatus.USER_NOT_FOUND:
                            self.out.error(f"User {target} not found")
                        case self.MediaStatus.UNREACHABLE:
                            self.out.error(f"User {target} is not reachable")
                        case self.MediaStatus.BLOCKED:
                            self.out.error(f"Account {client.username} is blocked")
                            break
                        case self.MediaStatus.BANNED:
                            self.out.error(f"Account {client.username} is banned")
                            break
                        case self.MediaStatus.GENERAL_ERROR:
                            self.out.error(f"Loading media from {target} caused an error")
                else:
                    self.anyLog(self.MediaStatus.OK, target)
                    if self.config.like.enabled:
                        if (self.config.like.enabled_filters and self.filter_check(self.config.like.filters, media_info)) or not self.config.like.enabled_filters:
                            status = self.likeAction(client, media_info)
                            self.logLike(status, target)
                            match status:
                                case self.MediaStatus.OK:
                                    self.out.info(f"Liked media from {target}")
                                case self.MediaStatus.USER_NOT_FOUND:
                                    self.out.error(f"User {target} not found")
                                case self.MediaStatus.UNREACHABLE:
                                    self.out.error(f"User {target} is not reachable")
                                case self.MediaStatus.BLOCKED:
                                    self.out.error(f"Account {client.username} is blocked")
                                    break
                                case self.MediaStatus.BANNED:
                                    self.out.error(f"Account {client.username} is banned")
                                    break
                                case self.MediaStatus.GENERAL_ERROR:
                                    self.out.error(f"Liking media from {target} caused an error")
                    if self.config.comment.enabled:
                        if (self.config.comment.enabled_filters and self.filter_check(self.config.comment.filters, media_info)) or not self.config.comment.enabled_filters:
                            status = self.commentAction(client, self.acquire_comment(), media_info)
                            self.logComment(status,target)
                            match status:
                                case self.MediaStatus.OK:
                                    self.out.info(f"Commented on media from {target}")
                                case self.MediaStatus.USER_NOT_FOUND:
                                    self.out.error(f"User {target} not found")
                                case self.MediaStatus.UNREACHABLE:
                                    self.out.error(f"User {target} is not reachable")
                                case self.MediaStatus.BLOCKED:
                                    self.out.error(f"Account {client.username} is blocked")
                                    break
                                case self.MediaStatus.BANNED:
                                    self.out.error(f"Account {client.username} is banned")
                                    break
                                case self.MediaStatus.GENERAL_ERROR:
                                    self.out.error(f"Commenting on media from {target} caused an error")
                if self.parent.stop:
                    self.out.info("Stopping process...")
                    self.anyLog(self.AnyStatus.OK,"Stopping process")
                    self.parent.stop = False
                    return
                if self.parent.logout:
                    self.out.info("Logging out...")
                    self.anyLog(self.AnyStatus.OK, "Logging out")
                    self.parent.logout = False
                    break
                time.sleep(10)
            if self.parent.stop:
                self.out.info("Stopping process...")
                self.anyLog(self.AnyStatus.OK, "Stopping process")
                return
