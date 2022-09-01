import pygame
import constants
from projectiles import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, laser_group: pygame.sprite.Group):
        super().__init__()
        self.image_set = [pygame.image.load('assets/player_red.png'), pygame.image.load('assets/player_white.png')]
        
        self.color = 0
        self.image = self.image_set[self.color]
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(self.rect.center)
        self.buffer_x = self.image.get_width() / 2
        self.buffer_y = self.image.get_height() / 2

        self.input = []
        self.cycle_ready = True
        self.fire_ready = True

        self.laser_group = laser_group

    def set_position(self, new_position):
        new_position = pygame.Vector2(new_position)
        self.position = new_position
        self.rect.center = [int(self.position.x), int(self.position.y)]

    def move(self, direction):
        direction = pygame.Vector2(direction)
        direction.scale_to_length(constants.PLAYER_SPD)
        self.set_position(self.position + direction)

        if self.position.x < self.buffer_x:
            self.set_position((self.buffer_x, self.position.y))
        
        if self.position.x > constants.WIDTH - self.buffer_x:
            self.set_position((constants.WIDTH - self.buffer_x, self.position.y))

    def cycle_color(self):
        if self.color == 0:
            self.color = 1
        elif self.color == 1:
            self.color = 0
        self.image = self.image_set[self.color]
        self.cycle_ready = False
    
    def handle_input(self):
        self.input = pygame.key.get_pressed()

        if self.input[pygame.K_LEFT]:
            self.move((-1, 0))
        if self.input[pygame.K_RIGHT]:
            self.move((1, 0))
        
        if self.input[pygame.K_LSHIFT] and self.cycle_ready:
            self.cycle_color()
        elif not self.input[pygame.K_LSHIFT]:
            self.cycle_ready = True
        
        if self.input[pygame.K_SPACE] and self.fire_ready:
            laser = Laser(self.color)
            laser.set_position(self.position)
            laser.set_direction((0, -1))
            self.laser_group.add(laser)
            self.fire_ready = False
        elif not self.input[pygame.K_SPACE]:
            self.fire_ready = True
