import pygame
import json

from ctypes import windll

from ..constants import Font, developer_elem, version_elem

user32 = windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


def get_btn(key):
    with open("src/cfg/keymapping_settings.json", "r") as f:
        keymapping = json.load(f)
    key_code = keymapping[key]
    return chr(key_code).upper()


class HUD:
    def __init__(self):
        """
        Инициализация HUD
        """
        self.elements = None
        self.cursor = pygame.image.load("src/assets/img/HUD/cursor.png")
        self.cursor = pygame.transform.scale(self.cursor, (24, 34))
        pygame.mouse.set_visible(False)

        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.last_mouse_pos = pygame.mouse.get_pos()

    def render(self, surface, bg_color=(15, 7, 36)):
        """
        Отрисовка HUD
        """
        surface.fill(bg_color)

        if hasattr(self, "has_moving_background") and self.has_moving_background:
            current_mouse_pos = pygame.mouse.get_pos()
            mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]
            mouse_dy = current_mouse_pos[1] - self.last_mouse_pos[1]

            self.bg_offset_x = max(-100, min(0, self.bg_offset_x - mouse_dx * 0.1))
            self.bg_offset_y = max(-100, min(0, self.bg_offset_y - mouse_dy * 0.1))

            if hasattr(self, "additions") and "background" in self.additions:
                surface.blit(
                    pygame.transform.scale(
                        self.additions["background"],
                        (SCREEN_WIDTH + 100, SCREEN_HEIGHT + 100),
                    ),
                    (self.bg_offset_x, self.bg_offset_y),
                )

            self.last_mouse_pos = current_mouse_pos
        else:
            surface.blit(
                pygame.transform.scale(
                    self.additions["background"],
                    (SCREEN_WIDTH + 100, SCREEN_HEIGHT + 100),
                ),
                (0, 0),
            )

        for key, value in self.elements.items():
            if isinstance(value, pygame.Rect):
                rect = pygame.Surface((value.width, value.height))
                rect.fill((50, 50, 50))
                surface.blit(rect, value)
                if key in self.additions["button_texts"]:
                    text = Font.MINECRAFT_FONT["text"].render(
                        self.additions["button_texts"][key], True, (255, 255, 255)
                    )
                    text_rect = text.get_rect(center=value.center)
                    surface.blit(text, text_rect)
            elif isinstance(value, pygame.Surface):
                if (
                    key in self.additions
                    and isinstance(self.additions[key], dict)
                    and "pos" in self.additions[key]
                ):
                    surface.blit(value, self.additions[key]["pos"])

        mouse_pos = pygame.mouse.get_pos()
        surface.blit(self.cursor, (mouse_pos[0], mouse_pos[1]))


class MainMenu(HUD):
    def __init__(self):
        """
        Инициализация HUD главного меню
        """
        super().__init__()

        self.has_moving_background = True

        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("src/assets/audio/menu_music.mp3")
        self.background_music.play(loops=-1)

        button_width = 300
        button_height = 60
        button_spacing = 60

        self.elements = {
            "start_game": pygame.Rect(
                CENTER_X - button_width // 2,
                CENTER_Y - button_spacing * 2,
                button_width,
                button_height,
            ),
            "settings": pygame.Rect(
                CENTER_X - button_width // 2,
                CENTER_Y - button_spacing * 0.5,
                button_width,
                button_height,
            ),
            "education": pygame.Rect(
                CENTER_X - button_width // 2,
                CENTER_Y + button_spacing,
                button_width,
                button_height,
            ),
            "exit": pygame.Rect(
                CENTER_X - button_width // 2,
                CENTER_Y + button_spacing * 2.5,
                button_width,
                button_height,
            ),
            "title": Font.MINECRAFT_FONT["title"].render(
                "MogCargo />", True, (255, 255, 255)
            ),
            "version": version_elem,
            "developer": developer_elem,
        }

        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "title": {
                "pos": (
                    CENTER_X - self.elements["title"].get_width() // 2,
                    CENTER_Y - 300,
                )
            },
            "version": {
                "pos": (
                    SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (5, SCREEN_HEIGHT - self.elements["developer"].get_height() - 5)
            },
            "button_texts": {
                "start_game": "Начать игру",
                "settings": "Настройки",
                "education": "Обучение",
                "exit": "Выйти",
            },
        }


class SettingsMenu(HUD):
    def __init__(self):
        super().__init__()
        self.has_moving_background = True
        self.update_elements()

    def update_elements(self):
        button_size = 60
        button_spacing = 80

        self.elements = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "description": Font.MINECRAFT_FONT["small"].render(
                "Нажмите на кнопку, чтобы изменить кнопку", True, (255, 255, 255)
            ),
            "up_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y - button_spacing * 2 + 20,
                button_size,
                button_size,
            ),
            "down_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y - button_spacing + 20,
                button_size,
                button_size,
            ),
            "left_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y + 20,
                button_size,
                button_size,
            ),
            "right_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y + button_spacing + 20,
                button_size,
                button_size,
            ),
            "back": pygame.Rect(
                CENTER_X - 150,
                CENTER_Y + button_spacing * 2 + 20,
                300,
                button_size,
            ),
            "title": Font.MINECRAFT_FONT["title"].render(
                "Настройки", True, (255, 255, 255)
            ),
            "up_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Вверх", True, (255, 255, 255)
            ),
            "down_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Вниз", True, (255, 255, 255)
            ),
            "left_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Влево", True, (255, 255, 255)
            ),
            "right_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Вправо", True, (255, 255, 255)
            ),
            "version": version_elem,
            "developer": developer_elem,
        }
        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "title": {
                "pos": (
                    CENTER_X - self.elements["title"].get_width() // 2,
                    CENTER_Y - 300,
                )
            },
            "description": {
                "pos": (
                    CENTER_X - self.elements["description"].get_width() // 2,
                    CENTER_Y - 180,
                )
            },
            "up_btn_label": {
                "pos": (
                    CENTER_X - 100,
                    CENTER_Y
                    - button_spacing * 2
                    + 20
                    + button_size // 2
                    - self.elements["up_btn_label"].get_height() // 2,
                )
            },
            "down_btn_label": {
                "pos": (
                    CENTER_X - 100,
                    CENTER_Y
                    - button_spacing
                    + 20
                    + button_size // 2
                    - self.elements["down_btn_label"].get_height() // 2,
                )
            },
            "left_btn_label": {
                "pos": (
                    CENTER_X - 100,
                    CENTER_Y
                    + 20
                    + button_size // 2
                    - self.elements["left_btn_label"].get_height() // 2,
                )
            },
            "right_btn_label": {
                "pos": (
                    CENTER_X - 100,
                    CENTER_Y
                    + button_spacing
                    + 20
                    + button_size // 2
                    - self.elements["right_btn_label"].get_height() // 2,
                )
            },
            "version": {
                "pos": (
                    SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (5, SCREEN_HEIGHT - self.elements["developer"].get_height() - 5)
            },
            "button_texts": {
                "up_btn": get_btn("up"),
                "down_btn": get_btn("down"),
                "left_btn": get_btn("left"),
                "right_btn": get_btn("right"),
                "back": "Главное меню",
            },
        }

    def render(self, surface, bg_color=(15, 7, 36)):
        self.update_elements()
        super().render(surface, bg_color)


class EducationMenu(HUD):
    pass


class GameMenu(HUD):
    pass
