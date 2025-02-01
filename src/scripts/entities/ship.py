import pygame
import math
import pymunk
import time

from ...constants import Device
from ...cfg.config import Config


class Ship(pygame.sprite.Sprite):
    img = pygame.image.load("src/assets/img/entities/ship/based/1.png")

    def __init__(self, pos, space, *groups):
        super().__init__(*groups)
        self.space = space
        
        # Настройка физического тела
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (100, 100)))
        self.body.position = pos
        
        # Настройка формы для коллизий
        self.shape = pymunk.Poly.create_box(self.body, (100, 100))
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        self.shape.collision_type = 1
        self.space.add(self.body, self.shape)
        
        # Загрузка анимаций
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
        
        # Настройка спрайта
        self.image = pygame.transform.scale(Ship.img, (100, 100))
        self.rect = self.image.get_rect(center=pos)
        self.engine_img = pygame.transform.scale(self.frames["idle"][0], (100, 100))
        self.current_frame = 0

        # Параметры движения
        self.acceleration = 30
        self.max_speed = 10
        self.friction = 0.7
        self.angle = 0
        
        # Параметры ускорения
        self.boost_active = False
        self.boost_start_time = 0
        self.boost_cooldown_start = 0

        # Границы мира
        self.world_width = Device.SCREEN_WIDTH * 3
        self.world_height = Device.SCREEN_HEIGHT * 4

    def update(self):
        # Обновляем позицию спрайта
        self.rect.center = self.body.position

        keys = pygame.key.get_pressed()
        current_time = time.time()
        
        # Управление поворотом
        if keys[Config.cfg["keymapping"]["left"]]:
            self.angle += 1
        if keys[Config.cfg["keymapping"]["right"]]:
            self.angle -= 1
            
        # Управление ускорением
        if keys[Config.cfg["keymapping"]["boost"]] and not self.boost_active:
            if current_time - self.boost_cooldown_start >= Config.user_data["boost_cooldown"]:
                self.boost_active = True
                self.boost_start_time = current_time
                
        if self.boost_active:
            if current_time - self.boost_start_time >= Config.user_data["boost_time"]:
                self.boost_active = False
                self.boost_cooldown_start = current_time
                
        boost_multiplier = 1.5 if self.boost_active else 1
            
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

        # Обновление анимации и спрайта
        self.update_animation()
        self.image.blit(self.engine_img, (0, 0))
        self.image = pygame.transform.rotate(
            pygame.transform.scale(Ship.img, (100, 100)), 
            self.angle
        )
        self.rect = self.image.get_rect(center=self.body.position)

        # Проверка границ карты
        if self.rect.left < 0:
            self.body.position = pymunk.Vec2d(self.rect.width / 2, self.body.position.y)
        elif self.rect.right > self.world_width:
            self.body.position = pymunk.Vec2d(
                self.world_width - self.rect.width / 2, 
                self.body.position.y
            )

        if self.rect.top < 0:
            self.body.position = pymunk.Vec2d(
                self.body.position.x, 
                self.rect.height / 2
            )
        elif self.rect.bottom > self.world_height:
            self.body.position = pymunk.Vec2d(
                self.body.position.x,
                self.world_height - self.rect.height / 2
            )
            
    def update_animation(self):
        if pygame.time.get_ticks() % 20 == 0:
            keys = pygame.key.get_pressed()
            
            # Анимация двигателя при движении вперед
            if keys[Config.cfg["keymapping"]["up"]] and not keys[Config.cfg["keymapping"]["break"]]:
                self.current_frame = (self.current_frame + 1) % 4
                self.engine_img = pygame.transform.scale(
                    self.frames["engine"][self.current_frame], 
                    (100, 100)
                )
            
            # Анимация при AFK
            else:
                self.current_frame = (self.current_frame + 1) % 3
                self.engine_img = pygame.transform.scale(
                    self.frames["idle"][self.current_frame], 
                    (100, 100)
                )
