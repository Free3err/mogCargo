import pygame
import os

pygame.font.init()

class Font:
    MINECRAFT_FONT = {
        "title_bold": pygame.font.Font(os.path.join("src", "assets", "font", "minecraft_bold.otf"), 96),
        "title": pygame.font.Font(os.path.join("src", "assets", "font", "minecraft.ttf"), 96),
        "h2": pygame.font.Font(os.path.join("src", "assets", "font", "minecraft.ttf"), 36),
        "text": pygame.font.Font(os.path.join("src", "assets", "font", "minecraft.ttf"), 24),
        "small": pygame.font.Font(os.path.join("src", "assets", "font", "minecraft.ttf"), 20)
    }

developer_elem = Font.MINECRAFT_FONT["small"].render(
    "© free3err. MIT License", True, (255, 255, 255)
)
version_elem = Font.MINECRAFT_FONT["small"].render(
    "v0.1.2", True, (255, 255, 255)
)
