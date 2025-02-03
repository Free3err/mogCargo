import pygame
import json
from random import randint
import pymunk
import os

from ..constants import Font, developer_elem, version_elem, Device
from ..cfg import Config

from ..scripts.entities import Ship, Asteroid, Planet
from ..scripts.camera import Camera

CENTER_X = Device.SCREEN_WIDTH // 2
CENTER_Y = Device.SCREEN_HEIGHT // 2


def get_key(key):
    with open("src/cfg/keymapping_settings.json", "r") as f:
        keymapping = json.load(f)
    key_code = keymapping[key]

    special_keys = {
        pygame.K_LSHIFT: "LShift",
        pygame.K_RSHIFT: "RShift",
        pygame.K_LCTRL: "LCtrl",
        pygame.K_RCTRL: "RCtrl",
        pygame.K_LALT: "LAlt",
        pygame.K_RALT: "RAlt",
        pygame.K_RETURN: "Enter",
        pygame.K_SPACE: "Space",
        pygame.K_TAB: "Tab",
        pygame.K_ESCAPE: "Esc",
        pygame.K_CAPSLOCK: "CapsLock",
        pygame.K_BACKSPACE: "Backspace",
        pygame.K_F1: "F1",
        pygame.K_F2: "F2",
        pygame.K_F3: "F3",
        pygame.K_F4: "F4",
        pygame.K_F5: "F5",
        pygame.K_F6: "F6",
        pygame.K_F7: "F7",
        pygame.K_F8: "F8",
        pygame.K_F9: "F9",
        pygame.K_F10: "F10",
        pygame.K_F11: "F11",
        pygame.K_F12: "F12",
    }

    if key_code in special_keys:
        return special_keys[key_code]

    return chr(key_code).upper()


def get_user_data(key):
    with open("src/cfg/user_data.json", "r") as f:
        user_data = json.load(f)
    return user_data[key]


class ScrollableHUD:
    def __init__(self):
        """Инициализация прокручиваемого интерфейса"""
        super().__init__()
        self.current_page = 1
        self.max_pages = 2

        self.buttons = {
            "next_page": pygame.Rect(
                CENTER_X + 200,
                CENTER_Y * 1.7,
                150,
                60,
            ),
            "prev_page": pygame.Rect(
                CENTER_X - 200 - 150,
                CENTER_Y * 1.7,
                150,
                60,
            ),
        }

    def render(self, surface, bg_color=(15, 7, 36)):
        """Отрисовка прокручиваемого интерфейса"""
        surface.fill(bg_color)

        current_mouse_pos = pygame.mouse.get_pos()
        mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]
        mouse_dy = current_mouse_pos[1] - self.last_mouse_pos[1]

        self.bg_offset_x = max(-100, min(0, self.bg_offset_x - mouse_dx * 0.1))
        self.bg_offset_y = max(-100, min(0, self.bg_offset_y - mouse_dy * 0.1))

        surface.blit(
            pygame.transform.scale(
                self.additions["background"],
                (Device.SCREEN_WIDTH + 150, Device.SCREEN_HEIGHT + 150),
            ),
            (self.bg_offset_x, self.bg_offset_y),
        )

        self.last_mouse_pos = current_mouse_pos

        for key in self.pages[self.current_page - 1]:
            value = self.elements[key]
            if isinstance(value, pygame.Rect):
                rect = pygame.Surface((value.width, value.height))
                rect.fill(
                    self.additions["rect_color"]
                    if f"{key}_color" not in self.additions
                    else self.additions[f"{key}_color"]
                )
                surface.blit(rect, value)
                if (
                    "button_texts" in self.additions
                    and key in self.additions["button_texts"]
                ):
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


class HUD:
    def __init__(self):
        """Инициализация базового интерфейса"""
        self.elements = None
        self.cursor = pygame.image.load("src/assets/img/HUD/cursor.png")
        self.cursor = pygame.transform.scale(self.cursor, (24, 34))
        pygame.mouse.set_visible(False)

        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.last_mouse_pos = pygame.mouse.get_pos()

    def render_cursor(self, surface):
        """Отрисовка курсора на поверхности"""
        mouse_pos = pygame.mouse.get_pos()
        surface.blit(self.cursor, (mouse_pos[0], mouse_pos[1]))

    def render(self, surface, bg_color=(15, 7, 36)):
        """Отрисовка базового интерфейса"""
        surface.fill(bg_color)

        if hasattr(self, "additions") and "background" in self.additions:
            if hasattr(self, "has_moving_background") and self.has_moving_background:
                current_mouse_pos = pygame.mouse.get_pos()
                mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]
                mouse_dy = current_mouse_pos[1] - self.last_mouse_pos[1]

                self.bg_offset_x = max(-100, min(0, self.bg_offset_x - mouse_dx * 0.1))
                self.bg_offset_y = max(-100, min(0, self.bg_offset_y - mouse_dy * 0.1))

                surface.blit(
                    pygame.transform.scale(
                        self.additions["background"],
                        (Device.SCREEN_WIDTH + 150, Device.SCREEN_HEIGHT + 150),
                    ),
                    (self.bg_offset_x, self.bg_offset_y),
                )

                self.last_mouse_pos = current_mouse_pos
            else:
                surface.blit(
                    pygame.transform.scale(
                        self.additions["background"],
                        (Device.SCREEN_WIDTH + 150, Device.SCREEN_HEIGHT + 150),
                    ),
                    (0, 0),
                )

        for key, value in self.elements.items():
            if isinstance(value, pygame.Rect):
                rect = pygame.Surface((value.width, value.height))
                rect.fill(
                    self.additions["rect_color"]
                    if f"{key}_color" not in self.additions
                    else self.additions[f"{key}_color"]
                )
                surface.blit(rect, value)
                if (
                    "button_texts" in self.additions
                    and key in self.additions["button_texts"]
                ):
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

        self.render_cursor(surface)


