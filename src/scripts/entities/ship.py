import pygame
import math
import pymunk
import time

from ...constants import Device, Shield
from ...cfg.config import Config


class Ship(pygame.sprite.Sprite):
    imgs = [
        pygame.image.load("src/assets/img/entities/ship/based/1.png"),
        pygame.image.load("src/assets/img/entities/ship/based/2.png"),
        pygame.image.load("src/assets/img/entities/ship/based/3.png"),
        pygame.image.load("src/assets/img/entities/ship/based/4.png")
    ]

    def __init__(self, pos, space, *groups):
        super().__init__(*groups)
        self.space = space

        # Настройка физического тела
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (100, 100)))
        self.body.position = pos

        # Настройка формы для коллизий
        self.shape = pymunk.Poly.create_box(self.body, (100, 100))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        self.space.add(self.body, self.shape)

        # Обработчик коллизий
        handler = space.add_collision_handler(1, 2)
        handler.separate = self.handle_collision

        # Настройка спрайта
        self.image = pygame.transform.scale(Ship.imgs[0], (100, 100))
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0

        # Параметры движения
        self.acceleration = 60
        self.max_speed = Config.user_data["max_speed"]
        self.friction = 0.7

        # Параметры ускорения
        self.boost_active = False
        self.boost_available = True
        self.boost_start_time = 0
        self.boost_cooldown_start = 0
        self.boost_cooldown_progress = 1.0

        # Параметры щита
        self.shield_active = False
        self.shield_available = True
        self.shield_start_time = 0
        self.shield_cooldown_start = 0
        self.elapsed_shield_time = 10

        # Другое
        self.hp = Config.user_data["hp"]
        self.delivered = False

        # Границы мира
        self.world_width = Device.SCREEN_WIDTH * 3
        self.world_height = Device.SCREEN_HEIGHT * 4

        # Другое
        self.shield_surface = pygame.Surface((140, 140), pygame.SRCALPHA)

    def handle_collision(self, arbiter, space, data):
        if not self.shield_active:
            self.hp -= 1
        return True

    def update(self):
        # Обновляем позицию спрайта
        self.rect.center = self.body.position

        keys = pygame.key.get_pressed()
        current_time = time.time()

        # Управление поворотом
        if keys[Config.cfg["keymapping"]["left"]]:
            self.angle += 2
        if keys[Config.cfg["keymapping"]["right"]]:
            self.angle -= 2

        # Управление ускорением
        if (
                keys[Config.cfg["keymapping"]["boost"]]
                and self.boost_available
                and not self.boost_active
        ):
            self.boost_active = True
            self.boost_available = False
            self.boost_start_time = current_time

        if self.boost_active:
            elapsed_time = current_time - self.boost_start_time
            self.boost_cooldown_progress = max(
                0.0, 1.0 - (elapsed_time / Config.user_data["boost_time"])
            )
            if elapsed_time >= Config.user_data["boost_time"]:
                self.boost_active = False
                self.boost_cooldown_start = current_time
                self.boost_cooldown_progress = 0.0

        if not self.boost_available and not self.boost_active:
            elapsed_cooldown = current_time - self.boost_cooldown_start
            self.boost_cooldown_progress = min(
                1.0, elapsed_cooldown / Config.user_data["boost_cooldown"]
            )
            if self.boost_cooldown_progress >= 1.0:
                self.boost_available = True

        boost_multiplier = (
            Config.user_data["boost_multiplier"] if self.boost_active else 1
        )

        # Движение вперед
        if keys[Config.cfg["keymapping"]["up"]]:
            angle_rad = math.radians(self.angle)
            self.body.apply_force_at_local_point(
                (
                    -math.sin(angle_rad) * self.acceleration * boost_multiplier,
                    -math.cos(angle_rad) * self.acceleration * boost_multiplier,
                )
            )

        # Торможение
        if keys[Config.cfg["keymapping"]["break"]]:
            self.body.velocity *= 0.99

        # Щит
        if keys[Config.cfg["keymapping"]["shield"]]:
            if self.shield_available and not self.shield_active:
                self.shield_active = True
                self.shield_available = False
                self.shield_start_time = current_time

        if self.shield_active:
            self.shield_surface.fill((0, 0, 0, 0))
            pygame.draw.circle(
                self.shield_surface,
                Shield.COLOR,
                (
                    self.rect.x,
                    self.rect.y,
                ),
                Shield.RADIUS,
            )
            pygame.draw.circle(
                self.shield_surface,
                Shield.BORDER_COLOR,
                (
                    self.rect.x,
                    self.rect.y,
                ),
                Shield.RADIUS,
                2,
            )
            elapsed_time = current_time - self.shield_start_time
            if elapsed_time >= Config.user_data["shield_time"]:
                self.shield_active = False
                self.shield_cooldown_start = current_time

        if not self.shield_available and not self.shield_active:
            elapsed_time = current_time - self.shield_cooldown_start
            if elapsed_time >= Config.user_data["shield_cooldown"]:
                self.shield_available = True

        # Обновление спрайта
        sprite_index = min(max(0, 4 - self.hp), 3)
        self.image = pygame.transform.rotate(pygame.transform.scale(Ship.imgs[sprite_index], (100, 100)), self.angle)
        self.rect = self.image.get_rect(center=self.body.position)

        # Проверка границ карты
        if self.rect.left < 0:
            self.body.position = pymunk.Vec2d(self.rect.width / 2, self.body.position.y)
        elif self.rect.right > self.world_width:
            self.body.position = pymunk.Vec2d(
                self.world_width - self.rect.width / 2, self.body.position.y
            )

        if self.rect.top < 0:
            self.body.position = pymunk.Vec2d(
                self.body.position.x, Device.SCREEN_HEIGHT * 3 - self.rect.height / 2
            )
        elif self.rect.bottom > Device.SCREEN_HEIGHT * 3:
            self.body.position = pymunk.Vec2d(
                self.body.position.x, self.rect.height / 2
            )
