import pygame
import random
import json
import os

from .scripts.HUD import MainMenu, SettingsMenu, EducationMenu, GameMenu, GameHUD
from .scripts import terminate
from .cfg import Config
from .constants import Font, Device, game_music_themes

FPS = Device.SCREEN_REFRESH_RATE


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.cfg = Config().cfg
        self.screen = pygame.display.set_mode()
        pygame.display.set_icon(pygame.image.load("src/assets/img/icon.png"))
        pygame.display.set_caption("MogCargo />")
        self.clock = pygame.time.Clock()


        self.huds = {
            "main": MainMenu(),
            "settings": SettingsMenu(),
            "education": EducationMenu(),
            "game_menu": GameMenu(),
            "game_hud": GameHUD(),
        }
        self.hud = self.huds["main"]
        self.waiting_for_key = False
        self.key_to_set = None
        self.camera = None
        self.now_playing = None

        self.music = pygame.mixer.Sound("src/assets/audio/menu_music.mp3")
        self.music.play(-1)

    def load_config(self):
        cfg = {}
        with open(os.path.join("src", "cfg", "keymapping_settings.json"), "r") as f:
            cfg["keymapping"] = json.load(f)
        return cfg

    def set_key(self, key):
        self.waiting_for_key = True
        self.key_to_set = key

    def handle_key_setting(self, event):
        if event.type == pygame.KEYDOWN:
            self.cfg["keymapping"][self.key_to_set] = event.key
            with open(os.path.join("src", "cfg", "keymapping_settings.json"), "w") as f:
                json.dump(self.cfg["keymapping"], f, indent=4)
            self.waiting_for_key = False
            self.key_to_set = None
            Config.__init__(Config())

    def play_sfx(self, sfx_name = None):
        if hasattr(self, "music"):
            self.music.stop()
        match self.hud:
            case MainMenu():
                self.music = pygame.mixer.Sound("src/assets/audio/menu_music.mp3")
                self.music.play(-1)
            case GameHUD():
                self.music = pygame.mixer.Sound(random.choice(game_music_themes))
                self.music.play(-1)

    def start_screen(self):
        start_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height())
        )
        font = Font.MINECRAFT_FONT["h2"]
        developer_text = font.render("Developed by free3err", True, (255, 255, 255))
        developer_text_rect = developer_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        team_text = font.render("MogCommunity Project", True, (255, 255, 255))
        team_text_rect = team_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )

        for alpha in range(0, 255, 5):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            start_surface.fill((0, 0, 0))
            developer_text.set_alpha(alpha)
            start_surface.blit(developer_text, developer_text_rect)
            self.screen.blit(start_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(20)

        pygame.time.delay(1000)
        for alpha in range(255, 0, -5):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            start_surface.fill((0, 0, 0))
            developer_text.set_alpha(alpha)
            start_surface.blit(developer_text, developer_text_rect)
            self.screen.blit(start_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)

        for alpha in range(0, 255, 5):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            start_surface.fill((0, 0, 0))
            team_text.set_alpha(alpha)
            start_surface.blit(team_text, team_text_rect)
            self.screen.blit(start_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

        pygame.time.delay(1000)
        for alpha in range(255, 0, -5):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            start_surface.fill((0, 0, 0))
            team_text.set_alpha(alpha)
            start_surface.blit(team_text, team_text_rect)
            self.screen.blit(start_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)

        pygame.time.delay(500)

    def render(self, hud=None):
        if hud is None:
            hud = self.hud
        self.screen.fill((0, 0, 0))

        hud.render(self.screen)

    def run(self):
        self.start_screen()
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if self.waiting_for_key:
                    self.handle_key_setting(event)
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if isinstance(self.hud, MainMenu):
                        if self.hud.elements["settings"].collidepoint(mouse_pos):
                            self.hud = self.huds["settings"]
                        elif self.hud.elements["education"].collidepoint(mouse_pos):
                            self.hud = self.huds["education"]
                        elif self.hud.elements["start_game"].collidepoint(mouse_pos):
                            self.hud = self.huds["game_menu"]
                        elif self.hud.elements["exit"].collidepoint(mouse_pos):
                            terminate()

                    elif isinstance(self.hud, SettingsMenu):
                        if self.hud.elements["up_btn"].collidepoint(mouse_pos):
                            self.set_key("up")
                        elif self.hud.elements["break_btn"].collidepoint(mouse_pos):
                            self.set_key("break")
                        elif self.hud.elements["left_btn"].collidepoint(mouse_pos):
                            self.set_key("left")
                        elif self.hud.elements["right_btn"].collidepoint(mouse_pos):
                            self.set_key("right")
                        elif self.hud.elements["boost_btn"].collidepoint(mouse_pos):
                            self.set_key("boost")
                        elif self.hud.elements["shield_btn"].collidepoint(mouse_pos):
                            self.set_key("shield")
                        elif self.hud.elements["interaction_btn"].collidepoint(
                            mouse_pos
                        ):
                            self.set_key("interaction")
                        elif self.hud.elements["back"].collidepoint(mouse_pos):
                            self.hud = self.huds["main"]
                        elif self.hud.elements["next_page"].collidepoint(mouse_pos):
                            self.hud.current_page += 1
                        elif self.hud.elements["prev_page"].collidepoint(mouse_pos):
                            self.hud.current_page -= 1

                    elif isinstance(self.hud, EducationMenu):
                        if self.hud.elements["back"].collidepoint(mouse_pos):
                            self.hud = self.huds["main"]
                        elif self.hud.elements["next_page"].collidepoint(mouse_pos):
                            self.hud.current_page += 1
                        elif self.hud.elements["prev_page"].collidepoint(mouse_pos):
                            self.hud.current_page -= 1

                    elif isinstance(self.hud, GameMenu):
                        if self.hud.elements["back"].collidepoint(mouse_pos):
                            self.hud = self.huds["main"]
                        elif self.hud.elements["play"].collidepoint(mouse_pos):
                            self.huds["game_hud"] = GameHUD()
                            self.hud = self.huds["game_hud"]
                            self.hud.start_time = pygame.time.get_ticks()
                            self.play_sfx()
                        elif self.hud.elements["hp_upgrade"].collidepoint(mouse_pos):
                            self.hud.try_purchase_upgrade("hp")
                        elif self.hud.elements["speed_upgrade"].collidepoint(mouse_pos):
                            self.hud.try_purchase_upgrade("speed")
                        elif self.hud.elements["boost_upgrade"].collidepoint(mouse_pos):
                            self.hud.try_purchase_upgrade("boost")
                        elif self.hud.elements["shield_upgrade"].collidepoint(mouse_pos):
                            self.hud.try_purchase_upgrade("shield")

                    elif isinstance(self.hud, GameHUD):
                        if self.hud.pause:
                            if self.hud.elements["продолжить"].collidepoint(mouse_pos):
                                self.hud.pause = False
                            elif self.hud.elements["выйти"].collidepoint(mouse_pos):
                                self.hud = self.huds["main"]
                                self.play_sfx()
                        elif self.hud.ship.hp <= 0 or self.hud.ship.delivered:
                            if self.hud.elements["заново"].collidepoint(mouse_pos):
                                self.huds["game_hud"] = GameHUD()
                                self.hud = self.huds["game_hud"]
                                self.hud.start_time = pygame.time.get_ticks()
                                self.play_sfx()
                            elif self.hud.elements["главное меню"].collidepoint(mouse_pos):
                                self.hud = self.huds["main"]
                                self.play_sfx()

                if (
                    isinstance(self.hud, GameHUD)
                ):
                    if (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                        self.hud.pause = not self.hud.pause

            self.render()
            pygame.display.flip()

        terminate()