class MainMenu(HUD):
    def __init__(self):
        """
        Инициализация HUD главного меню
        """
        super().__init__()

        self.has_moving_background = True

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
            "rect_color": (50, 50, 50),
            "title": {
                "pos": (
                    CENTER_X - self.elements["title"].get_width() // 2,
                    CENTER_Y - 300,
                )
            },
            "version": {
                "pos": (
                    Device.SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    Device.SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (
                    5,
                    Device.SCREEN_HEIGHT - self.elements["developer"].get_height() - 5,
                )
            },
            "button_texts": {
                "start_game": "Начать игру",
                "settings": "Настройки",
                "education": "Обучение",
                "exit": "Выйти",
            },
        }


class SettingsMenu(HUD, ScrollableHUD):
    def __init__(self):
        HUD.__init__(self)
        ScrollableHUD.__init__(self)
        self.has_moving_background = True
        self.update_elements()

    def update_elements(self):
        button_height = 60
        button_width = 100
        button_spacing = 80

        self.elements = {
            "description": Font.MINECRAFT_FONT["small"].render(
                "Нажмите на кнопку, чтобы изменить кнопку", True, (255, 255, 255)
            ),
            "back": pygame.Rect(
                CENTER_X - 150,
                CENTER_Y * 1.7,
                300,
                60,
            ),
            "up_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y - button_spacing * 2 + 20,
                button_width,
                button_height,
            ),
            "break_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y - button_spacing + 20,
                button_width,
                button_height,
            ),
            "left_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y + 20,
                button_width,
                button_height,
            ),
            "right_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y + button_spacing + 20,
                button_width,
                button_height,
            ),
            "boost_btn": pygame.Rect(
                CENTER_X + 50,
                CENTER_Y + button_spacing * 2 + 20,
                button_width,
                button_height,
            ),
            "shield_btn": pygame.Rect(
                CENTER_X + 100,
                CENTER_Y - button_spacing + 20,
                button_width,
                button_height,
            ),
            "interaction_btn": pygame.Rect(
                CENTER_X + 100,
                CENTER_Y + 20,
                button_width,
                button_height,
            ),
            "back": pygame.Rect(
                CENTER_X - 150,
                CENTER_Y * 1.7,
                300,
                button_height,
            ),
            "title": Font.MINECRAFT_FONT["title"].render(
                "Настройки", True, (255, 255, 255)
            ),
            "up_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Вверх", True, (255, 255, 255)
            ),
            "break_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Тормоз", True, (255, 255, 255)
            ),
            "left_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Влево", True, (255, 255, 255)
            ),
            "right_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Вправо", True, (255, 255, 255)
            ),
            "boost_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Ускорение", True, (255, 255, 255)
            ),
            "shield_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Щит", True, (255, 255, 255)
            ),
            "interaction_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Взаимодействие", True, (255, 255, 255)
            ),
            "prev_page": self.buttons["prev_page"],
            "next_page": self.buttons["next_page"],
            "version": version_elem,
            "developer": developer_elem,
        }
        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "rect_color": (50, 50, 50),
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
                    CENTER_X - 150,
                    CENTER_Y
                    - button_spacing * 2
                    + 20
                    + button_height // 2
                    - self.elements["up_btn_label"].get_height() // 2,
                )
            },
            "break_btn_label": {
                "pos": (
                    CENTER_X - 150,
                    CENTER_Y
                    - button_spacing
                    + 20
                    + button_height // 2
                    - self.elements["break_btn_label"].get_height() // 2,
                )
            },
            "left_btn_label": {
                "pos": (
                    CENTER_X - 150,
                    CENTER_Y
                    + 20
                    + button_height // 2
                    - self.elements["left_btn_label"].get_height() // 2,
                )
            },
            "right_btn_label": {
                "pos": (
                    CENTER_X - 150,
                    CENTER_Y
                    + button_spacing
                    + 20
                    + button_height // 2
                    - self.elements["right_btn_label"].get_height() // 2,
                )
            },
            "boost_btn_label": {
                "pos": (
                    CENTER_X - 150,
                    CENTER_Y
                    + button_spacing * 2
                    + 20
                    + button_height // 2
                    - self.elements["boost_btn_label"].get_height() // 2,
                )
            },
            "shield_btn_label": {
                "pos": (
                    CENTER_X - 200,
                    CENTER_Y
                    - button_spacing
                    + 20
                    + button_height // 2
                    - self.elements["shield_btn_label"].get_height() // 2,
                )
            },
            "interaction_btn_label": {
                "pos": (
                    CENTER_X - 200,
                    CENTER_Y
                    + 20
                    + button_height // 2
                    - self.elements["interaction_btn_label"].get_height() // 2,
                )
            },
            "version": {
                "pos": (
                    Device.SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    Device.SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (
                    5,
                    Device.SCREEN_HEIGHT - self.elements["developer"].get_height() - 5,
                )
            },
            "button_texts": {
                "up_btn": get_key("up"),
                "break_btn": get_key("break"),
                "left_btn": get_key("left"),
                "right_btn": get_key("right"),
                "boost_btn": get_key("boost"),
                "shield_btn": get_key("shield"),
                "interaction_btn": get_key("interaction"),
                "back": "Главное меню",
                "next_page": "Далее",
                "prev_page": "Назад",
            },
        }

        self.pages = [
            [
                "title",
                "description",
                "up_btn_label",
                "break_btn_label",
                "left_btn_label",
                "right_btn_label",
                "boost_btn_label",
                "next_page",
                "up_btn",
                "break_btn",
                "left_btn",
                "right_btn",
                "boost_btn",
                "back",
                "version",
                "developer",
            ],
            [
                "title",
                "description",
                "shield_btn_label",
                "interaction_btn_label",
                "prev_page",
                "shield_btn",
                "interaction_btn",
                "back",
                "version",
                "developer",
            ],
        ]

    def render(self, surface, bg_color=(15, 7, 36)):
        self.update_elements()
        ScrollableHUD.render(self, surface, bg_color)


