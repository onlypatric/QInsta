from datetime import datetime
from enum import Enum
import os
from pathlib import Path
import re
import string
from threading import Thread,Lock
import time
import traceback
from requests import get,post
from typing import Dict, List, Tuple
from uuid import getnode
from instagrapi import Client,exceptions,types
from PyQt6.QtCore import QThread, pyqtSignal,pyqtSlot,QObject
from extracomps.ButtonHolder import ButtonHolder
from utils.configLoader import Config,Filters
from utils.ExtractionParams import ExtractionParams,TargetType
from extracomps.ConsoleWriter import ConsoleWriter
from extracomps.ConsoleList import ConsoleList
import pandas as pd
import json
from appdirs import user_data_dir
import random
import json
from .License import License,LicenseManager,ActionType
import hashlib
import platform
import psutil


def get_system_info():
    return {
        'cpu': platform.processor(),
        'cores': psutil.cpu_count(logical=False),
        'ram': psutil.virtual_memory().total,
        'name': platform.system()
    }


def system_info_to_hex(info):
    # Convert the dictionary to a string
    info_str = str(info)

    # Create a SHA-256 hash of the string
    hash_object = hashlib.sha256(info_str.encode())

    # Convert the hash to a hexadecimal string
    hex_dig = hash_object.hexdigest()

    return hex_dig

TEST_MODE = False
LICENSE_TYPE = License.BASIC
UAS = [
    "Instagram 323.0.0.35.65 Android (34/14; 480dpi; 1080x2290; realme; RMX3782; RE5C6CL1; mt6835; en_GB; 578014094)",
    "Instagram 317.0.0.34.109 Android (30/11; 480dpi; 1080x2098; TCL; T790Y; Seattle; qcom; it_IT; 563459864)",
    "Instagram 318.0.0.30.110 Android (34/14; 460dpi; 1080x2094; Google/google; Pixel 7 Pro; cheetah; cheetah; en_US; 566040990)",
    "Instagram 317.0.0.34.109 Android (31/12; 440dpi; 1080x2180; Xiaomi; M2007J3SG; apollo; qcom; de_DE; 563459864)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20F75 Instagram 341.0.1.29.93 (iPhone12,1; iOS 16_5_1;"]

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
class InstagramSignals:
    total = pyqtSignal()
    login = pyqtSignal()
    current_account = pyqtSignal(str)
    dms = pyqtSignal()
    comment = pyqtSignal()
    like = pyqtSignal()
    follow = pyqtSignal()
    banned = pyqtSignal()
    blocked = pyqtSignal()
    successful = pyqtSignal()
    dec_successful = pyqtSignal()
class CodeConnected:
    def obtain_code(self, for_: str, challenge_type: str):
        self.info(f"Asking verification code for {challenge_type}")
        self.request_input_code.emit(for_, str(challenge_type), self.code)
        while self.code.code is None:
            self.sleep(0.5)
        return self.code.obtainCode()
class InstaProcess(QThread, Readables, ConsoleConnected, InstagramSignals, CodeConnected):
    started = pyqtSignal()
    paused = pyqtSignal()
    finished = pyqtSignal()
    request_input_code = pyqtSignal(str,str,Code)
    log_output_signal = pyqtSignal(
        LogRegister, LogRegister, LogRegister, LogRegister, LogRegister)
    pause = False
    stop = False
    code = None
    def __init__(self, config:Config,buttons:ButtonHolder):
        super().__init__()
        self.code = Code()
        self.licenseType=LICENSE_TYPE
        self.config = config
        self.accepted = None
        self.buttons = buttons
        self.appdata = user_data_dir("QInsta","pstudios",roaming=True if os.name == "nt" else False)
        self.logins = LogRegister("Login")
        self.messages = LogRegister("Messages")
        self.comments = LogRegister("Comments")
        self.likes = LogRegister("Likes")
        self.follows = LogRegister("Follows")
        self.all = LogRegister("All")
        self.config_path = self.appdata
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path, exist_ok=True)
        self.cookiepath = os.path.join(self.config_path, "Cookies")
        self.log_path = os.path.join(self.config_path, "logs")
        os.makedirs(self.config_path,exist_ok=True)
        os.makedirs(self.cookiepath, exist_ok=True)
    def run(self):
        license_location = os.path.join(self.config_path, "LICENSE-KEY.txt")
        device_id = system_info_to_hex(get_system_info())
        BASE_URL = "https://patricpintescul.pythonanywhere.com"
        url = f"{BASE_URL}/check_and_add_device"
        license_info_url = f"{BASE_URL}/obtain_license_info"
        if not os.path.exists(license_location):
            self.critical("License file not found!")
            return
        elif len(open(license_location,"r").read())<5:
            self.critical("Invalid license key!")
            os.remove(license_location)
            return
        else:
            try:
                license_key = open(license_location, "r").read().strip()
                data = {
                    "license_name": license_key,
                    "device_id": device_id
                }
                response = post(url, json=data)
                license_name_data = {
                    "license_name": license_key
                }
                license_info_response = get(license_info_url, data=license_name_data,json=license_name_data,params=license_name_data)
                self.licenseType = License.BASIC
                if license_info_response.json().get("max_devices",None)==None:
                    self.critical(
                        "License does not exist or is full of registered computers")
                    os.remove(license_location)
                    return
                if license_info_response.json()["max_devices"]>2:
                    self.licenseType = License.PRO
                if response.json()["result"] == False:  # license is not valid
                    self.critical("License does not exist or is full of registered computers")
                    os.remove(license_location)
                    return
            except Exception as e:
                traceback.print_exc()
                self.critical(f"Error checking license, please retry: {e}")
                return
        ConsoleWriter.clear()
        valid_extensions = [".txt",".csv",".json",".xlsx"]
        self.parsedUserList=None
        if (self.config.follow.filters.maxmedia > 2137483647 and self.licenseType == License.BASIC) or\
                (self.licenseType == License.BASIC and any([self.config.downloadEmail,self.config.randomActions])):
            self.critical("Configuration file not valid, this configuration is for enterprise!")
            return
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

        self.info("Device settings are not yet supported...")
        ConsoleWriter.clear()
        self.started.emit()
        self.info("Starting script.")

        self.stop = False
        self.logout = False
        self.pc = ProcessCore(self.parsedUserList, self.parsedTargetList, self.config, self, self.appdata, self.cookiepath)
        self.buttons.enableAll()
        self.pc.run()
        self.buttons.disableAll()


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
        self.all.export(f"{dir}/all_{date}.txt")
