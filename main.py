import pygame
import constants
from player import Player
from enemy import Enemy
from starScroll import StarMaker
from random import randint

class Spawner:
    def __init__(self, rows, cols):
        row_interval = int(constants.HEIGHT / 2 / (rows + 1))
        col_interval = int(constants.WIDTH / (cols + 1))
        row_coordinate = list(range(row_interval, int(constants.HEIGHT) - row_interval + 1, row_interval))
        col_coordinate = list(range(col_interval, constants.WIDTH - col_interval + 1, col_interval))
        self.grid = []
        for i in range(0, cols, 1):
            for j in range(0, rows, 1):
                self.grid.append((col_coordinate[i], row_coordinate[j]))
        self.spawn_limit = 5
        self.increase_chance = 10

    def spawn_enemy(self, enemy_group: pygame.sprite.Group, laser_group: pygame.sprite.Group):
        print(self.spawn_limit)
        increase = randint(1, 100)
        if increase < self.increase_chance and self.spawn_limit < len(self.grid):
            self.spawn_limit += 1
        
        enemy_number = randint(self.spawn_limit - 4, self.spawn_limit)
        i = 0
        if len(enemy_group) == 0:
            while i < enemy_number:
                spawn_x = randint(0, constants.WIDTH)
                index = randint(0, len(self.grid) - 1)
                target_position = self.grid[index]
                self.grid.remove(target_position)
                spawn_color = randint(0,1)
        
                enemy = Enemy(laser_group)
                if spawn_color == 1:
                    enemy.cycle_color()
                enemy.set_position((spawn_x, -enemy.buffer_y))
                enemy.set_target(target_position)
                enemy.set_direction((enemy.target - enemy.position).normalize())

                enemy_group.add(enemy)
                i += 1

    def kill_enemy(self, enemy: Enemy):
        self.grid.append(enemy.target)
        enemy.kill()

class Game:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.screen.fill('black')
        self.clock = pygame.time.Clock()

        self.run = True
    
        self.play_screen = StarMaker()
        self.star_group = pygame.sprite.Group()

        self.player_laser_group = pygame.sprite.Group()

        self.player_group = pygame.sprite.GroupSingle()

        self.enemy_group = pygame.sprite.Group()
        self.enemy_laser_group = pygame.sprite.Group()

        self.spawner = Spawner(4, 5)

        self.state = 0
        self.score = 0
        self.last_score = 0
    
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 30)
        self.splash_text_1 = self.font.render('PRESS UP TO PLAY', True, 'white')
        self.splash_rect_1 = self.splash_text_1.get_rect(center = (constants.WIDTH / 2, constants.HEIGHT / 2))
        self.splash_text_2 = self.font.render('RED KILLS WHITE, WHITE KILLS RED', True, 'white')
        self.splash_rect_2 = self.splash_text_2.get_rect(midtop = (self.splash_rect_1.midbottom))

    def collisions(self):
        for laser in self.enemy_laser_group:
            if pygame.sprite.collide_rect(self.player, laser) and laser.color != self.player.color:
                self.state = 0
                self.reset()

        for laser in self.player_laser_group:
            for enemy in self.enemy_group:
                if pygame.sprite.collide_rect(enemy, laser) and laser.color != enemy.color:
                    self.score += 1
                    self.spawner.kill_enemy(enemy)
                    laser.kill()
    
    def reset(self):
        self.player.set_position((constants.WIDTH / 2, constants.HEIGHT - (2 * self.player.buffer_y)))
        self.last_score = self.score
        self.score = 0
        self.star_group.empty()
        self.player_group.empty()
        for enemy in self.enemy_group:
            self.spawner.kill_enemy(enemy)
        self.enemy_laser_group.empty()
        self.player_laser_group.empty()

    def run_game(self):
        while self.run:
            if self.state == 0:
                pygame.display.set_caption(f'LAST SCORE: {self.last_score}')
                self.screen.fill('black')
                self.screen.blit(self.splash_text_1, self.splash_rect_1)
                self.screen.blit(self.splash_text_2, self.splash_rect_2)
                pygame.display.flip()
                self.clock.tick(60)

            if self.state == 1:
                self.play_screen.spawn_stars(self.star_group)
                
                self.star_group.update()
                self.player.handle_input()
                self.player_laser_group.update()
                self.enemy_laser_group.update()
                self.enemy_group.update()
                if len(self.enemy_group) == 0:
                    self.spawner.spawn_enemy(self.enemy_group, self.enemy_laser_group)
                self.collisions()
                
                pygame.display.set_caption(f'SCORE: {self.score}')

                self.screen.fill('black')
                self.star_group.draw(self.screen)
                self.player_laser_group.draw(self.screen)
                self.player_group.draw(self.screen)
                self.enemy_laser_group.draw(self.screen)
                self.enemy_group.draw(self.screen)

                pygame.display.flip()       
                self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if self.state == 0:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.state = 1
                        self.player = Player(self.player_laser_group)
                        self.player.set_position((constants.WIDTH / 2, constants.HEIGHT - (2 * self.player.buffer_y)))
                        self.player_group.add(self.player)
                        pygame.time.wait(500)

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run_game()
    pygame.quit()