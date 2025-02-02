from random import choice

import pygame.sprite
import pymunk


class Planet(pygame.sprite.Sprite):
    imgs = [
        pygame.image.load("src/assets/img/entities/planet/1.png"),
        pygame.image.load("src/assets/img/entities/planet/2.png"),
        pygame.image.load("src/assets/img/entities/planet/3.png"),
    ]

    def __init__(self, pos, space, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type

        # Настройка спрайта
        self.original_image = pygame.transform.scale(choice(Planet.imgs), (250, 250))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        
        # Параметры вращения
        self.angle = 0
        self.rotation_speed = choice([-0.1, 0.1])

        # Настройка физического тела
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos

        # Настройка формы для коллизий
        self.shape = pymunk.Circle(self.body, self.rect.width // 2)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.shape.collision_type = 3
        space.add(self.body, self.shape)

    def update(self):
        self.angle += self.rotation_speed
    
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
