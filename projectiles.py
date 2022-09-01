import pygame
import constants

class Laser(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image_set = [pygame.image.load('assets/laser_red.png'), pygame.image.load('assets/laser_white.png')]

        self.color = color
        self.image = self.image_set[self.color]
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2(0, 0)
        self.buffer_x = self.image.get_width() / 2
        self.buffer_y = self.image.get_height() / 2

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
    
    def update(self):
        self.move(constants.LASER_SPD)
        out_x = self.position.x < -self.buffer_x or self.position.x > constants.WIDTH + self.buffer_x
        out_y = self.position.y < -self.buffer_y or self.position.y > constants.WIDTH + self.buffer_y

        if out_x or out_y:
            self.kill()
