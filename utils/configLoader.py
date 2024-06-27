import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Filters:
    frequency: int
    minfollowers: int
    maxfollowers: int
    minmedia: int
    maxmedia: int


@dataclass
class Message:
    enabled: bool
    text: List[str] = field(default_factory=list)
    enabled_filters: bool = False
    filters: Filters = field(default_factory=lambda: Filters(1, 0, 0, 0, 0))
    timebeforemessage: int = 0
    timeaftermessage: int = 0


@dataclass
class Comment:
    enabled: bool
    text: List[str] = field(default_factory=list)
    enabled_filters: bool = False
    filters: Filters = field(default_factory=lambda: Filters(1, 0, 0, 0, 0))
    timebeforecomment: int = 0
    timeaftercomment: int = 0


@dataclass
class Action:
    enabled: bool
    enabled_filters: bool = False
    filters: Filters = field(default_factory=lambda: Filters(1, 0, 0, 0, 0))
    timebefore: int = 0
    timeafter: int = 0


@dataclass
class OtherTimings:
    loadinguser: dict
    accounttask: dict
    blockban: dict
    logout: dict


@dataclass
class SaveParams:
    to_json: bool = False
    to_csv: bool = False
    blocks: bool = False
    bans: bool = False
    twice_attempt: bool = False
    ask_for_code: bool = False
    save_cookies: bool = True
    save_session: bool = True


@dataclass
class SendingParams:
    onlytoverified: bool = False
    onlytononverified: bool = False
    sendtoall: bool = True


@dataclass
class Device:
    user_agent: dict
    user_agent_order: int


@dataclass
class Config:
    user_list: Path = "None"
    parallel:int = "None"
    accounts_list: Path = "None"
    exportType: int = 0
    usersforeachaccount: int = 0
    proxies: List[str] = field(default_factory=list)
    message: Message = field(default_factory=Message)
    comment: Comment = field(default_factory=Comment)
    like: Action = field(default_factory=lambda: Action(False))
    follow: Action = field(default_factory=lambda: Action(False))
    otherTimings: OtherTimings = field(default_factory=OtherTimings)
    saveParams: SaveParams = field(default_factory=SaveParams)
    sendingParams: SendingParams = field(default_factory=SendingParams)
    device: Device = field(default_factory=lambda: Device(
        {"iphone": False, "android": True}))


def open_config(path: str, dct:dict=None):
    if dct is not None:
        res = dct
    else:
        res = json.load(open(path))
    message = Message(
        enabled=res["message"]["enabled"],
        text=res["message"]["text"],
        enabled_filters=res["message"]["enabled_filters"],
        filters=Filters(**res["message"]["filters"]),
        timebeforemessage=res["message"]["timebeforemessage"],
        timeaftermessage=res["message"]["timeaftermessage"]
    )
    comment = Comment(
        enabled=res["comment"]["enabled"],
        text=res["comment"]["text"],
        enabled_filters=res["comment"]["enabled_filters"],
        filters=Filters(**res["comment"]["filters"]),
        timebeforecomment=res["comment"]["timebeforecomment"],
        timeaftercomment=res["comment"]["timeaftercomment"]
    )
    like = Action(
        enabled=res["like"]["enabled"],
        enabled_filters=res["like"]["enabled_filters"],
        filters=Filters(**res["like"]["filters"]),
        timebefore=res["like"]["timebeforelike"],
        timeafter=res["like"]["timeafterlike"]
    )
    follow = Action(
        enabled=res["follow"]["enabled"],
        enabled_filters=res["follow"]["enabled_filters"],
        filters=Filters(**res["follow"]["filters"]),
        timebefore=res["follow"]["timebeforefollow"],
        timeafter=res["follow"]["timeafterfollow"]
    )
    otherTimings = OtherTimings(
        loadinguser=res["otherTimings"]["loadinguser"],
        accounttask=res["otherTimings"]["accounttask"],
        blockban=res["otherTimings"]["blockban"],
        logout=res["otherTimings"]["logout"]
    )
    saveParams = SaveParams(
        to_json=res["saveParams"]["toJson"],
        to_csv=res["saveParams"]["toCSV"],
        blocks=res["saveParams"]["blocks"],
        bans=res["saveParams"]["bans"],
        twice_attempt=res["saveParams"]["twiceAttempt"],
        ask_for_code=res["saveParams"]["askForCode"],
        save_cookies=res["saveParams"]["saveCookies"],
        save_session=res["saveParams"]["saveSession"]
    )
    sendingParams = SendingParams(
        onlytoverified=res["sendingParams"]["onlytoverified"],
        onlytononverified=res["sendingParams"]["onlytononverified"],
        sendtoall=res["sendingParams"]["sendtoall"]
    )
    device = Device(
        user_agent=res["device"]["userAgent"],
        user_agent_order=res["device"]["userAgentOrder"]
    )
    return Config(
        user_list=Path(res["user_list"]),
        parallel=res["parallel"],
        accounts_list=Path(res["accounts_list"]),
        exportType=res["exportType"],
        usersforeachaccount=res["usersforeachaccount"],
        proxies=res["proxies"],
        message=message,
        comment=comment,
        like=like,
        follow=follow,
        otherTimings=otherTimings,
        saveParams=saveParams,
        sendingParams=sendingParams,
        device=device
    )
