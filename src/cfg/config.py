import json


class Config:
    def __init__(self):
        self.cfg = self.load_config()

    def load_config(self):
        cfg = {}
        with open("src/cfg/keymapping_settings.json", "r") as file:
            cfg["keymapping"] = json.load(file)
        return cfg
