from datetime import datetime
from enum import Enum
import json
import os


class License(Enum):
    FREE = 0
    BASIC = 1
    PRO = 2


class ActionType(Enum):
    INTERACTION = "interaction"
    LOGIN = "login"


class LicenseManager:
    def __init__(self, json_path: str, license_type: License):
        self.json_path = json_path
        self.license_type = license_type
        self.date_key = datetime.now().strftime("%Y-%m-%d")
        self.actions = self.load_actions()

    def load_actions(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_actions(self):
        with open(self.json_path, 'w') as file:
            json.dump(self.actions, file)

    def get_today_actions(self, action_type: ActionType):
        if self.date_key not in self.actions:
            self.actions[self.date_key] = {
                ActionType.INTERACTION.value: 0, ActionType.LOGIN.value: 0}
        return self.actions[self.date_key][action_type.value]

    def update_today_actions(self, action_type: ActionType, new_action_count):
        if self.date_key not in self.actions:
            self.actions[self.date_key] = {
                ActionType.INTERACTION.value: 0, ActionType.LOGIN.value: 0}
        self.actions[self.date_key][action_type.value] = new_action_count
        self.save_actions()

    def increment_interaction(self) -> bool:
        actions_today = self.get_today_actions(ActionType.INTERACTION)
        actions_today += 1
        self.update_today_actions(ActionType.INTERACTION, actions_today)

        if self.license_type == License.FREE and actions_today > 25:
            return True
        elif self.license_type == License.BASIC and actions_today > 750:
            return True
        elif self.license_type == License.PRO:
            return False  # Pro users have unlimited actions

        return False

    def increment_login(self) -> bool:
        actions_today = self.get_today_actions(ActionType.LOGIN)
        actions_today += 1
        self.update_today_actions(ActionType.LOGIN, actions_today)

        if self.license_type == License.FREE and actions_today > 5:
            return True
        elif self.license_type == License.BASIC and actions_today > 100:
            return True
        elif self.license_type == License.PRO:
            return False  # Pro users have unlimited actions

        return False
