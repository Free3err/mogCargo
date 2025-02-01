from random import randint, uniform
import pygame
import pymunk
import math

from ...constants import Device

class Asteroid(pygame.sprite.Sprite):
    img = pygame.image.load("src/assets/img/entities/asteroid.png")
    
    def __init__(self, pos, space):
        super().__init__()
        
        # Инициализация размера и изображения
        self.size = randint(80, 200)
        self.image = pygame.transform.scale(Asteroid.img, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        # Настройка физического тела
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.size // 2))
        self.body.position = pos
        
        # Настройка формы для коллизий
        self.shape = pymunk.Circle(self.body, self.size // 2)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        self.shape.collision_type = 2
        space.add(self.body, self.shape)
        
        # Настройка движения
        angle = uniform(0, 2 * math.pi)
        speed = uniform(20, 60)
        self.body.velocity = (speed * math.cos(angle), speed * math.sin(angle))
        self.body.angular_velocity = uniform(-1, 1)
        
        # Время следующего импульса
        self.next_impulse = pygame.time.get_ticks() + randint(1000, 3000)
    
    def update(self):
        # Обновляем позицию спрайта
        self.rect.center = self.body.position
        
        # Проверяем необходимость добавления случайного импульса
        current_time = pygame.time.get_ticks()
        if current_time > self.next_impulse:
            # Генерируем случайный импульс
            impulse_angle = uniform(0, 2 * math.pi)
            impulse_force = uniform(10, 40)  # Уменьшили силу импульса с 20-100 до 10-40
            
            # Применяем импульс к астероиду
            self.body.apply_impulse_at_local_point(
                (impulse_force * math.cos(impulse_angle),
                 impulse_force * math.sin(impulse_angle))
            )
            
            # Устанавливаем время следующего импульса
            self.next_impulse = current_time + randint(1000, 3000)
        
        # Обновляем изображение с учетом поворота
        self.image = pygame.transform.rotate(
            pygame.transform.scale(Asteroid.img, (self.size, self.size)),
            math.degrees(self.body.angle)
        )
        self.rect = self.image.get_rect(center=self.body.position)
        
        # Удаляем астероид, если он вышел за границы
        if (self.body.position.x < 0 or
            self.body.position.x > Device.SCREEN_WIDTH * 3 or
            self.body.position.y < 0 or
            self.body.position.y > Device.SCREEN_HEIGHT * 4):
            self.kill()
