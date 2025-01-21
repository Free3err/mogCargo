import pygame
import json

from ctypes import windll

from ..constants import Font, developer_elem, version_elem

user32 = windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


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
        pygame.K_F12: "F12"
    }
    
    if key_code in special_keys:
        return special_keys[key_code]
    
    return chr(key_code).upper()

class ScrollableHUD():
    def __init__(self):
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
        surface.fill(bg_color)

        current_mouse_pos = pygame.mouse.get_pos()
        mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]
        mouse_dy = current_mouse_pos[1] - self.last_mouse_pos[1]

        self.bg_offset_x = max(-100, min(0, self.bg_offset_x - mouse_dx * 0.1))
        self.bg_offset_y = max(-100, min(0, self.bg_offset_y - mouse_dy * 0.1))

        surface.blit(
            pygame.transform.scale(
                self.additions["background"],
                (SCREEN_WIDTH + 150, SCREEN_HEIGHT + 150),
            ),
            (self.bg_offset_x, self.bg_offset_y),
        )

        self.last_mouse_pos = current_mouse_pos

        for key in self.pages[self.current_page - 1]:
            value = self.elements[key]
            if isinstance(value, pygame.Rect):
                rect = pygame.Surface((value.width, value.height))
                rect.fill((50, 50, 50))
                surface.blit(rect, value)
                if "button_texts" in self.additions and key in self.additions["button_texts"]:
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
                        (SCREEN_WIDTH + 150, SCREEN_HEIGHT + 150),
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
                if "button_texts" in self.additions and key in self.additions["button_texts"]:
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
            "shot_btn": pygame.Rect(
                CENTER_X + 100,
                CENTER_Y - button_spacing * 2 + 20,
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
            "shot_btn_label": Font.MINECRAFT_FONT["text"].render(
                "Выстрел", True, (255, 255, 255)
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
            "shot_btn_label": {
                "pos": (
                    CENTER_X - 200,
                    CENTER_Y
                    - button_spacing * 2
                    + 20
                    + button_height // 2
                    - self.elements["shot_btn_label"].get_height() // 2,
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
                    SCREEN_WIDTH - self.elements["version"].get_width() - 5,
                    SCREEN_HEIGHT - self.elements["version"].get_height() - 5,
                )
            },
            "developer": {
                "pos": (5, SCREEN_HEIGHT - self.elements["developer"].get_height() - 5)
            },
            "button_texts": {
                "up_btn": get_key("up"),
                "break_btn": get_key("break"),
                "left_btn": get_key("left"),
                "right_btn": get_key("right"),
                "boost_btn": get_key("boost"),
                "shot_btn": get_key("shot"),
                "shield_btn": get_key("shield"),
                "interaction_btn": get_key("interaction"),
                "back": "Главное меню",
                "next_page": "Далее",
                "prev_page": "Назад",
            },
        }
        
        self.pages = [["title", "description", "up_btn_label", "break_btn_label", "left_btn_label", "right_btn_label", "boost_btn_label", "next_page", "up_btn", "break_btn", "left_btn", "right_btn", "boost_btn", "back", "version", "developer"], 
                      ["title", "description", "shield_btn_label", "interaction_btn_label", "prev_page", "shot_btn_label", "shield_btn", "interaction_btn", "shot_btn", "back", "version", "developer"]]

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
                "Ваша цель - доставлять различные грузы на станции.", True, (255, 255, 255)
            ),
            "target_description_part_3": Font.MINECRAFT_FONT["text"].render(
                "Для этого вам нужно будет управлять своим кораблем.", True, (255, 255, 255)
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
            "desc_special_shot": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('shot')} - выстрелить", True, (255, 255, 255)
            ),
            "desc_special_shield": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('shield')} - активировать щит", True, (255, 255, 255)
            ),
            "common_title": Font.MINECRAFT_FONT["h2"].render(
                "Общее использование", True, (255, 255, 255)
            ),
            "desc_common_interaction": Font.MINECRAFT_FONT["text"].render(
                f"{get_key('interaction')} - взаимодействие с объектами", True, (255, 255, 255)
            ),
            "version": version_elem,
            "developer": developer_elem,
        }
        self.additions = {
            "background": pygame.image.load("src/assets/img/HUD/backgrounds/stars.png"),
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
                    CENTER_X - self.elements["target_description_part_1"].get_width() // 2,
                    275,
                )
            },
            "target_description_part_2": {
                "pos": (
                    CENTER_X - self.elements["target_description_part_2"].get_width() // 2,
                    325,
                )
            },
            "target_description_part_3": {
                "pos": (
                    CENTER_X - self.elements["target_description_part_3"].get_width() // 2,
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
            "desc_special_shot": {
                "pos": (
                    CENTER_X - self.elements["desc_special_shot"].get_width() // 2,
                    275,
                )
            },
            "desc_special_shield": {
                "pos": (
                    CENTER_X - self.elements["desc_special_shield"].get_width() // 2,
                    325,
                )
            },
            "common_title": {
                "pos": (
                    CENTER_X - self.elements["common_title"].get_width() // 2,
                    375,
                )
            },
            "desc_common_interaction": {
                "pos": (
                    CENTER_X - self.elements["desc_common_interaction"].get_width() // 2,
                    425,
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
                "back": "Главное меню",
                "next_page": "Далее",
                "prev_page": "Назад",
            },
        }
        self.pages = [["title", "target_title", "target_description_part_1", "target_description_part_2", 
                             "target_description_part_3", "moving_title", "desc_moving_up", "desc_moving_break",
                             "desc_moving_left", "desc_moving_right", "desc_moving_boost", "back", "next_page", "version", "developer"], 
                      ["title", "special_title", "desc_special_shot", "desc_special_shield",
                             "common_title", "desc_common_interaction", "back", "prev_page", "version", "developer"]]
        
    def render(self, surface, bg_color=(15, 7, 36)):
        self.update_elements()
        ScrollableHUD.render(self, surface, bg_color)


class GameMenu(HUD):
    pass
