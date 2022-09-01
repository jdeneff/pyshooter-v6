import pygame
import constants
from random import randint

class AbstractStar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 0
        self.position = pygame.Vector2((randint(0, constants.WIDTH), -5))
        self.direction = pygame.Vector2((0, 1))

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image.fill(constants.CLEAR)
        self.center = (10, 10)
    
    def set_position(self, new_position):
        pass

    def update(self):
        self.position += self.speed * self.direction
        self.set_position(self.position)
        if self.position.y > constants.HEIGHT + 10:
            self.kill()

class SmallStar(AbstractStar):
    def __init__(self):
        super().__init__()
        self.rect = pygame.draw.circle(self.image, constants.GRAY1, self.center, 2)
        self.speed = 1
    
    def set_position(self, new_position):
        self.position = pygame.Vector2(new_position)
        self.rect.center = (int(self.position.x), int(self.position.y))
    
class MedStar(AbstractStar):
    def __init__(self):
        super().__init__()
        self.rect = pygame.draw.circle(self.image, constants.GRAY2, self.center, 3)
        self.speed = 2
    
    def set_position(self, new_position):
        self.position = pygame.Vector2(new_position)
        self.rect.center = (int(self.position.x), int(self.position.y))

class BigStar(AbstractStar):
    def __init__(self):
        super().__init__()
        self.rect = pygame.draw.circle(self.image, constants.GRAY3, self.center, 4)
        self.speed = 3
    
    def set_position(self, new_position):
        self.position = pygame.Vector2(new_position)
        self.rect.center = (int(self.position.x), int(self.position.y))

class StarMaker:
    def __init__(self):
        self.small_int = 20
        self.med_int = 5
        self.big_int = 1
    
    def spawn_stars(self, sprite_group):
        small_num = randint(0, 59)
        med_num = randint(0, 59)
        big_num = randint(0, 59)

        if small_num < self.small_int:
            star = SmallStar()
            sprite_group.add(star)

        if med_num < self.med_int:
            star = MedStar()
            sprite_group.add(star)

        if big_num < self.big_int:
            star = BigStar()
            sprite_group.add(star)