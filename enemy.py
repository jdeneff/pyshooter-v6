import pygame
import constants
from projectiles import Laser
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, laser_group):
        super().__init__()
        self.image_set = [pygame.image.load('assets/enemy_red.png'), pygame.image.load('assets/enemy_white.png')]
        
        self.color = 0
        self.image = self.image_set[self.color]
        self.rect = self.image.get_rect()

        self.state = 0

        self.position = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, 0)
        self.target = pygame.Vector2(0, 0)

        self.buffer_x = self.image.get_width() / 2
        self.buffer_y = self.image.get_height() / 2

        self.margin = 20

        self.fire_int = 1

        self.laser_group = laser_group

    def set_target(self, target):
        target = pygame.Vector2(target)
        self.target = target

    def set_position(self, new_position):
        new_position = pygame.Vector2(new_position)
        self.position = new_position
        self.rect.center = [int(self.position.x), int(self.position.y)]

    def set_direction(self, new_direction):
        new_direction = pygame.Vector2(new_direction)
        new_direction.normalize()
        self.direction = new_direction

    def move(self, speed):
        self.direction.scale_to_length(speed)
        self.set_position(self.position + self.direction)
        self.direction.normalize()
    
    def cycle_color(self):
        if self.color == 0:
            self.color = 1
        elif self.color == 1:
            self.color = 0
        self.image = self.image_set[self.color]
    
    def fire_laser(self):
        laser = Laser(self.color)
        laser.set_position(self.position)
        laser.set_direction((0, 1))
        self.laser_group.add(laser)

    def move_to(self):
        distance = self.position.distance_to(self.target)
        if distance > constants.ENEMY_SPD:
            self.move(constants.ENEMY_SPD)
        elif distance < constants.ENEMY_SPD and distance > 0:
            self.set_position(self.target)
            self.set_direction((1, 0))
            self.state += 1

    def wiggle(self):
        if self.position.x >= self.target.x + self.margin:
            self.set_direction((-1, 0))
        if self.position.x < self.target.x - self.margin:
            self.set_direction((1, 0))
        self.move(1)

        fire_prob = randint(0, 239)
        if fire_prob < self.fire_int:
            self.fire_laser()
    
    def update(self):
        if self.state == 0:
            self.move_to()
        elif self.state == 1:
            self.wiggle()

