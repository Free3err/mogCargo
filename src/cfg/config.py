import json
import os


class Config:
    cfg = {}
    user_data = {}

    @classmethod
    def load_config(cls):
        with open(os.path.join("src", "cfg", "keymapping_settings.json"), "r") as file:
            cls.cfg["keymapping"] = json.load(file)
        with open(os.path.join("src", "cfg", "levels_cfg.json"), "r") as file:
            cls.cfg["levels"] = json.load(file)

    @classmethod 
    def initialize(cls):
        cls.load_config()
        cls.initialize_user_data()

    @classmethod
    def initialize_user_data(cls):
        with open(os.path.join("src", "cfg", "user_data.json"), "r") as f:
            cls.user_data = json.load(f)
            
        current_level = cls.user_data["level"]
        for level in cls.cfg["levels"]:
            if cls.cfg["levels"][level]["exp"] <= cls.user_data["exp"]:
                current_level = level
                
        if current_level != cls.user_data["level"]:
            cls.user_data["level"] = current_level
            cls.user_data["credits"] += cls.cfg["levels"][current_level]["credits"]
                
        current_exp = cls.user_data["exp"] - cls.cfg["levels"][current_level]["exp"]
        next_exp = cls.cfg["levels"][str(int(current_level) + 1)]["exp"] - cls.cfg["levels"][current_level]["exp"]
        cls.user_data["level_percent"] = current_exp / next_exp if next_exp > 0 else 1.0
        
        cls.user_data["exp"] -= cls.cfg["levels"][current_level]["exp"]
        
        with open(os.path.join("src", "cfg", "user_data.json"), "w") as f:
            json.dump(cls.user_data, f, indent=4)


Config.initialize()
