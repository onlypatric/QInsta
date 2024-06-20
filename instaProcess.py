from enum import Enum
import os
from pathlib import Path
import re
from threading import Thread,Lock
import time
from typing import Dict, List, Tuple
from instagrapi import Client,exceptions,types
from PyQt6.QtCore import QThread, pyqtSignal
from ButtonHolder import ButtonHolder
from configLoader import Config,Filters
from ConsoleWriter import ConsoleWriter
from ConsoleList import ConsoleList
import pandas as pd
import json
from appdata import AppDataPaths
import random
import json
class License(Enum):
    basic=0
    advanced=1
    pro=2
    unlimited=3

class SentStatus(Enum):
    OK = 0
    GENERAL_ERROR = 1
    USER_NOT_FOUND = 2
    BANNED = 3
    BLOCKED = 4
    UNREACHABLE = 5

class LoginStatus(Enum):
    OK = 0
    GENERAL_ERROR = 1
    BAD_PASSWORD = 2
    BAD_USERNAME = 3
    BAD_PROXY = 4
    LOGIN_REQUIRED = 5

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
                # check if separator is : or ; or , or . or /
                if file.readline().count(":") > 1:
                    sep = ":"
                elif file.readline().count(";") > 1:
                    sep = ";"
                elif file.readline().count(",") > 1:
                    sep = ","
                elif file.readline().count(".") > 1:
                    sep = "."
                elif file.readline().count("/") > 1:
                    sep = "/"
                if sep is None:
                    return False, []
                user_list = [
                    {
                        "username": line.split(":")[0],
                        "password": line.split(":")[1]
                    }
                    for line in file.readlines()
                ]
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
    request_input_code = pyqtSignal(str)
    pause = False
    stop = False
    code = None
    def __init__(self, config:Config,licenseType:License,buttons:ButtonHolder):
        super().__init__()
        self.licenseType=licenseType
        self.config = config
        self.accepted = None
        self.buttons = buttons
        self.appdata = AppDataPaths()
        self.config_path = self.appdata.get_config_path("QInsta",create=True)
        self.cookie_path = os.path.join(self.config_path, "/Cookies")
        self.log_path = os.path.join(self.config_path, "/logs")
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        if not os.path.exists(self.cookie_path):
            os.makedirs(self.cookie_path)
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

        self.finished.emit()

class ProcessCore:
    userlist: List[Dict[str, str]]
    targetlist = List[str]
    config:Config
    out: ConsoleConnected

    def __init__(self, userlist, target, config, out: ConsoleConnected, path:AppDataPaths,cookie_path:str, testMode: bool = False) -> None:
        self.userlist = userlist
        self.targetlist = target
        self.config = config
        self.out = out
        self.testMode = testMode
        self.userlock = Lock()
        self.targetlock = Lock()
        self.messagelock = Lock()
        self.commentlock = Lock()
        self.proxylock = Lock()
        self.path = path
        self.cookie_path = cookie_path
    
    def acquire_user(self) -> Dict[str,str]:
        self.userlock.acquire()
        if len(self.userlist) > 0:
            user = self.userlist.pop(0)
            self.userlist.append(user)
            self.userlock.release()
            return user
        self.userlock.release()
        return None
    def target_size(self) -> int:
        return len(self.targetlist)
    def acquire_target(self) -> str:
        self.targetlock.acquire()
        if len(self.targetlist) > 0:
            target = self.targetlist.pop(0)
            self.targetlock.release()
            return target
        self.targetlock.release()
        return None
    def acquire_message(self) -> List[str]:
        self.messagelock.acquire()
        if len(self.config.message.text) > 0:
            message = self.config.message.text.pop(0)
            self.config.message.text.append(message)
            self.messagelock.release()
            return ProcessUtils.process_strings(message)
        self.messagelock.release()
        return None
    def acquire_comment(self) -> str:
        self.commentlock.acquire()
        if len(self.config.comment.text) > 0:
            comment = self.config.comment.text.pop(0)
            self.config.comment.text.append(comment)
            self.commentlock.release()
            return comment
        self.commentlock.release()
        return None
    def acquire_proxy(self) -> str:
        self.proxylock.acquire()
        if len(self.config.proxies) > 0:
            proxy = self.config.proxies.pop(0)
            self.config.proxies.append(proxy)
            self.proxylock.release()
            return proxy
        self.proxylock.release()
        return None
    def check_cookies_exist(self,username:str) -> bool:
        return os.path.exists(os.path.join(self.cookie_path,f"{username}.json"))
    def get_cookies(self, username:str) -> Dict[str,str]:
        if not self.check_cookies_exist(username):
            return None
        with open(os.path.join(self.cookie_path, f"{username}.json"), "r") as file:
            return json.load(file)


