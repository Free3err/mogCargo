import pygame
import os

from ctypes import windll

pygame.font.init()


class Font:
    MINECRAFT_FONT = {
        "title_bold": pygame.font.Font(
            os.path.join("src", "assets", "font", "minecraft_bold.otf"), 96
        ),
        "title": pygame.font.Font(
            os.path.join("src", "assets", "font", "minecraft.ttf"), 96
        ),
        "h2": pygame.font.Font(
            os.path.join("src", "assets", "font", "minecraft.ttf"), 36
        ),
        "text": pygame.font.Font(
            os.path.join("src", "assets", "font", "minecraft.ttf"), 24
        ),
        "small": pygame.font.Font(
            os.path.join("src", "assets", "font", "minecraft.ttf"), 20
        ),
    }


class Device:
    user32 = windll.user32
    SCREEN_WIDTH = user32.GetSystemMetrics(0)
    SCREEN_HEIGHT = user32.GetSystemMetrics(1)
    SCREEN_REFRESH_RATE = 120


developer_elem = Font.MINECRAFT_FONT["small"].render(
    "© free3err. GNU GPL v3.0 License", True, (255, 255, 255)
)
version_elem = Font.MINECRAFT_FONT["small"].render("v0.5.0", True, (255, 255, 255))
