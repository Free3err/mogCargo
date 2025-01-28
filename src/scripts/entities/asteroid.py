from random import randint, uniform
import pygame

class Asteroid(pygame.sprite.Sprite):
    img = pygame.image.load("src/assets/img/entities/asteroid.png")
    
    def __init__(self, pos):
        super().__init__()
        self.size = randint(10, 100)
        self.image = pygame.transform.scale(Asteroid.img, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        self.speed_x = -uniform(0.01, 0.1)
        self.speed_y = uniform(0.01, 0.1)
        
        self.x = float(pos[0])
        self.y = float(pos[1])
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y
