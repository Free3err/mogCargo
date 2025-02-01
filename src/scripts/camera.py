import pygame
from ..constants import Device

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width * 3
        self.height = height * 3
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
        
    def update(self, target):
        x = -target.rect.centerx + Device.SCREEN_WIDTH // 2
        y = -target.rect.centery + Device.SCREEN_HEIGHT // 2
        
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - Device.SCREEN_WIDTH), x)
        y = max(-(self.height - Device.SCREEN_HEIGHT), y)
        
        self.camera = pygame.Rect(x, y, self.width, self.height) 