class EducationMenu(HUD, ScrollableHUD):
    def __init__(self):
        HUD.__init__(self)
        ScrollableHUD.__init__(self)
        self.has_moving_background = True

    def update_elements(self):
        self.elements = {
            "title": Font.MINECRAFT_FONT["title"].render(
                "Обучение", True, (255, 255, 255)
            ),
            "version": version_elem,
            "developer": developer_elem,
            "back": pygame.Rect(
                CENTER_X - 150,
                CENTER_Y * 1.7,
                300,
                60,
            ),
            "prev_page": self.buttons["prev_page"],
            "next_page": self.buttons["next_page"],
            "target_title": Font.MINECRAFT_FONT["h2"].render(
                "Цель игры", True, (255, 255, 255)
            ),
            "target_description_part_1": Font.MINECRAFT_FONT["text"].render(
                "MogCargo /> - игра про космические перевозки.", True, (255, 255, 255)
            ),
            "target_description_part_2": Font.MINECRAFT_FONT["text"].render(
                "Ваша цель - доставлять различные грузы на станции.",
                True,
                (255, 255, 255),
            ),
            "target_description_part_3": Font.MINECRAFT_FONT["text"].render(
                "Для этого вам нужно будет управлять своим кораблем.",
                True,
                (255, 255, 255),
            ),
            "moving_title": Font.MINECRAFT_FONT["h2"].render(
                "Движение", True, (255, 255, 255)
            ),
            "desc_moving_up": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('up')} - движение вперед", True, (255, 255, 255)
            ),
            "desc_moving_break": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('break')} - торможение", True, (255, 255, 255)
            ),
            "desc_moving_left": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('left')} - повернуть влево", True, (255, 255, 255)
            ),
            "desc_moving_right": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('right')} - повернуть вправо", True, (255, 255, 255)
            ),
            "desc_moving_boost": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('boost')} - Ускорение", True, (255, 255, 255)
            ),
            "special_title": Font.MINECRAFT_FONT["h2"].render(
                "Специальные действия", True, (255, 255, 255)
            ),
            "desc_special_shield": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('shield')} - активировать щит", True, (255, 255, 255)
            ),
            "common_title": Font.MINECRAFT_FONT["h2"].render(
                "Общее использование", True, (255, 255, 255)
            ),
            "desc_common_interaction": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('interaction')} - взаимодействие с объектами",
                True,
                (255, 255, 255),
            ),
            "version": version_elem,
            "developer": developer_elem,
        }
        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "rect_color": (50, 50, 50),
            "title": {
                "pos": (
                    CENTER_X - self.elements["title"].get_width() // 2,
                    100,
                )
            },
            "target_title": {
                "pos": (
                    CENTER_X - self.elements["target_title"].get_width() // 2,
                    225,
                )
            },
            "target_description_part_1": {
                "pos": (
                    CENTER_X
                    - self.elements["target_description_part_1"].get_width() // 2,
                    275,
                )
            },
            "target_description_part_2": {
                "pos": (
                    CENTER_X
                    - self.elements["target_description_part_2"].get_width() // 2,
                    325,
                )
            },
            "target_description_part_3": {
                "pos": (
                    CENTER_X
                    - self.elements["target_description_part_3"].get_width() // 2,
                    375,
                )
            },
            "moving_title": {
                "pos": (
                    CENTER_X - self.elements["moving_title"].get_width() // 2,
                    425,
                )
            },
            "desc_moving_up": {
                "pos": (
                    CENTER_X - self.elements["desc_moving_up"].get_width() // 2,
                    475,
                )
            },
            "desc_moving_break": {
                "pos": (
                    CENTER_X - self.elements["desc_moving_break"].get_width() // 2,
                    525,
                )
            },
            "desc_moving_left": {
                "pos": (
                    CENTER_X - self.elements["desc_moving_left"].get_width() // 2,
                    575,
                )
            },
            "desc_moving_right": {
                "pos": (
                    CENTER_X - self.elements["desc_moving_right"].get_width() // 2,
                    625,
                )
            },
            "desc_moving_boost": {
                "pos": (
                    CENTER_X - self.elements["desc_moving_boost"].get_width() // 2,
                    675,
                )
            },
            "special_title": {
                "pos": (
                    CENTER_X - self.elements["special_title"].get_width() // 2,
                    225,
                )
            },
            "desc_special_shield": {
                "pos": (
                    CENTER_X - self.elements["desc_special_shield"].get_width() // 2,
                    275,
                )
            },
            "common_title": {
                "pos": (
                    CENTER_X - self.elements["common_title"].get_width() // 2,
                    325,
                )
            },
            "desc_common_interaction": {
                "pos": (
                    CENTER_X
                    - self.elements["desc_common_interaction"].get_width() // 2,
                    375,
                )
            },
            "version": {
                "pos": (
                    Device.SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    Device.SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (
                    5,
                    Device.SCREEN_HEIGHT - self.elements["developer"].get_height() - 5,
                )
            },
            "button_texts": {
                "back": "Главное меню",
                "next_page": "Далее",
                "prev_page": "Назад",
            },
        }
        self.pages = [
            [
                "title",
                "target_title",
                "target_description_part_1",
                "target_description_part_2",
                "target_description_part_3",
                "moving_title",
                "desc_moving_up",
                "desc_moving_break",
                "desc_moving_left",
                "desc_moving_right",
                "desc_moving_boost",
                "back",
                "next_page",
                "version",
                "developer",
            ],
            [
                "title",
                "special_title",
                "desc_special_shield",
                "common_title",
                "desc_common_interaction",
                "back",
                "prev_page",
                "version",
                "developer",
            ],
        ]

    def render(self, surface, bg_color=(15, 7, 36)):
        self.update_elements()
        ScrollableHUD.render(self, surface, bg_color)


