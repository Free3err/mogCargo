import pygame
import math
import pymunk

from ...constants import Device


class Ship(pygame.sprite.Sprite):
    img = pygame.image.load("src/assets/img/entities/ship/based/1.png")

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.space = pymunk.Space()
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (200, 200)))
        self.shape = pymunk.Poly.create_box(self.body)
        self.space.add(self.body, self.shape)
        self.body.position = pos
        self.image = pygame.transform.scale(Ship.img, (100, 100))
        self.rect = self.image.get_rect(center=pos)

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
        if keys[pygame.K_a]:
            self.angle += 1
        if keys[pygame.K_d]:
            self.angle -= 1
        if keys[pygame.K_w]:
            angle_rad = math.radians(self.angle)
            self.body.apply_force_at_local_point(
                (
                    -math.sin(angle_rad) * self.acceleration * 2,
                    -math.cos(angle_rad) * self.acceleration * 2,
                )
            )

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
