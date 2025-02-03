import json
import os
from .main import Game

def create_default_configs():
    cfg_dir = os.path.join(os.path.dirname(__file__), 'cfg')
    try:
        os.makedirs(cfg_dir, exist_ok=False)
    except FileExistsError:
        return

    keymapping = {
        "up": 119,
        "break": 32,
        "left": 97,
        "right": 100,
        "boost": 1073742049,
        "shot": 13,
        "shield": 113,
        "interaction": 101
    }
    levels = {
        str(i): {
            "exp": exp,
            "credits": credits
        } for i, (exp, credits) in enumerate([
            (0, 0),
            (50, 100),
            (100, 200),
            (200, 200),
            (300, 200),
            (1000, 1000),
            (1500, 300),
            (2000, 300),
            (3000, 2000),
            (4000, 2000),
            (5000, 2000),
            (6000, 1000),
            (7000, 1000)
        ])
    }
    user_data = {
        "exp": 20,
        "level": "0",
        "level_percent": 0.4,
        "credits": 200,
        "boost_time": 10,
        "boost_multiplier": 1.5,
        "boost_cooldown": 30,
        "shield_time": 15,
        "shield_cooldown": 45,
        "max_speed": 8,
        "hp": 4
    }
    default_configs = {
        "keymapping_settings.json": keymapping,
        "levels_cfg.json": levels,
        "user_data.json": user_data
    }
    for filename, data in default_configs.items():
        filepath = os.path.join(cfg_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
create_default_configs()
game = Game()