class ProcessThread(Thread):
    targetlist: List[str]
    config: Config
    out: ConsoleConnected
    def __init__(self, config, out: ConsoleConnected, testMode: bool = False,parent:ProcessCore=None,path:AppDataPaths=None,cookiepath:str=None) -> None:
        self.config = config
        self.out = out
        self.testMode = testMode
        self.parent = parent
        self.path = path
        self.cookiepath = cookiepath
    def new_client(self) -> Client:
        proxy = None
        client = Client()
        proxy = self.parent.acquire_proxy()
        if proxy:
            self.out.info(self.name+"| Using proxy "+proxy)
            client.set_proxy(proxy)
        self.out.info(self.name+"| Initalized new Instagram Instance")
        return client
    def maskPassword(self, password:str) -> str:
        return password[0]+("*"*(len(password)-2))+password[-1]
    def login(self,client:Client,username:str=None,password:str=None) -> LoginStatus:
        self.out.info("Logging in...")
        if username is None and password is None:
            userdata = self.parent.acquire_user()
            username = userdata["username"]
            password = userdata["password"]
        try:
            cookies = self.parent.get_cookies(username)
            if cookies:
                try:
                    client.set_settings(cookies)
                    client.new_feed_exist()
                except:
                    self.out.warning(
                        self.name+"| Failed to load cookies, attempting normal login")
                    client.login(username, password,
                                relogin=self.config.saveParams.twice_attempt)
            else:
                client.login(username, password,relogin=self.config.saveParams.twice_attempt)
            self.out.info(f"{self.name}| Logged in as {username} with password {self.maskPassword(password)}")
            return LoginStatus.OK
        except exceptions.BadCredentials as e:
            self.out.error(f"{self.name}| Password {self.maskPassword(password)} is marked as wrong when attempting to login as {username}")
            return LoginStatus.BAD_PASSWORD
        except exceptions.UserNotFound as e:
            self.out.error(f"{self.name}| Username {username} is marked as not existent when attempting to login as {username}")
            return LoginStatus.BAD_USERNAME
        except exceptions.ProxyAddressIsBlocked as e:
            self.out.error(f"{self.name}| Proxy {client.proxy} has connection issues or is banned by Instagram.")
            return LoginStatus.BAD_PROXY
        except exceptions.LoginRequired as e:
            self.out.error(f"{self.name}| Login has been blocked for {username} with password {self.maskPassword(password)}")
            return LoginStatus.LOGIN_REQUIRED
        except exceptions.TwoFactorRequired as e:
            self.out.error(f"{self.name}| 2FA required for {username} with password {self.maskPassword(password)}")
            return LoginStatus.LOGIN_REQUIRED
        except exceptions.ChallengeRequired:
            self.out.error(f"{self.name}| Challenge required for {username} with password {self.maskPassword(password)}")
            return LoginStatus.LOGIN_REQUIRED
        except exceptions.RateLimitError:
            self.out.error(f"{self.name}| Rate limit error for {username} with password {self.maskPassword(password)}")
            return LoginStatus.GENERAL_ERROR
        except exceptions.ReloginAttemptExceeded:
            self.out.error(f"{self.name}| Relogin attempt exceeded for {username} with password {self.maskPassword(password)}")
            return LoginStatus.GENERAL_ERROR
        except exceptions.ClientError:
            self.out.error(f"{self.name}| Client error for {username} with password {self.maskPassword(password)}")
            return LoginStatus.GENERAL_ERROR
        except Exception as e:
            self.out.error(f"{self.name}| Login failed when attempting to login as {username} with password {self.maskPassword(password)}")
            self.out.error(str(e))
            return LoginStatus.GENERAL_ERROR
    def sendMessage(self,client:Client,user_info:types.User):
        if not self.config.message.enabled:
            return None
        message = self.parent.acquire_message(self.config.message.text)
        return self._action_message_send(client, message, user_info)
    def _action_message_send(self,client:Client,fullmessage:List[str],userinfo:types.User):
        try:
            for msg in fullmessage:
                if msg.startswith("@"):
                    try:
                        client.direct_profile_share(client.user_info_by_username(msg.replace("@", "")).pk, userinfo.pk)
                    except exceptions.UserNotFound:
                        self.out.error(f"Cannot share profile {msg} because the account is not found")
                elif msg.startswith("reel:"):
                    client.direct_media_share(client.media_info(client.media_pk_from_url(msg.replace("reel:", ""))).id(), userinfo.pk)
                elif msg.startswith("post:"):
                    client.direct_media_share(client.media_info(client.media_pk_from_url(msg.replace("post:", ""))).id(), userinfo.pk)
                else:
                    client.direct_send(msg.replace("{username}", userinfo.username).replace(
                        "{name}", userinfo.full_name).replace("{followers}", userinfo.follower_count).replace("{following}", userinfo.following_count), userinfo.pk)
            return SentStatus.OK
        except exceptions.UserNotFound:
            return SentStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return SentStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return SentStatus.BLOCKED
        except exceptions.ChallengeRequired:
            return SentStatus.BANNED
        except Exception as e:
            return SentStatus.GENERAL_ERROR
    def filter_check(self,filter:Filters,user_info:types.User) -> bool:
        if filter.minfollowers>user_info.follower_count:
            return False
        if filter.maxfollowers<user_info.follower_count:
            return False
        if filter.minmedia>user_info.media_count:
            return False
        if filter.maxmedia<user_info.media_count:
            return False
        return True
    def likeAction(self,client:Client,user_info:types.User,user_media:types.Media):
        if self.config.like.enabled and self.config.like.enabled_filters:
            if self.filter_check(self.config.like.filters,user_info):
                try:
                    client.media_like(user_media.id)
                    return SentStatus.OK
                except exceptions.UserNotFound:
                    return SentStatus.USER_NOT_FOUND
                except exceptions.PrivateAccount:
                    return SentStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return SentStatus.BLOCKED
                except exceptions.ChallengeRequired:
                    return SentStatus.BANNED
                except Exception:
                    return SentStatus.GENERAL_ERROR
        elif self.config.like.enabled:
            try:
                client.media_like(user_media.id)
                return SentStatus.OK
            except exceptions.UserNotFound:
                return SentStatus.USER_NOT_FOUND
            except exceptions.PrivateAccount:
                return SentStatus.UNREACHABLE
            except exceptions.RateLimitError:
                return SentStatus.BLOCKED
            except exceptions.ChallengeRequired:
                return SentStatus.BANNED
            except Exception:
                return SentStatus.GENERAL_ERROR

    def commentAction(self,client:Client,userinfo:types.User,user_media:types.Media):
        if self.config.comment.enabled:
            cmt = self.parent.acquire_comment()
            if self.config.comment.enabled_filters:
                if self.filter_check(self.config.comment.filters, userinfo):
                    try:
                        client.media_comment(user_media.id, cmt.replace("{username}", userinfo.username).replace(
                            "{name}", userinfo.full_name).replace("{followers}", userinfo.follower_count).replace("{following}", userinfo.following_count).replace("{likes}",user_media.like_count).replace("{comments}",user_media.comment_count))
                        return SentStatus.OK
                    except exceptions.UserNotFound:
                        return SentStatus.USER_NOT_FOUND
                    except exceptions.PrivateAccount:
                        return SentStatus.UNREACHABLE
                    except exceptions.RateLimitError:
                        return SentStatus.BLOCKED
                    except exceptions.ChallengeRequired:
                        return SentStatus.BANNED
                    except Exception:
                        return SentStatus.GENERAL_ERROR
            else:
                try:
                    client.media_comment(user_media.id, cmt)
                    return SentStatus.OK
                except exceptions.UserNotFound:
                    return SentStatus.USER_NOT_FOUND
                except exceptions.PrivateAccount:
                    return SentStatus.UNREACHABLE
                except exceptions.RateLimitError:
                    return SentStatus.BLOCKED
                except exceptions.ChallengeRequired:
                    return SentStatus.BANNED
                except Exception:
                    return SentStatus.GENERAL_ERROR
    def followAction(self, client:Client, user_info:types.User):
        if self.config.follow.enabled:
            try:
                client.user_follow(user_info.pk)
                return SentStatus.OK
            except exceptions.UserNotFound:
                return SentStatus.USER_NOT_FOUND
            except exceptions.PrivateAccount:
                return SentStatus.UNREACHABLE
            except exceptions.RateLimitError:
                return SentStatus.BLOCKED
            except exceptions.ChallengeRequired:
                return SentStatus.BANNED
            except Exception:
                return SentStatus.GENERAL_ERROR
    def get_user_info(self, client:Client, target:str) -> types.User | SentStatus:
        try:
            self.out.info(f"{self.name}| Loading target {target}")
            if target.isnumeric():
                self.out.info(f"{self.name}| target {target} is a UserID")
                return client.user_info(target)
            self.out.info(f"{self.name}| opening {target} page")
            return client.user_info_by_username(target)
        except exceptions.UserNotFound:
            return SentStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return SentStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return SentStatus.BLOCKED
        except exceptions.ChallengeRequired:
            return SentStatus.BANNED
        except Exception as e:
            self.out.error(f"{self.name}| ERROR: {e}")
            return SentStatus.GENERAL_ERROR
    def get_media_info(self, client:Client, target:types.User) -> types.Media | SentStatus:
        try:
            self.out.info(f"{self.name}| Loading target {target}")
            return client.user_medias(target.pk,amount=1)[0]
        except exceptions.UserNotFound:
            return SentStatus.USER_NOT_FOUND
        except exceptions.PrivateAccount:
            return SentStatus.UNREACHABLE
        except exceptions.RateLimitError:
            return SentStatus.BLOCKED
        except exceptions.ChallengeRequired:
            return SentStatus.BANNED
        except Exception as e:
            self.out.error(f"{self.name}| ERROR: {e}")
            return SentStatus.GENERAL_ERROR
    def run(self):
        while self.parent.target_size()>0:
            client = self.new_client()
            status = self.login(client)
            if status != LoginStatus.OK:
                continue
            if self.config.saveParams.save_cookies or self.config.saveParams.save_session:
                if not os.path.exists(self.cookiepath):
                    os.makedirs(self.cookiepath)
                client.dump_settings(os.path.join(self.cookiepath,f"{client.username}.json"))
            for i in range(self.config.usersforeachaccount):
                target = self.parent.acquire_target()
                if target is None:
                    self.out.info(f"{self.name}| No more targets to choose from...")
                    break
                userinfo = self.get_user_info(client, target)
                if isinstance(userinfo, SentStatus):
                    self.out.error(f"{self.name}| Failed to get user info for {target} due to {userinfo.name}")
                    if userinfo == SentStatus.BANNED:
                        self.out.info(f"{self.name}| Banned account, exiting...")
                        break
                    elif userinfo == SentStatus.BLOCKED:
                        self.out.info(f"{self.name}| Account is rate limited, exiting...")
                        break
                    continue
                if self.config.follow.enabled:
                    self.followAction(client, userinfo)
                if self.config.message.enabled:
                    self.sendMessage(client, target)
                if userinfo.media_count>0:
                    usermedia = self.get_media_info(client,userinfo)
                    if isinstance(usermedia, SentStatus):
                        self.out.error(f"{self.name}| Failed to get media info for {target} due to {usermedia.name}")
                        if usermedia == SentStatus.BANNED:
                            self.out.info(f"{self.name}| Banned account, exiting...")
                            break
                        elif usermedia == SentStatus.BLOCKED:
                            self.out.info(f"{self.name}| Account is rate limited, exiting...")
                            break
                        continue
                    if self.config.like.enabled:
                        self.likeAction(client, userinfo, usermedia)
                    if self.config.comment.enabled:
                        self.commentAction(client, userinfo, usermedia)
            self.out.info(f"{self.name}| Finished, stopping for {self.config.otherTimings.logout} seconds")

class ProcessUtils:
    @staticmethod
    def process_strings(array):
        # Step 1: Extract and save the first string, then append it to the end of the array
        first_string = array.pop(0)
        array.append(first_string)

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
