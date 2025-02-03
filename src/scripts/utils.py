import pygame
import sys
import json

from ..cfg.config import Config

def terminate():
    with open("src/cfg/user_data.json", "w") as f:
        json.dump(Config.user_data, f, indent=4)
    pygame.quit()
    sys.exit()