class ProcessUtils:
    cookiepath:str
    config:Config
    userlist:List[Dict[str,str]]
    targetlist:List[str]
    license_tier:License

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
        if self.license_tier == License.FREE:
            return True
        if filter.minfollowers > user_info.follower_count:
            return False
        if (filter.maxfollowers < user_info.follower_count and filter.maxfollowers<filter.minfollowers) and filter.maxfollowers:
            return False
        if filter.minmedia > user_info.media_count:
            return False
        if filter.maxmedia < user_info.media_count and filter.maxmedia>filter.minmedia:
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
    
    def filter_targets(self,blacklist:"Blacklist"):# type: ignore
        self.targetlist = blacklist.filter_out(self.targetlist)

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
    def sleep(self,s:int):
        if s != 0:
            time.sleep(s)
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
        BANNED = 6
        BLOCKED = 7
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
    def logLogin(self, status: LoginStatus, username: str = None, password: str = None,cookies:bool=False):
        self.parent.logins.log(f"LOGIN FOR {username}:{self.maskPassword(password)} | STATUS -> {status} | COOKIES -> {cookies}")
        self.parent.all.log(f"LOGIN FOR {username}:{self.maskPassword(password)} | STATUS -> {status} | COOKIES -> {cookies}")
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
        if self.testmode:
            return random.choices([self.MessageStatus.OK, self.MessageStatus.GENERAL_ERROR, self.MessageStatus.USER_NOT_FOUND, self.MessageStatus.BANNED, self.MessageStatus.BLOCKED, self.MessageStatus.UNREACHABLE, self.MessageStatus.MEDIA_NOT_FOUND], weights=[0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])[0]
        self.sleep(self.config.message.timebeforemessage)
        for msg in msgcollection:
            # verify wether the "msg" contains any letter or number
            if not any(char.isalnum() for char in msg):
                continue
            if msg.startswith("@"):
                try:
                    client.direct_profile_share(client.user_info_by_username(
                        msg.replace("@", "")).pk, [user_info.pk])
                except exceptions.UserNotFound:
                    return self.MessageStatus.USER_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
                except (exceptions.ClientForbiddenError,exceptions.GenericRequestError,Exception):
                    return self.MessageStatus.GENERAL_ERROR
            elif msg.startswith("reel:"):
                try:
                    client.direct_media_share(client.media_info(
                        client.media_pk_from_url(msg.replace("reel:", ""))).id, [user_info.pk])
                except exceptions.MediaNotFound:
                    return self.MessageStatus.MEDIA_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
                except (exceptions.ClientForbiddenError, exceptions.GenericRequestError,Exception):
                    return self.MessageStatus.GENERAL_ERROR
            elif msg.startswith("post:"):
                try:
                    client.direct_media_share(client.media_info(
                        client.media_pk_from_url(msg.replace("post:", ""))).id, [user_info.pk])
                except exceptions.MediaNotFound:
                    return self.MessageStatus.MEDIA_NOT_FOUND
                except exceptions.PrivateAccount:
                    return self.MessageStatus.UNREACHABLE
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
                except (exceptions.ClientForbiddenError, exceptions.GenericRequestError,Exception):
                    return self.MessageStatus.GENERAL_ERROR
            else:
                try:
                    client.direct_send(msg.replace("{username}", str(user_info.username)).replace(
                        "{name}", str(user_info.full_name)).replace("{followers}", str(user_info.follower_count)).replace("{following}", str(user_info.following_count)), [user_info.pk])
                except exceptions.DirectError:
                    return self.MessageStatus.UNREACHABLE
                except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
                    return self.MessageStatus.BLOCKED
                except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
                    return self.MessageStatus.BANNED
                except (exceptions.ClientForbiddenError, exceptions.GenericRequestError,Exception):
                    return self.MessageStatus.GENERAL_ERROR
        self.sleep(self.config.message.timeaftermessage)
        return self.MessageStatus.OK

    def likeAction(self, client: Client, user_info: types.User, user_media: types.Media):
        if self.testmode:
            return random.choices([self.MediaStatus.OK, self.MediaStatus.BANNED, self.MediaStatus.BLOCKED, self.MediaStatus.UNREACHABLE, self.MediaStatus.GENERAL_ERROR, self.MediaStatus.USER_NOT_FOUND], weights=[0.9, 0.05, 0.05, 0.05, 0.05, 0.05])[0]
        try:
            if self.config.like.enabled_filters:
                if self.filter_check(self.config.like.filters, user_info):
                    self.sleep(self.config.like.timebefore)
                    client.media_like(user_media.id)
                    self.sleep(self.config.like.timeafter)
                    return self.MediaStatus.OK
            else:
                self.sleep(self.config.like.timebefore)
                client.media_like(user_media.id)
                self.sleep(self.config.like.timeafter)
                return self.MediaStatus.OK
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception:
            return self.MediaStatus.GENERAL_ERROR

    def commentAction(self, client: Client, userinfo: types.User, user_media: types.Media):
        if self.testmode:
            return random.choices([self.MediaStatus.OK, self.MediaStatus.BANNED, self.MediaStatus.BLOCKED, self.MediaStatus.UNREACHABLE, self.MediaStatus.GENERAL_ERROR, self.MediaStatus.USER_NOT_FOUND], weights=[0.9, 0.05, 0.05, 0.05, 0.05, 0.05])[0]
        cmt = self.acquire_comment()
        try:
            if self.config.comment.enabled_filters:
                if self.filter_check(self.config.comment.filters, userinfo):
                    self.sleep(self.config.comment.timebeforecomment)
                    client.media_comment(user_media.id, cmt.replace("{username}", userinfo.username).replace(
                        "{name}", userinfo.full_name).replace("{followers}", str(userinfo.follower_count)).replace("{following}", str(userinfo.following_count)).replace("{likes}", str(user_media.like_count)).replace("{comments}", str(user_media.comment_count)))
                    self.sleep(self.config.comment.timeaftercomment)
                return self.MediaStatus.OK
            else:
                self.sleep(self.config.comment.timebeforecomment)
                client.media_comment(user_media.id, cmt)
                self.sleep(self.config.comment.timeaftercomment)
                return self.MediaStatus.OK
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception:
            return self.MediaStatus.GENERAL_ERROR

    def followAction(self, client: Client, user_info: types.User):
        if self.testmode:
            return random.choices([self.UserStatus.OK, self.UserStatus.BANNED, self.UserStatus.BLOCKED, self.UserStatus.UNREACHABLE, self.UserStatus.GENERAL_ERROR, self.UserStatus.USER_NOT_FOUND], weights=[0.9, 0.05, 0.05, 0.05, 0.05, 0.05])[0]
        try:
            if self.config.follow.enabled_filters:
                if self.filter_check(self.config.follow.filters, user_info):
                    self.sleep(self.config.follow.timebefore)
                    client.user_follow(user_info.pk)
                    self.sleep(self.config.follow.timeafter)
                    return self.UserStatus.OK
            else:
                self.sleep(self.config.follow.timebefore)
                client.user_follow(user_info.pk)
                self.sleep(self.config.follow.timeafter)
                return self.UserStatus.OK
            return self.UserStatus.OK
        except exceptions.UserNotFound:
            return self.UserStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.UserStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.UserStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.UserStatus.BANNED
        except Exception:
            return self.UserStatus.GENERAL_ERROR
    def random_user_info(self,target:str):
        return types.User(pk="123", username=target, full_name=target, is_private=True, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"), is_verified=random.random() > 0.50, media_count=random.randint(0, 100), follower_count=random.randint(0, 10000), following_count=random.randint(0, 1000), is_business=False)
    def get_user_info(self, client: Client, target: str) -> types.User | UserStatus:
        try:
            if self.testmode:
                return random.choices([self.random_user_info(target), self.UserStatus.BANNED, self.UserStatus.BLOCKED, self.UserStatus.UNREACHABLE, self.UserStatus.GENERAL_ERROR,self.UserStatus.USER_NOT_FOUND], weights=[0.9, 0.05, 0.05, 0.05, 0.05,0.05])[0]
            if target.isnumeric():
                self.out.info(f"target {target} is a UserID")
                return client.user_info_v1(target)
            try:
                info1 = client.search_users_v1(target,10)[0]
                if info1.username==target:
                    self.out.info(f"Quick search found {target}")
                    return client.user_info_v1(info1)
                self.out.info(f"Opening {target}'s page")
                return client.user_info_by_username_v1(target)
            except Exception as e:
                return client.user_info_by_username_v1(target)
        except exceptions.UserNotFound:
            return self.UserStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.UserStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.UserStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.UserStatus.BANNED
        except Exception as e:
            self.out.warning(str(e))
            return self.UserStatus.GENERAL_ERROR
    def random_media(self,target:types.User) -> types.Media:
        return types.Media(id="123", user=types.UserShort(pk=target.pk, username=target.username, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"), is_verified=random.random() > 0.50,is_private=random.random()>0.50), code="ABC123", taken_at=datetime.now(), like_count=random.randint(0, 1000), comment_count=random.randint(0, 100),pk=800,media_type=1,caption_text="",usertags=[],sponsor_tags=[])
    def get_media_info(self, client: Client, target: types.User) -> types.Media | MediaStatus:
        try:
            if target.media_count<1:
                return self.MediaStatus.NONE_AVAIABLE
            if self.testmode:
                return random.choices([self.random_media(target), self.MediaStatus.BANNED, self.MediaStatus.BLOCKED, self.MediaStatus.MEDIA_NOT_FOUND, self.MediaStatus.GENERAL_ERROR], weights=[0.9, 0.05, 0.05, 0.05, 0.05])[0]
            return client.user_medias(target.pk, amount=1)[0]
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception as e:
            return self.MediaStatus.GENERAL_ERROR
    def random_actions(self, client:Client):
        try:
            match random.randint(0, 2):
                case 0:
                    if client.new_feed_exist():
                        client.get_timeline_feed()
                case 1:
                    client.media_seen([media.id for media in client.reels()])
                case 2:
                    client.explore_page()
                    client.explore_reels()
            return self.AnyStatus.OK
        except exceptions.PrivateAccount:
            return self.AnyStatus.UNREACHABLE
        except (exceptions.RateLimitError, exceptions.PleaseWaitFewMinutes):
            return self.AnyStatus.BLOCKED
        except (exceptions.ChallengeRequired, exceptions.ChallengeError, exceptions.ChallengeRedirection, exceptions.ChallengeSelfieCaptcha, exceptions.ChallengeUnknownStep, exceptions.RecaptchaChallengeForm):
            return self.AnyStatus.BANNED
        except Exception as e:
            return self.AnyStatus.GENERAL_ERROR
    def open_account(self, client:Client):
        try:
            client.get_timeline_feed()
            client.news_inbox_v1()
            return self.AnyStatus.OK
        except exceptions.PrivateAccount:
            return self.AnyStatus.UNREACHABLE
        except (exceptions.RateLimitError, exceptions.PleaseWaitFewMinutes):
            return self.AnyStatus.BLOCKED
        except (exceptions.ChallengeRequired, exceptions.ChallengeError, exceptions.ChallengeRedirection, exceptions.ChallengeSelfieCaptcha, exceptions.ChallengeUnknownStep, exceptions.RecaptchaChallengeForm):
            return self.AnyStatus.BANNED
        except Exception as e:
            return self.AnyStatus.GENERAL_ERROR
    def login(self, client: Client,attempt_twice:bool=True,user:Dict[str,str]=None) -> LoginStatus:
        if user is not None:
            credentials = user
        else:
            credentials = self.acquire_user()
        try:
            if self.check_cookies_exist(credentials["username"]) and not self.testmode:
                self.out.info("Found cookies for "+credentials["username"])
                cookies = self.get_cookies(credentials["username"])
                client.set_settings(cookies)
                try:
                    client.new_feed_exist()
                    client.user_info_by_username_v1("instagram")
                    self.logLogin(self.LoginStatus.OK,credentials['username'],credentials["password"])
                except:
                    try:client.logout()
                    except:pass
                    self.remove_cookies(credentials["username"])
                    self.anyLog(self.AnyStatus.GENERAL_ERROR,f"Cookies failed to load for {credentials['username']}")
                    if attempt_twice:
                        self.out.warning("Failed to login, removing cookies and trying again...")
                        return self.login(client, False, credentials)
                return self.LoginStatus.OK
            if self.testmode:
                client.username = credentials["username"]
                status =  random.choices([self.LoginStatus.OK, self.LoginStatus.BAD_PASSWORD, self.LoginStatus.BAD_USERNAME, self.LoginStatus.LOGIN_REQUIRED, self.LoginStatus.GENERAL_ERROR], weights=[0.9, 0.05, 0.05, 0.05, 0.05])[0]
                self.logLogin(self.LoginStatus.OK,credentials['username'], credentials["password"])
                return status
            client.login(credentials["username"], credentials["password"])
            self.logLogin(self.LoginStatus.OK,credentials['username'],credentials["password"])
            return self.LoginStatus.OK
        except exceptions.UserNotFound:
            self.logLogin(self.LoginStatus.BAD_USERNAME,credentials['username'],credentials["password"])
            return self.LoginStatus.BAD_USERNAME
        except exceptions.BadPassword:
            self.logLogin(self.LoginStatus.BAD_PASSWORD, credentials['username'], credentials["password"])
            return self.LoginStatus.BAD_PASSWORD
        except exceptions.LoginRequired:
            self.logLogin(self.LoginStatus.LOGIN_REQUIRED, credentials['username'], credentials["password"])
            return self.LoginStatus.LOGIN_REQUIRED
        except (exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeRequired,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            self.logLogin(self.LoginStatus.BANNED, credentials['username'], credentials["password"])
            return self.LoginStatus.BANNED
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            self.logLogin(self.LoginStatus.BLOCKED, credentials['username'], credentials["password"])
            self.out.error("Rate limit reached, please try again later.")
            return self.LoginStatus.BLOCKED
        except exceptions.ProxyAddressIsBlocked:
            self.logLogin(self.LoginStatus.BLOCKED, credentials['username'], credentials["password"])
            self.out.error("IP address is blocked, if you are using a proxy or VPN make sure it is not shared.")
            return self.LoginStatus.BLOCKED
        except Exception as e:
            import traceback
            self.logLogin(self.LoginStatus.GENERAL_ERROR, credentials['username'], credentials["password"])
            return self.LoginStatus.GENERAL_ERROR


class Blacklist:
    def __init__(self, path: str):
        self.path = path
        self.blacklist = self._load_blacklist()

    def _load_blacklist(self):
        if not os.path.exists(self.path):
            os.makedirs(str(Path(self.path).parent.absolute()),exist_ok=True)
            open(self.path,"x").close()
        with open(self.path, "r") as file:
            return set(file.read().splitlines())

    def add_user(self, username: str):
        if username not in self.blacklist:
            with open(self.path, "a") as file:
                file.write(username + "\n")
            self.blacklist.add(username)

    def filter_out(self, usernames: list[str]):
        return [x for x in usernames if x not in self.blacklist]

    def reload_blacklist(self):
        self.blacklist = self._load_blacklist()
class ProcessCore(ProcessUtils,InstaCore):
    userlist: List[Dict[str, str]]
    targetlist = List[str]
    config:Config
    out: ConsoleConnected
    testmode:bool = TEST_MODE

    def __init__(self, userlist, target, config, out: ConsoleConnected|InstaProcess, path:str,cookie_path:str, testmode: bool = False) -> None:
        self.userlist = userlist
        self.targetlist = target
        self.config = config
        self.out = out
        self.path = path
        self.cookiepath = cookie_path
        self.parent=out
        licpath = os.path.join(path, "data")
        if not os.path.exists(licpath):os.makedirs(licpath,exist_ok=True)
        self.blacklist_path = os.path.join(licpath, "blacklist.txt")
        self.license_tier = self.parent.licenseType
        self.license_manager = LicenseManager(os.path.join(licpath,"data.json"),self.license_tier)
    
    def new_client(self) -> Client:
        proxy = None
        client = Client()
        client.set_user_agent(random.choice(UAS))
        client.challenge_code_handler = self.parent.obtain_code if self.config.saveParams.ask_for_code else lambda x,y: "".join(random.choices("1234567890", k=6))
        proxy = self.acquire_proxy()
        if proxy:
            self.out.debug("Using proxy "+proxy)
            client.set_proxy(proxy)
        self.out.debug("Initalized new Instagram Instance")
        return client
    def save_cookies(self, client: Client, username: str):
        if self.testmode:return
        if not os.path.exists(self.cookiepath):
            os.makedirs(self.cookiepath)
        client.dump_settings(os.path.join(self.cookiepath, f"{username}.json"))
    def run(self):
        bl = Blacklist(self.blacklist_path)
        self.filter_targets(bl) # filter out old people that have been already interacted with
        # run until targets have been finished
        while self.target_size()>0:
            client = self.new_client() # create a new instagram connection
# ------------------------------------------------------------------ CHECK FOR STOP SIGNAL
            if self.parent.stop:
                self.out.info("Stopping process...")
                self.anyLog(self.AnyStatus.OK, "Stopping process")
                self.parent.stop = False
                return
# ------------------------------------------------------------------ END CHECK FOR STOP SIGNAL
            if self.license_manager.increment_login():
                self.out.warning("License limit reached, stopping process")
                return
# ------------------------------------------------------------------ LOGINS SECTION
            self.sleep(self.config.timebeforelogin)
            creds = self.acquire_user() # obtain credentials
            self.out.debug("Logging in to "+str(creds))
            username = creds["username"]
            status = self.login(client,attempt_twice=self.config.saveParams.twice_attempt,user=creds) # login using the credentials
            self.parent.login.emit()
            if status != self.LoginStatus.OK: # check if status is not "OK"
                if status == self.LoginStatus.BANNED:
                    self.parent.banned.emit()
                    self.sleep(int(self.config.otherTimings.blockban["ban"]))
                elif status == self.LoginStatus.BLOCKED:
                    self.parent.blocked.emit()
                    self.sleep(int(self.config.otherTimings.blockban["block"]))
                self.out.error(f"Failed to login status -> {status.name}")
                continue
            self.parent.successful.emit()
            self.out.info(f"Logged in as {creds['username']}")
            self.parent.current_account.emit(f"{creds['username']} | {self.maskPassword(creds['password'])}")
            if self.config.saveParams.save_cookies or self.config.saveParams.save_session:
                self.save_cookies(client, creds['username']) # save cookies
            downloadpath = None
            downloadpathfname = None
            if self.config.downloadEmail:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                downloadpathfname = datetime.now().strftime("QINSTA-download-%d-%m-%Y-%H.csv")
                downloadpath = os.path.join(desktop_path, downloadpathfname)
            if self.config.loginActions:
                status = self.open_account(client) # open account info
                if status != self.AnyStatus.OK:
                    self.out.error(f"Failed to open account information status -> {status.name}")
            self.sleep(self.config.timeafterlogin)
# ------------------------------------------------------------------ END LOGINS SECTION

# ------------------------------------------------------------------ CHECK FOR STOP SIGNAL
            if self.parent.stop:
                self.out.info("Stopping process...")
                self.anyLog(self.AnyStatus.OK, "Stopping process")
                self.parent.stop = False
                return
# ------------------------------------------------------------------ END CHECK FOR STOP SIGNAL
            i = 0
            try:
                while i < self.config.usersforeachaccount: # loop that goes from 0 to self.config.usersforeachaccount
    # ------------------------------------------------------------------ ACQUIRE TARGET
                    target = self.acquire_target() # obtain target
                    if self.license_manager.increment_interaction():
                        self.out.warning("License limit reached, stopping process")
                        return
                    i += 1
                    if target is None:
                        self.out.debug(f"All targets have been interacted with")
                        self.out.debug("Stopping process...")
                        break
    # ------------------------------------------------------------------ END ACQUIRE TARGET
    # ------------------------------------------------------------------ ACQUIRE USER INFO
                    if self.config.randomActions: # random actions if needed
                        status = self.random_actions(client) # execute it
                        if status == self.AnyStatus.BANNED:
                            self.parent.banned.emit()
                            self.sleep(int(self.config.otherTimings.blockban["ban"]))
                            self.parent.dec_successful.emit()
                            self.out.error(f"Account {client.username} is banned")
                            break
                        elif status == self.AnyStatus.BLOCKED:
                            self.parent.blocked.emit()
                            self.sleep(int(self.config.otherTimings.blockban["block"]))
                            self.parent.dec_successful.emit()
                            self.out.error(f"Account {client.username} is blocked")
                            break
                        elif status == self.AnyStatus.GENERAL_ERROR:
                            self.out.error(f"Random actions caused an error")
                            self.remove_cookies(creds["username"])
                            break
                        self.out.info(f"Executed random actions")
                    self.sleep(int(self.config.otherTimings.loadinguser["before"]))
                    self.out.debug(f"Loading {target}'s page")
                    user_info = self.get_user_info(client, target) # obtain user info
                    if isinstance(user_info, self.UserStatus):
                        self.anyLog(user_info, f"USER LOAD {target}")
                        match user_info:
                            case self.UserStatus.USER_NOT_FOUND:
                                self.out.error(f"User {target} not found")
                            case self.UserStatus.UNREACHABLE:
                                self.out.error(f"User {target} is not reachable")
                            case self.UserStatus.BLOCKED:
                                self.parent.blocked.emit()
                                self.sleep(int(self.config.otherTimings.blockban["block"]))
                                self.parent.dec_successful.emit()
                                self.out.error(f"Account {client.username} is blocked")
                                break
                            case self.UserStatus.BANNED:
                                self.parent.banned.emit()
                                self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                self.parent.dec_successful.emit()
                                self.out.error(f"Account {client.username} is banned")
                                break
                            case self.UserStatus.GENERAL_ERROR:
                                self.out.error(f"Loading user {target} caused an error")
                                self.remove_cookies(creds["username"])
                                break
                        continue
                    else:
                        self.out.info(f"Opened {target}'s page")
                        self.anyLog(self.UserStatus.OK, f"USER LOAD {target}")
                    self.sleep(int(self.config.otherTimings.loadinguser["after"]))
    # ------------------------------------------------------------------ END ACQUIRE USER INFO
    # ------------------------------------------------------------------ DOWNLOAD USER INFO
                    if downloadpath is not None and self.license_manager.license_type==License.PRO:
                        if not os.path.exists(downloadpath):
                            with open(downloadpath, "w") as file:
                                file.write("sep=,\nusername,full_name,public_email,public_phone,contact_phone,follower_count,following_count,userid\n")
                        user_export = f"{user_info.username},{user_info.full_name},{user_info.public_email},{str(user_info.public_phone_country_code)+str(user_info.public_phone_number)},{user_info.contact_phone_number},{user_info.follower_count},{user_info.following_count},{user_info.pk}\n"
                        with open(downloadpath, "a") as file:
                            file.write(user_export)
                        self.out.info(f"Exported {target} to {downloadpathfname}")
    # ------------------------------------------------------------------ END DOWNLOAD USER INFO
    # ------------------------------------------------------------------ CHECK SENDING PARAMETER
                    if not self.config.sendingParams.sendtoall:
                        if  (self.config.sendingParams.onlytononverified and user_info.is_verified):
                            self.out.warning(f"User {target} is verified, skipping...")
                            self.anyLog(self.UserStatus.GENERAL_ERROR, target)
                            i-=1
                            continue
                        elif(self.config.sendingParams.onlytoverified and not user_info.is_verified):
                            self.out.warning(f"User {target} is not verified, skipping...")
                            self.anyLog(self.UserStatus.GENERAL_ERROR, target)
                            i-=1
                            continue
                    bl.add_user(target)
    # ------------------------------------------------------------------ END CHECK SENDING PARAMETER
    # ------------------------------------------------------------------ LOAD MEDIA
                    if self.config.like.enabled or self.config.comment.enabled:
                        self.out.info(f"Loading media from {target}")
                        media_info = self.get_media_info(client, user_info)
                        if isinstance(media_info, self.MediaStatus):
                            self.anyLog(media_info, f"MEDIA LOAD {target}")
                            match media_info:
                                case self.MediaStatus.NONE_AVAIABLE:
                                    self.out.info(f"No media available for {target}")
                                case self.MediaStatus.USER_NOT_FOUND:
                                    self.out.error(f"User {target} not found")
                                case self.MediaStatus.UNREACHABLE:
                                    self.out.error(f"User {target} is not reachable")
                                case self.MediaStatus.BLOCKED:
                                    self.parent.blocked.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["block"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is blocked")
                                    break
                                case self.MediaStatus.BANNED:
                                    self.parent.banned.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is banned")
                                    break
                                case self.MediaStatus.GENERAL_ERROR:
                                    self.out.error(f"Loading media from {target} caused an error")
                        else:
                            self.out.info(f"Loaded media from {target}")
                            self.anyLog(self.MediaStatus.OK, f"MEDIA LOAD {target}")
    # ------------------------------------------------------------------ LIKE MEDIA
                            if self.config.like.enabled:
                                if (self.config.like.enabled_filters and self.filter_check(self.config.like.filters, user_info)) or not self.config.like.enabled_filters:
                                    self.sleep(self.config.like.timebefore)
                                    self.out.debug(f"Liking media from {target}")
                                    status = self.likeAction(client, user_info,media_info)
                                    self.logLike(status, target)
                                    match status:
                                        case self.MediaStatus.OK:
                                            self.parent.total.emit()
                                            self.parent.like.emit()
                                            self.out.info(f"Liked media from {target}")
                                        case self.MediaStatus.USER_NOT_FOUND:
                                            self.out.error(f"User {target} not found")
                                        case self.MediaStatus.UNREACHABLE:
                                            self.out.error(f"User {target} is not reachable")
                                        case self.MediaStatus.BLOCKED:
                                            self.parent.blocked.emit()
                                            self.sleep(int(self.config.otherTimings.blockban["block"]))
                                            self.parent.dec_successful.emit()
                                            self.out.error(f"Account {client.username} is blocked")
                                            break
                                        case self.MediaStatus.BANNED:
                                            self.parent.banned.emit()
                                            self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                            self.parent.dec_successful.emit()
                                            self.out.error(f"Account {client.username} is banned")
                                            break
                                        case self.MediaStatus.GENERAL_ERROR:
                                            self.out.error(f"Liking media from {target} caused an error")
                                    self.sleep(self.config.like.timeafter)
    # ------------------------------------------------------------------ END LIKE MEDIA
    # ------------------------------------------------------------------ COMMENT MEDIA
                            if self.config.comment.enabled:
                                if (self.config.comment.enabled_filters and self.filter_check(self.config.comment.filters, user_info)) or not self.config.comment.enabled_filters:
                                    self.sleep(self.config.comment.timebeforecomment)
                                    self.out.debug(f"Commenting on media from {target}")
                                    status = self.commentAction(client, user_info, media_info)
                                    self.logComment(status,target)
                                    match status:
                                        case self.MediaStatus.OK:
                                            self.parent.total.emit()
                                            self.parent.comment.emit()
                                            self.out.info(f"Commented on media from {target}")
                                        case self.MediaStatus.USER_NOT_FOUND:
                                            self.out.error(f"User {target} not found")
                                        case self.MediaStatus.UNREACHABLE:
                                            self.out.error(f"User {target} is not reachable")
                                        case self.MediaStatus.BLOCKED:
                                            self.parent.blocked.emit()
                                            self.sleep(int(self.config.otherTimings.blockban["block"]))
                                            self.parent.dec_successful.emit()
                                            self.out.error(f"Account {client.username} is blocked")
                                            break
                                        case self.MediaStatus.BANNED:
                                            self.parent.banned.emit()
                                            self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                            self.parent.dec_successful.emit()
                                            self.out.error(f"Account {client.username} is banned")
                                            break
                                        case self.MediaStatus.GENERAL_ERROR:
                                            self.out.error(f"Commenting on media from {target} caused an error")
                                    self.sleep(
                                        self.config.comment.timeaftercomment)
    # ------------------------------------------------------------------ END COMMENT MEDIA
    # ------------------------------------------------------------------ END LOAD MEDIA
    # ------------------------------------------------------------------ SEND MESSAGE
                    if self.config.message.enabled:
                        if self.config.message.enabled_filters:
                            self.filter_check(self.config.message.filters,user_info)
                        if (self.config.message.enabled_filters and self.filter_check(self.config.message.filters, user_info)) or not self.config.message.enabled_filters:
                            self.sleep(self.config.message.timebeforemessage)
                            self.out.debug(f"Reaching {target} through DMs")
                            status = self.message(client,self.acquire_message(), user_info)
                            self.logMessage(status, target)
                            match status:
                                case self.MessageStatus.OK:
                                    self.parent.total.emit()
                                    self.parent.dms.emit()
                                    self.out.info(f"Message sent to {target}")
                                case self.MessageStatus.USER_NOT_FOUND:
                                    self.out.error(f"User {target} not found")
                                case self.MessageStatus.UNREACHABLE:
                                    self.out.error(f"User {target} is not reachable")
                                case self.MessageStatus.BLOCKED:
                                    self.parent.blocked.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["block"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is blocked")
                                    break
                                case self.MessageStatus.BANNED:
                                    self.parent.banned.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is banned")
                                    break
                                case self.MessageStatus.GENERAL_ERROR:
                                    self.out.error(f"Could not send message to {target}")
                            self.sleep(self.config.message.timeaftermessage)
    # ------------------------------------------------------------------ END SEND MESSAGE
    # ------------------------------------------------------------------ FOLLOW TARGET
                    if self.config.follow.enabled:
                        if (self.config.follow.enabled_filters and self.filter_check(self.config.follow.filters, user_info)) or not self.config.follow.enabled_filters:
                            self.sleep(self.config.follow.timebefore)
                            self.out.debug(f"Following {target}")
                            status = self.followAction(client, user_info)
                            self.logFollow(status, target)
                            match status:
                                case self.UserStatus.OK:
                                    self.parent.total.emit()
                                    self.parent.follow.emit()
                                    self.out.info(f"Followed {target}")
                                case self.UserStatus.USER_NOT_FOUND:
                                    self.out.error(f"User {target} not found")
                                case self.UserStatus.UNREACHABLE:
                                    self.out.error(f"User {target} is not reachable")
                                case self.UserStatus.BLOCKED:
                                    self.parent.blocked.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["block"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is blocked")
                                    break
                                case self.UserStatus.BANNED:
                                    self.parent.banned.emit()
                                    self.sleep(int(self.config.otherTimings.blockban["ban"]))
                                    self.parent.dec_successful.emit()
                                    self.out.error(f"Account {client.username} is banned")
                                    break
                                case self.UserStatus.GENERAL_ERROR:
                                    self.out.error(f"Following {target} caused an error")
                                    break
                            self.sleep(self.config.follow.timeafter)
    # ------------------------------------------------------------------ END FOLLOW TARGET
    # ------------------------------------------------------------------ CHECK FOR STOP SIGNAL
                    if self.parent.stop:
                        self.out.info("Stopping process...")
                        self.anyLog(self.AnyStatus.OK,"Stopping process")
                        self.parent.stop = False
                        return
    # ------------------------------------------------------------------ END CHECK FOR STOP SIGNAL
    # ------------------------------------------------------------------ CHECK FOR LOGOUT SIGNAL
                    if self.parent.logout:
                        self.out.info("Logging out...")
                        self.anyLog(self.AnyStatus.OK, f"Logging out of {client.username}")
                        self.parent.logout = False
                        self.sleep(int(self.config.otherTimings.logout["after"])+int(self.config.otherTimings.logout["before"]))
                        break
    # ------------------------------------------------------------------ END CHECK FOR LOGOUT SIGNAL
            except Exception as exc:
                self.out.warning("An error occured during session "+str(exc)+" logging into new account...")
# ------------------------------------------------------------------ CHECK FOR STOP SIGNAL
            if self.parent.stop:
                self.out.info("Stopping process...")
                self.anyLog(self.AnyStatus.OK, "Stopping process")
                self.parent.stop = False
                return
# ------------------------------------------------------------------ END CHECK FOR STOP SIGNAL


class ExtractorCore(QThread, CodeConnected, ConsoleConnected):
    testmode: bool = TEST_MODE
    request_input_code = pyqtSignal(str, str, Code)
    code = Code()

    class LoginStatus(Enum):
        OK = 1
        BAD_PASSWORD = 2
        BAD_USERNAME = 3
        LOGIN_REQUIRED = 4
        GENERAL_ERROR = 5
        BLOCKED = 6
        BANNED = 7

    class UserStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
        MEDIA_NOT_FOUND = 6
    class MediaStatus(Enum):
        OK = 0
        GENERAL_ERROR = 1
        USER_NOT_FOUND = 2
        BANNED = 3
        BLOCKED = 4
        UNREACHABLE = 5
    def __init__(self, config:ExtractionParams,testmode: bool = False) -> None:
        QThread.__init__(self)
        self.config = config
        self.appdatapath = user_data_dir("EQInsta","pstudios",roaming=True if os.name=="nt" else False)
        self.cookiepath = os.path.join(self.appdatapath,"cookies/")
        if not os.path.exists(self.appdatapath):
            os.makedirs(self.appdatapath,exist_ok=True)

    def new_client(self) -> Client:
        client = Client()
        client.challenge_code_handler = self.obtain_code
        if self.config.proxy!="":
            self.debug("Using proxy "+self.config.proxy)
            client.set_proxy(self.config.proxy)
        self.debug("Initalized new Instagram Instance")
        return client

    def save_cookies(self, client: Client, username: str):
        if self.testmode:
            return
        if not os.path.exists(self.cookiepath):
            os.makedirs(self.cookiepath)
        client.dump_settings(os.path.join(self.cookiepath, f"{username}.json"))
    def remove_cookies(self, username: str):
        if self.testmode:
            return
        os.remove(os.path.join(self.cookiepath, f"{username}.json"))
    def get_cookies(self, username: str) -> dict:
        return Client.load_settings(os.path.join(self.cookiepath, f"{username}.json"))
    def check_cookies_exist(self, username: str) -> bool:
        return os.path.exists(os.path.join(self.cookiepath, f"{username}.json"))
    def login(self, client: Client, attempt_twice: bool = True, user: Dict[str, str] = None) -> LoginStatus:
        credentials = user
        try:
            if self.check_cookies_exist(credentials["username"]) and not self.testmode:
                self.info("Found cookies for "+credentials["username"])
                cookies = self.get_cookies(credentials["username"])
                client.set_settings(cookies)
                try:
                    client.new_feed_exist()
                except:
                    try:
                        client.logout()
                    except:
                        pass
                    self.remove_cookies(credentials["username"])
                    if attempt_twice:
                        self.warning(
                            "Failed to login, removing cookies and trying again...")
                        return self.login(client, False, credentials)
                return self.LoginStatus.OK
            if self.testmode:
                client.username = credentials["username"]
                status = random.choices([self.LoginStatus.OK, self.LoginStatus.BAD_PASSWORD, self.LoginStatus.BAD_USERNAME,
                                        self.LoginStatus.LOGIN_REQUIRED, self.LoginStatus.GENERAL_ERROR], weights=[0.9, 0.05, 0.05, 0.05, 0.05])[0]
                return status
            client.login(credentials["username"], credentials["password"])
            return self.LoginStatus.OK
        except exceptions.UserNotFound:
            return self.LoginStatus.BAD_USERNAME
        except exceptions.BadPassword:
            return self.LoginStatus.BAD_PASSWORD
        except exceptions.LoginRequired:
            return self.LoginStatus.LOGIN_REQUIRED
        except (exceptions.ChallengeError, exceptions.ChallengeRedirection, exceptions.ChallengeRequired, exceptions.ChallengeSelfieCaptcha, exceptions.ChallengeUnknownStep, exceptions.RecaptchaChallengeForm):
            return self.LoginStatus.BANNED
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            self.error("Rate limit reached, please try again later.")
            return self.LoginStatus.BLOCKED
        except exceptions.ProxyAddressIsBlocked:
            self.error(
                "IP address is blocked, if you are using a proxy or VPN make sure it is not shared.")
            return self.LoginStatus.BLOCKED
        except Exception as e:
            return self.LoginStatus.GENERAL_ERROR
    def random_user_info(self,target:str):
        return types.User(pk="123", username=target, full_name=target, is_private=True, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"), is_verified=random.random() > 0.50, media_count=random.randint(0, 100), follower_count=random.randint(0, 10000), following_count=random.randint(0, 1000), is_business=False)
    def get_user_info(self, client: Client, target: str) -> types.User | UserStatus:
        try:
            if self.testmode:
                return random.choices([self.random_user_info(target), self.UserStatus.BANNED, self.UserStatus.BLOCKED, self.UserStatus.UNREACHABLE, self.UserStatus.GENERAL_ERROR,self.UserStatus.USER_NOT_FOUND], weights=[0.9, 0.05, 0.05, 0.05, 0.05,0.05])[0]
            if target.isnumeric():
                self.info(f"target {target} is a UserID")
                return client.user_info(target)
            self.info(f"opening {target} page")
            return client.user_info_by_username(target)
        except exceptions.UserNotFound:
            return self.UserStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.UserStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.UserStatus.BLOCKED
        except (exceptions.ChallengeRequired,exceptions.ChallengeError,exceptions.ChallengeRedirection,exceptions.ChallengeSelfieCaptcha,exceptions.ChallengeUnknownStep,exceptions.RecaptchaChallengeForm):
            return self.UserStatus.BANNED
        except Exception as e:
            return self.UserStatus.GENERAL_ERROR

    def random_media(self, target: types.User) -> types.Media:
        return types.Media(id="123", user=types.UserShort(pk=target.pk, username=target.username, profile_pic_url=types.HttpUrl("https://www.google.com"), profile_pic_url_hd=types.HttpUrl("https://www.google.com"), is_verified=random.random() > 0.50, is_private=random.random() > 0.50), code="ABC123", taken_at=datetime.now(), like_count=random.randint(0, 1000), comment_count=random.randint(0, 100), pk=800, media_type=1, caption_text="", usertags=[], sponsor_tags=[])

    def get_media_info(self, client: Client, url: str) -> types.Media | MediaStatus:
        try:
            pk = client.media_pk_from_url(url)
            media_info = client.media_info(pk)
            return media_info
        except exceptions.UserNotFound:
            return self.MediaStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return self.MediaStatus.UNREACHABLE
        except (exceptions.RateLimitError,exceptions.PleaseWaitFewMinutes):
            return self.MediaStatus.BLOCKED
        except (exceptions.ChallengeRequired, exceptions.ChallengeError, exceptions.ChallengeRedirection, exceptions.ChallengeSelfieCaptcha, exceptions.ChallengeUnknownStep, exceptions.RecaptchaChallengeForm):
            return self.MediaStatus.BANNED
        except Exception as e:
            self.warning("ERROR -> "+str(e))
            return self.MediaStatus.GENERAL_ERROR
    def run(self) -> None:
        try:
            client = self.new_client()
            user = {"username": self.config.username, "password": self.config.password}
            self.debug(f"Logging in as {self.config.username}")
            status = self.login(client, True, user)
            if status == self.LoginStatus.OK:
                self.info(f"Successfully logged into {self.config.username}")
            else:
                self.error(f"Login failed, status -> {status.name}")
                return
            self.info("Waiting 1 minute to start process")
            time.sleep(60)
            self.debug("Starting extraction process")
            i = self.config.max_amount
            if not os.path.exists(self.config.output_path):
                os.makedirs(self.config.output_path,exist_ok=True)
            if self.config.target_type == TargetType.FOLLOWERS or self.config.target_type == TargetType.FOLLOWINGS:
                self.config.target = "".join(filter(lambda x: x in string.digits + string.ascii_letters + string.punctuation, self.config.target))
                user_info = self.get_user_info(client, self.config.target)
                if isinstance(user_info, self.UserStatus):
                    self.error(f"Failed to get user info, status -> {user_info.name}")
                    return
                self.debug(f"Getting {self.config.target_type.value} of {user_info.username}")
                max_id = self.config.max_id if self.config.max_id else ""
                
                with open(os.path.join(self.config.output_path, f"{user_info.username}-{self.config.max_amount}.txt"), "w",encoding="utf-8") as f, open(os.path.join(self.config.output_path, f"{user_info.username}-{self.config.max_amount}-FULL.csv"), "w",encoding="utf-8") as f2:
                    # set the separator in f2 to be ,
                    f2.write("sep=;\n")
                    f2.write("USERNAME;FULL_NAME;ACCOUNT_PRIVACY;USERID\n")
                    while i > 0:
                        if self.config.target_type == TargetType.FOLLOWERS:
                            try:
                                users, max_id = client.user_followers_gql_chunk(
                                    user_info.pk, max_amount=50,max_id=max_id)
                            except:
                                self.warning(
                                    "GQL API block, waiting for a random amount of time")
                                time.sleep(random.random()*10)
                                try:
                                    users,max_id = client.user_followers_v1_chunk(user_info.pk,max_amount=50,max_id=max_id)
                                except Exception as e:
                                    if "wait" in str(e):
                                        self.warning("Instagram limited the account, waiting 3 minutes before a new attempt")
                            self.info("Chunk of users downloaded, max_id:")
                            self.info(max_id)
                            for user in users:
                                i -= 1
                                f.write(user.username+"\n")
                                f2.write(f"{user.username};{user.full_name};{'PRIVATE' if user.is_private else 'PUBLIC'};{user.pk}\n")
                        elif self.config.target_type == TargetType.FOLLOWINGS:
                            time.sleep(random.random()*5)
                            try:
                                users, max_id = client.user_following_v1_chunk(user_info.pk, max_amount=50,max_id=max_id)
                            except Exception as e:
                                if "wait" in str(e):
                                    self.warning("Instagram limited the account, waiting 3 minutes before a new attempt")
                            self.info("Chunk of users downloaded, max_id:")
                            self.info(max_id)
                            for user in users:
                                i-=1
                                f.write(user.username+"\n")
                                f2.write(f"{user.username};{user.full_name};{'PRIVATE' if user.is_private else 'PUBLIC'};{user.pk}\n")
            elif self.config.target_type == TargetType.HASHTAGS:
                max_id=self.config.max_id if self.config.max_id else ""
                with open(os.path.join(self.config.output_path, f"{self.config.target}-{self.config.max_amount}.txt"), "w",encoding="utf-8") as f, open(os.path.join(self.config.output_path, f"{self.config.target}-{self.config.max_amount}-FULL.csv"), "w",encoding="utf-8") as f2:
                    f2.write("sep=;\n")
                    f2.write("USERNAME;FULL_NAME;ACCOUNT_PRIVACY;USERID;MEDIA_LIKES;MEDIA_COMMENTS\n")
                    while i > 0:
                        try:
                            client.hashtag_medias_a1_chunk(
                                self.config.target, max_id=max_id)
                        except:
                            self.warning("A1 API block, waiting for a random amount of time")
                            time.sleep(random.random()*10)
                            try:
                                medias,max_id = client.hashtag_medias_v1_chunk(self.config.target,max_id=max_id)
                            except Exception as e:
                                if "wait" in str(e):
                                    self.warning("Instagram limited the account, waiting 3 minutes before a new attempt")
                        self.info("Chunk of users downloaded, max_id:")
                        self.info(max_id)
                        for media in medias:
                            f.write(media.user.username+"\n")
                            f2.write(f"{media.user.username};{media.user.full_name};{'PRIVATE' if media.user.is_private else 'PUBLIC'};{media.user.pk};{media.like_count};{media.comment_count}\n")
                            i-=1
            elif self.config.target_type == TargetType.LIKES or self.config.target_type == TargetType.COMMENTS:
                media_info = self.get_media_info(client, self.config.target)
                if isinstance(media_info, self.MediaStatus):
                    self.error(f"Failed to load media, status -> {media_info.name}")
                    return
                with open(os.path.join(self.config.output_path, f"{media_info.code}-{self.config.max_amount}.txt"), "w",encoding="utf-8") as f, open(os.path.join(self.config.output_path, f"{media_info.code}-{self.config.max_amount}-FULL.csv"), "w",encoding="utf-8") as f2:
                    f2.write("sep=;\n")
                    f2.write("USERNAME;FULL_NAME;ACCOUNT_PRIVACY;USERID\n")
                    if self.config.target_type == TargetType.LIKES:
                        users = client.media_likers(media_info.pk)
                        for user in users:
                            f.write(user.username+"\n")
                            f2.write(f"{user.username};{user.full_name};{'PRIVATE' if user.is_private else 'PUBLIC'};{user.pk}\n")
                    elif self.config.target_type == TargetType.COMMENTS:
                        comments = client.media_comments(media_info.pk, min(media_info.comment_count,self.config.max_amount))
                        for comment in comments:
                            f.write(comment.user.username+"\n")
                            f2.write(f"{comment.user.username};{comment.user.full_name};{'PRIVATE' if comment.user.is_private else 'PUBLIC'};{comment.user.pk}\n")
            self.info(f"Done, extracted all {self.config.max_amount} users")
        except Exception as e:
            self.error(str(e))
            self.warning("Stopping extraction process")