class GameMenu(HUD):
    def __init__(self):
        super().__init__()
        self.has_moving_background = True
        self.update_elements()

        self.stats_cards = {
            "Прочность корабля": {
                "value": Config.user_data["hp"],
                "description": "+1 к прочности",
                "max_value": Config.cfg["prices"]["hp"]["max_level"],
                "price": Config.cfg["prices"]["hp"]["base_price"],
            },
            "Скорость корабля": {
                "value": Config.user_data["max_speed"],
                "description": "+10% к скорости",
                "max_value": Config.cfg["prices"]["speed"]["max_level"],
                "price": Config.cfg["prices"]["speed"]["base_price"],
            },
            "Ускорение": {
                "value": Config.user_data["boost_time"],
                "description": "-10% кулдаун",
                "max_value": Config.cfg["prices"]["boost"]["max_level"],
                "price": Config.cfg["prices"]["boost"]["base_price"],
            },
            "Щит": {
                "value": Config.user_data["shield_time"],
                "description": "+10% длительность",
                "max_value": Config.cfg["prices"]["shield"]["max_level"],
                "price": Config.cfg["prices"]["shield"]["base_price"],
            },
        }

    def update_elements(self):
        user_data = Config.user_data
        current_level = user_data.get("level", "1")
        credits = user_data.get("credits", 0)
        exp = user_data.get("exp", 0)

        self.elements = {
            "title": Font.MINECRAFT_FONT["title"].render("Меню", True, (255, 255, 255)),
            "version": version_elem,
            "developer": developer_elem,
            "back": pygame.Rect(
                CENTER_X - 200 - 300,
                CENTER_Y * 1.7,
                300,
                60,
            ),
            "play": pygame.Rect(
                CENTER_X + 200,
                CENTER_Y * 1.7,
                300,
                60,
            ),
            "border_level_bar": pygame.Rect(CENTER_X - 202, CENTER_Y + 248, 404, 24),
            "level_bar": pygame.Rect(
                CENTER_X - 200,
                CENTER_Y + 250,
                400 * (user_data.get("level_percent", 0)),
                20,
            ),
            "credits_icon": pygame.transform.scale(
                pygame.image.load("src/assets/img/HUD/coin.png"), (40, 40)
            ),
            "level_icon": pygame.transform.scale(
                pygame.image.load("src/assets/img/HUD/book.png"), (40, 40)
            ),
            "credits_text": Font.MINECRAFT_FONT["text"].render(
                f"Кредиты: {credits}", True, (255, 255, 255)
            ),
            "level_text": Font.MINECRAFT_FONT["text"].render(
                f"Уровень: {current_level}", True, (255, 255, 255)
            ),
            "exp_text": Font.MINECRAFT_FONT["text"].render(
                f"{exp} / {Config.cfg['levels'][str(int(current_level) + 1)]['exp']}",
                True,
                (255, 255, 255),
            ),
            "hp_upgrade": pygame.Rect(
                CENTER_X - 500,
                CENTER_Y - 100,
                200,
                250,
            ),
            "speed_upgrade": pygame.Rect(
                CENTER_X - 250,
                CENTER_Y - 100,
                200,
                250,
            ),
            "boost_upgrade": pygame.Rect(
                CENTER_X,
                CENTER_Y - 100,
                200,
                250,
            ),
            "shield_upgrade": pygame.Rect(
                CENTER_X + 250,
                CENTER_Y - 100,
                200,
                250,
            ),
            "hp_title": Font.MINECRAFT_FONT["text"].render(
                "Прочность", True, (255, 255, 255)
            ),
            "speed_title": Font.MINECRAFT_FONT["text"].render(
                "Скорость", True, (255, 255, 255)
            ),
            "boost_title": Font.MINECRAFT_FONT["text"].render(
                "Ускорение", True, (255, 255, 255)
            ),
            "shield_title": Font.MINECRAFT_FONT["text"].render(
                "Щит", True, (255, 255, 255)
            ),
            "hp_desc": Font.MINECRAFT_FONT["small"].render(
                "+1 к проч.", True, (255, 255, 255)
            ),
            "speed_desc": Font.MINECRAFT_FONT["small"].render(
                "+10% к скор.", True, (255, 255, 255)
            ),
            "boost_desc": Font.MINECRAFT_FONT["small"].render(
                "+10% длит.", True, (255, 255, 255)
            ),
            "shield_desc": Font.MINECRAFT_FONT["small"].render(
                "+10% длит.", True, (255, 255, 255)
            ),
            "hp_value": Font.MINECRAFT_FONT["text"].render(
                f"{round(user_data['hp'])} ед.", True, (255, 255, 255)
            ),
            "speed_value": Font.MINECRAFT_FONT["text"].render(
                f"{round(user_data['max_speed'])} ед. / сек", True, (255, 255, 255)
            ),
            "boost_value": Font.MINECRAFT_FONT["text"].render(
                f"{round(user_data['boost_time'])} сек.", True, (255, 255, 255)
            ),
            "shield_value": Font.MINECRAFT_FONT["text"].render(
                f"{round(user_data['shield_time'])} сек.", True, (255, 255, 255)
            ),
        }
        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
            "rect_color": (50, 50, 50),
            "title": {
                "pos": (
                    CENTER_X - self.elements["title"].get_width() // 2,
                    CENTER_Y - 300,
                )
            },
            "version": {
                "pos": (
                    Device.SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    Device.SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (
                    5,
                    Device.SCREEN_HEIGHT - self.elements["developer"].get_height() - 5,
                )
            },
            "button_texts": {
                "back": "Главное меню",
                "play": "Начать игру",
            },
            "credits_icon": {
                "pos": (CENTER_X - 450, CENTER_Y + 170),
            },
            "credits_text": {
                "pos": (
                    CENTER_X - 450 + self.elements["credits_icon"].get_width() + 10,
                    CENTER_Y + 180,
                ),
            },
            "level_icon": {
                "pos": (CENTER_X - 450, CENTER_Y + 240),
            },
            "level_text": {
                "pos": (
                    CENTER_X - 450 + self.elements["level_icon"].get_width() + 10,
                    CENTER_Y + 250,
                ),
            },
            "border_level_bar_color": (255, 255, 255),
            "level_bar_color": (247, 132, 0),
            "exp_text": {
                "pos": (CENTER_X - 152 + 400, CENTER_Y + 250),
            },
            "hp_title": {
                "pos": (
                    CENTER_X - 500 + (200 - self.elements["hp_title"].get_width()) // 2,
                    CENTER_Y - 80,
                )
            },
            "speed_title": {
                "pos": (
                    CENTER_X
                    - 250
                    + (200 - self.elements["speed_title"].get_width()) // 2,
                    CENTER_Y - 80,
                )
            },
            "boost_title": {
                "pos": (
                    CENTER_X + (200 - self.elements["boost_title"].get_width()) // 2,
                    CENTER_Y - 80,
                )
            },
            "shield_title": {
                "pos": (
                    CENTER_X
                    + 250
                    + (200 - self.elements["shield_title"].get_width()) // 2,
                    CENTER_Y - 80,
                )
            },
            "hp_desc": {
                "pos": (
                    CENTER_X - 500 + (200 - self.elements["hp_desc"].get_width()) // 2,
                    CENTER_Y - 40,
                )
            },
            "speed_desc": {
                "pos": (
                    CENTER_X
                    - 250
                    + (200 - self.elements["speed_desc"].get_width()) // 2,
                    CENTER_Y - 40,
                )
            },
            "boost_desc": {
                "pos": (
                    CENTER_X + (200 - self.elements["boost_desc"].get_width()) // 2,
                    CENTER_Y - 40,
                )
            },
            "shield_desc": {
                "pos": (
                    CENTER_X
                    + 250
                    + (200 - self.elements["shield_desc"].get_width()) // 2,
                    CENTER_Y - 40,
                )
            },
            "hp_value": {
                "pos": (
                    CENTER_X - 500 + (200 - self.elements["hp_value"].get_width()) // 2,
                    CENTER_Y + 100,
                )
            },
            "speed_value": {
                "pos": (
                    CENTER_X
                    - 250
                    + (200 - self.elements["speed_value"].get_width()) // 2,
                    CENTER_Y + 100,
                )
            },
            "boost_value": {
                "pos": (
                    CENTER_X + (200 - self.elements["boost_value"].get_width()) // 2,
                    CENTER_Y + 100,
                )
            },
            "shield_value": {
                "pos": (
                    CENTER_X
                    + 250
                    + (200 - self.elements["shield_value"].get_width()) // 2,
                    CENTER_Y + 100,
                )
            },
        }

    def try_purchase_upgrade(self, upgrade_type):
        user_data = Config.user_data
        prices = Config.cfg["prices"]

        match upgrade_type:
            case "hp":
                current_value = user_data["hp"]
                current_level = Config.cfg["prices"]["hp"]["current_level"]
                price = prices["hp"]["base_price"]
            case "speed":
                current_value = user_data["max_speed"]
                current_level = Config.cfg["prices"]["speed"]["current_level"]
                price = prices["speed"]["base_price"]

            case "boost":
                current_value = user_data["boost_time"]
                current_level = Config.cfg["prices"]["boost"]["current_level"]
                price = prices["boost"]["base_price"]
            case "shield":
                current_value = user_data["shield_time"]
                current_level = Config.cfg["prices"]["shield"]["current_level"]
                price = prices["shield"]["base_price"]

        if current_level >= prices[upgrade_type]["max_level"]:
            return

        if user_data["credits"] >= price:
            user_data["credits"] -= price

            match upgrade_type:
                case "hp":
                    user_data["hp"] += 1
                case "speed":
                    user_data["max_speed"] += 1
                case "boost":
                    user_data["boost_time"] += 1
                case "shield":
                    user_data["shield_time"] += 1

            Config.cfg["prices"][upgrade_type]["current_level"] += 1
            Config.cfg["prices"][upgrade_type]["base_price"] = round(
                Config.cfg["prices"][upgrade_type]["base_price"] * 1.2
            )

            with open(os.path.join("src", "cfg", "prices.json"), "w") as f:
                json.dump(Config.cfg["prices"], f, indent=4)

            with open(os.path.join("src", "cfg", "user_data.json"), "w") as f:
                json.dump(Config.user_data, f, indent=4)

            Config.__init__(Config())
            self.update_elements()

    def draw_stats_cards(self, screen):
        x_start = Device.SCREEN_WIDTH // 2 - 400
        y = 200
        card_width = 250
        card_spacing = 20

        for title, data in self.stats_cards.items():
            self.draw_card(
                screen,
                x_start,
                y,
                card_width,
                title,
                str(data["value"]),
                data["description"],
                data["max_value"],
                data["price"],
            )
            x_start += card_width + card_spacing

    def draw_card(
        self, screen, x, y, width, title, value, description, max_value, price
    ):
        height = 100
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), 0)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)

        # Отрисовка заголовка
        title_font = Font.MINECRAFT_FONT["text"].render(title, True, (255, 255, 255))
        screen.blit(title_font, (x + 5, y + 5))

        # Отрисовка значения
        value_font = Font.MINECRAFT_FONT["text"].render(
            f"{value} / {max_value}", True, (255, 255, 255)
        )
        screen.blit(value_font, (x + width // 2 - value_font.get_width() // 2, y + 40))

        # Отрисовка описания
        desc_font = Font.MINECRAFT_FONT["small"].render(
            description, True, (200, 200, 200)
        )
        screen.blit(desc_font, (x + 5, y + height - 20))

        # Отрисовка цены
        price_font = Font.MINECRAFT_FONT["small"].render(
            f"Цена: {price}", True, (255, 215, 0)
        )
        screen.blit(
            price_font, (x + width - price_font.get_width() - 5, y + height - 20)
        )

    def render(self, surface, bg_color=(15, 7, 36)):
        self.update_elements()
        surface.fill(bg_color)

        if hasattr(self, "additions") and "background" in self.additions:
            if hasattr(self, "has_moving_background") and self.has_moving_background:
                current_mouse_pos = pygame.mouse.get_pos()
                mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]
                mouse_dy = current_mouse_pos[1] - self.last_mouse_pos[1]

                self.bg_offset_x = max(-100, min(0, self.bg_offset_x - mouse_dx * 0.1))
                self.bg_offset_y = max(-100, min(0, self.bg_offset_y - mouse_dy * 0.1))

                surface.blit(
                    pygame.transform.scale(
                        self.additions["background"],
                        (Device.SCREEN_WIDTH + 150, Device.SCREEN_HEIGHT + 150),
                    ),
                    (self.bg_offset_x, self.bg_offset_y),
                )

                self.last_mouse_pos = current_mouse_pos

        for key, value in self.elements.items():
            if isinstance(value, pygame.Rect):
                rect = pygame.Surface((value.width, value.height))
                rect.fill(
                    self.additions["rect_color"]
                    if f"{key}_color" not in self.additions
                    else self.additions[f"{key}_color"]
                )
                surface.blit(rect, value)
                if (
                    "button_texts" in self.additions
                    and key in self.additions["button_texts"]
                ):
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

        # Отрисовка карточек прокачки
        for upgrade in ["hp", "speed", "boost", "shield"]:
            pygame.draw.rect(surface, (50, 50, 50), self.elements[f"{upgrade}_upgrade"])
            pygame.draw.rect(
                surface, (255, 255, 255), self.elements[f"{upgrade}_upgrade"], 2
            )

            surface.blit(
                self.elements[f"{upgrade}_title"],
                self.additions[f"{upgrade}_title"]["pos"],
            )
            surface.blit(
                self.elements[f"{upgrade}_desc"],
                self.additions[f"{upgrade}_desc"]["pos"],
            )
            surface.blit(
                self.elements[f"{upgrade}_value"],
                self.additions[f"{upgrade}_value"]["pos"],
            )

        self.render_cursor(surface)


class GameHUD(HUD):
    def __init__(self):
        super().__init__()
        self.loading_hud = LoadingHUD()
        self.loading = True
        self.pause = False
        self.is_gaven = False
        self.elements = {}
        self.start_time = pygame.time.get_ticks()

        self.space = pymunk.Space()
        self.space.damping = 0.8

        self.camera = Camera(Device.SCREEN_WIDTH, Device.SCREEN_HEIGHT)
        self.sprites = pygame.sprite.Group()

        for i in range(2):
            planet = Planet(
                (
                    randint(0, Device.SCREEN_WIDTH * 3),
                    randint(0, Device.SCREEN_HEIGHT * 3),
                ),
                self.space,
                "start" if i % 2 == 0 else "end",
            )
            self.sprites.add(planet)

        self.ship = Ship(
            (
                randint(200, Device.SCREEN_WIDTH * 3 - 200),
                randint(200, Device.SCREEN_HEIGHT * 3 - 200),
            ),
            self.sprites.sprites()[0],
            self.sprites.sprites()[1],
            self.space,
        )
        self.sprites.add(self.ship)

        attempts = 0
        asteroids_count = randint(100, 150)
        spawned_asteroids = 0

        while spawned_asteroids < asteroids_count and attempts < 1000:
            pos = (
                randint(0, Device.SCREEN_WIDTH * 3),
                randint(0, Device.SCREEN_HEIGHT * 3),
            )

            distance = (
                (pos[0] - self.ship.rect.centerx) ** 2
                + (pos[1] - self.ship.rect.centery) ** 2
            ) ** 0.5
            if distance >= 250:
                asteroid = Asteroid(pos, self.space)
                self.sprites.add(asteroid)
                spawned_asteroids += 1

            attempts += 1

    def render(self, surface, bg_color=(0, 0, 0)):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < 2000:
            surface.fill(bg_color)
            self.loading_hud.render(surface)
        else:
            self.loading = False
            if not self.pause:
                if not self.ship.delivered:
                    if self.ship.hp <= 0:
                        for sprite in self.sprites:
                            sprite.kill()
                        self.render_game_over(surface)
                    else:
                        surface.fill(bg_color)
                        self.space.step(1 / 60.0)

                        self.sprites.update()
                        self.camera.update(self.ship)

                        for sprite in self.sprites:
                            surface.blit(sprite.image, self.camera.apply(sprite))

                        self.render_minimap(surface)
                        minimap_width = Device.SCREEN_WIDTH // 6

                        # HP Bar
                        pygame.draw.rect(
                            surface, (255, 255, 255), (minimap_width + 50, 25, 304, 34)
                        )
                        pygame.draw.rect(
                            surface,
                            (255, 0, 0),
                            (
                                minimap_width + 52,
                                27,
                                300 * max(0, self.ship.hp / Config.user_data["hp"]),
                                30,
                            ),
                        )
                        surface.blit(
                            Font.MINECRAFT_FONT["text"].render(
                                f"HP: {self.ship.hp}", True, (255, 255, 255)
                            ),
                            (minimap_width + 370, 30),
                        )

                        # Boost Bar
                        pygame.draw.rect(
                            surface, (255, 255, 255), (minimap_width + 50, 65, 304, 34)
                        )
                        pygame.draw.rect(
                            surface,
                            (0, 191, 255),
                            (
                                minimap_width + 52,
                                67,
                                300 * self.ship.boost_cooldown_progress,
                                30,
                            ),
                        )
                        surface.blit(
                            Font.MINECRAFT_FONT["text"].render(
                                f"Boost: {int(self.ship.boost_cooldown_progress * 100)}%",
                                True,
                                (255, 255, 255),
                            ),
                            (minimap_width + 370, 70),
                        )

                        # Статус груза
                        surface.blit(
                            Font.MINECRAFT_FONT["text"].render(
                                "Груз взят" if self.ship.has_cargo else "Груз не взят",
                                True,
                                (255, 255, 255),
                            ),
                            (minimap_width + 50, 105),
                        )

                else:
                    if not self.is_gaven:
                        self.game_data = {
                            "exp": randint(40, 80),
                            "credits": round(
                                randint(100, 200)
                                * self.ship.hp
                                / Config.user_data["hp"]
                            ),
                        }
                        Config.user_data["exp"] += self.game_data["exp"]
                        Config.user_data["credits"] += self.game_data["credits"]
                        self.is_gaven = True
                        Config.__init__(Config())

                    self.render_game_won(surface, self.game_data)

            else:
                self.render_pause_menu(surface)

    def render_game_over(self, surface):
        overlay = pygame.Surface((Device.SCREEN_WIDTH, Device.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))

        game_over_text = Font.MINECRAFT_FONT["h2"].render(
            "Игра окончена", True, (255, 0, 0)
        )
        text_rect = game_over_text.get_rect(
            center=(Device.SCREEN_WIDTH // 2, Device.SCREEN_HEIGHT // 4)
        )
        surface.blit(game_over_text, text_rect)

        button_width = 300
        button_height = 50
        button_spacing = 20
        button_y = Device.SCREEN_HEIGHT // 2 - button_height

        buttons = ["Заново", "Главное меню"]
        self.elements = {}

        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(
                Device.SCREEN_WIDTH // 2 - button_width // 2,
                button_y + (button_height + button_spacing) * i,
                button_width,
                button_height,
            )
            pygame.draw.rect(surface, (50, 50, 50), button_rect)

            button_text = Font.MINECRAFT_FONT["text"].render(
                text, True, (255, 255, 255)
            )
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)

            self.elements[text.lower()] = button_rect

        self.render_cursor(surface)

    def render_game_won(self, surface, game_data):
        overlay = pygame.Surface((Device.SCREEN_WIDTH, Device.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))

        won_text = Font.MINECRAFT_FONT["h2"].render(
            "Уровень пройден!", True, (56, 242, 124)
        )
        text_rect = won_text.get_rect(
            center=(Device.SCREEN_WIDTH // 2, Device.SCREEN_HEIGHT // 4)
        )
        surface.blit(won_text, text_rect)

        exp_text = Font.MINECRAFT_FONT["text"].render(
            f"Получено опыта: {game_data['exp']}", True, (255, 255, 255)
        )
        exp_rect = exp_text.get_rect(
            center=(Device.SCREEN_WIDTH // 2, Device.SCREEN_HEIGHT // 3)
        )
        surface.blit(exp_text, exp_rect)

        credits_text = Font.MINECRAFT_FONT["text"].render(
            f"Получено кредитов: {game_data['credits']}", True, (255, 255, 255)
        )
        credits_rect = credits_text.get_rect(
            center=(Device.SCREEN_WIDTH // 2, Device.SCREEN_HEIGHT // 3 + 30)
        )
        surface.blit(credits_text, credits_rect)

        button_width = 300
        button_height = 50
        button_spacing = 20
        button_y = Device.SCREEN_HEIGHT // 2 - button_height

        buttons = ["Заново", "Главное меню"]
        self.elements = {}

        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(
                Device.SCREEN_WIDTH // 2 - button_width // 2,
                button_y + (button_height + button_spacing) * i,
                button_width,
                button_height,
            )
            pygame.draw.rect(surface, (50, 50, 50), button_rect)

            button_text = Font.MINECRAFT_FONT["text"].render(
                text, True, (255, 255, 255)
            )
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)

            self.elements[text.lower()] = button_rect

        self.render_cursor(surface)

    def render_pause_menu(self, surface):
        overlay = pygame.Surface((Device.SCREEN_WIDTH, Device.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))

        pause_text = Font.MINECRAFT_FONT["h2"].render(
            "Игра приостановлена", True, (255, 255, 255)
        )
        text_rect = pause_text.get_rect(
            center=(Device.SCREEN_WIDTH // 2, Device.SCREEN_HEIGHT // 4)
        )
        surface.blit(pause_text, text_rect)

        button_width = 200
        button_height = 50
        button_spacing = 20
        button_y = Device.SCREEN_HEIGHT // 2 - button_height

        buttons = ["Продолжить", "Выйти"]

        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(
                Device.SCREEN_WIDTH // 2 - button_width // 2,
                button_y + (button_height + button_spacing) * i,
                button_width,
                button_height,
            )
            pygame.draw.rect(surface, (50, 50, 50), button_rect)

            button_text = Font.MINECRAFT_FONT["text"].render(
                text, True, (255, 255, 255)
            )
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)

            self.elements[text.lower()] = button_rect

        self.render_cursor(surface)

    def render_minimap(self, surface):
        minimap_width = Device.SCREEN_WIDTH // 6
        minimap_height = Device.SCREEN_HEIGHT // 6
        minimap_surface = pygame.Surface((minimap_width, minimap_height))
        minimap_surface.fill((0, 0, 0))
        border = pygame.Rect(0, 0, minimap_width, minimap_height)

        scale_x = minimap_width / (Device.SCREEN_WIDTH * 3)
        scale_y = minimap_height / (Device.SCREEN_HEIGHT * 3)

        # Отрисовка спрайтов
        for sprite in self.sprites:
            pos_x = int(sprite.body.position.x * scale_x)
            pos_y = int(sprite.body.position.y * scale_y)
            if isinstance(sprite, Asteroid):
                if 0 <= pos_x <= minimap_width and 0 <= pos_y <= minimap_height:
                    pygame.draw.circle(
                        minimap_surface, (128, 128, 128), (pos_x, pos_y), 2
                    )
            elif isinstance(sprite, Planet):
                if 0 <= pos_x <= minimap_width and 0 <= pos_y <= minimap_height:
                    match sprite.type:
                        case "start":
                            pygame.draw.circle(
                                minimap_surface, (242, 68, 56), (pos_x, pos_y), 3
                            )
                        case "end":
                            pygame.draw.circle(
                                minimap_surface, (56, 242, 124), (pos_x, pos_y), 3
                            )

        # Отрисовка корабля
        ship_x = int(self.ship.body.position.x * scale_x)
        ship_y = int(self.ship.body.position.y * scale_y)

        if 0 <= ship_x <= minimap_width and 0 <= ship_y <= minimap_height:
            pygame.draw.circle(minimap_surface, (255, 255, 0), (ship_x, ship_y), 3)

        # Отрисовка границы и вывод на экран
        pygame.draw.rect(minimap_surface, (255, 255, 255), border, 2)
        surface.blit(minimap_surface, (25, 25))

    def handle_collision(self, arbiter, space, data):
        if not self.ship.shield_active:
            ship = arbiter.shapes[0].body.sprite
            asteroid = arbiter.shapes[1].body.sprite

            if pygame.sprite.collide_mask(ship, asteroid):
                return True
        return False


class LoadingHUD(HUD):
    def __init__(self):
        super().__init__()
        self.texts = [
            Font.MINECRAFT_FONT["h2"].render("Загрузка.", True, (255, 255, 255)),
            Font.MINECRAFT_FONT["h2"].render("Загрузка..", True, (255, 255, 255)),
            Font.MINECRAFT_FONT["h2"].render("Загрузка...", True, (255, 255, 255)),
        ]
        self.current_text = 0
        self.update_elements()

    def update_elements(self):
        self.elements = {"loading_text": self.texts[self.current_text]}

        self.additions = {
            "loading_text": {
                "pos": (
                    CENTER_X - self.elements["loading_text"].get_width() // 2,
                    CENTER_Y - self.elements["loading_text"].get_height() // 2,
                ),
            },
        }

    def render(self, surface, bg_color=(0, 0, 0)):
        surface.fill(bg_color)

        loading_text = self.elements["loading_text"]
        loading_pos = self.additions["loading_text"]["pos"]
        surface.blit(loading_text, loading_pos)

        self.current_text += 1
        self.current_text %= 3
        pygame.time.delay(300)
        self.update_elements()
