import pygame
import math
import pymunk

from ...constants import Device
from ...cfg.config import Config


class Ship(pygame.sprite.Sprite):
    img = pygame.image.load("src/assets/img/entities/ship/based/1.png")

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.space = pymunk.Space()
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (200, 200)))
        self.frames = {
            "idle": [
                pygame.image.load("src/assets/img/entities/ship/engines/idle.png").subsurface((i * 6, 0, 6, 6))
                for i in range(3)
            ],
            "engine": [
                pygame.image.load("src/assets/img/entities/ship/engines/powering.png").subsurface((i * 6, 0, 6, 6))
                for i in range(4)
            ]
        }
        self.shape = pymunk.Poly.create_box(self.body)
        self.space.add(self.body, self.shape)
        self.body.position = pos
        self.image = pygame.transform.scale(Ship.img, (100, 100))
        self.rect = self.image.get_rect(center=pos)
        self.engine_img = pygame.transform.scale(self.frames["idle"][0], (100, 100))
        self.current_frame = 0

        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 30
        self.max_speed = 10
        self.friction = 0.7
        self.angle = 0

    def update(self):
        self.space.step(1 / Device.SCREEN_REFRESH_RATE)
        self.rect.center = self.body.position

        keys = pygame.key.get_pressed()
        if keys[Config.cfg["keymapping"]["left"]]:
            self.angle += 1
        if keys[Config.cfg["keymapping"]["right"]]:
            self.angle -= 1
        if keys[Config.cfg["keymapping"]["up"]]:
            angle_rad = math.radians(self.angle)
            self.body.apply_force_at_local_point(
                (
                    -math.sin(angle_rad) * self.acceleration * 2,
                    -math.cos(angle_rad) * self.acceleration * 2,
                )
            )
        self.update_animation()
        self.image.blit(self.engine_img, (0, 0))
        self.image = pygame.transform.rotate(
            pygame.transform.scale(Ship.img, (100, 100)), self.angle
        )
        self.rect = self.image.get_rect(center=self.body.position)

        if self.rect.left < 0:
            self.body.position = pymunk.Vec2d(self.rect.width / 2, self.body.position.y)
        elif self.rect.right > Device.SCREEN_WIDTH:
            self.body.position = pymunk.Vec2d(
                Device.SCREEN_WIDTH - self.rect.width / 2, self.body.position.y
            )

        if self.rect.top < 0:
            self.body.position = pymunk.Vec2d(
                self.body.position.x, self.rect.height / 2
            )
        elif self.rect.bottom > Device.SCREEN_HEIGHT:
            self.body.position = pymunk.Vec2d(
                self.body.position.x, Device.SCREEN_HEIGHT - self.rect.height / 2
            )
            
    def update_animation(self):
        if pygame.time.get_ticks() % 20 == 0:
            if pygame.key.get_pressed()[Config.cfg["keymapping"]["up"]]:
                self.current_frame = (self.current_frame + 1) % 4
                self.engine_img = pygame.transform.scale(self.frames["engine"][self.current_frame], (100, 100))
            else:
                self.current_frame = (self.current_frame + 1) % 3
                self.engine_img = pygame.transform.scale(self.frames["idle"][self.current_frame], (100, 100))
