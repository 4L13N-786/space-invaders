import pygame # type: ignore
import sys
from random import choice, randint
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser

class Game:
    def __init__(self):

        # ==== PLAYER ==== #
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, 3)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #==== HEALTH & SCORE ==== #
        self.lives = 3
        self.live_surf = pygame.image.load("graphics/player.png").convert_alpha()
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 + 20)

        self.score = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 15)


        #==== OBSTACLES ==== #
        self.shape = obstacle.shape
        self.block_size = 4
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (SCREEN_WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = SCREEN_WIDTH / 15, y_start = 315)

        #==== ALIENS ==== #
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        #==== EXTRA ALIEN ==== #
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        #==== MUSIC ==== #
        music = pygame.mixer.Sound("audio/music.wav")
        music.set_volume(0.2)
        music.play(loops = -1)

        self.laser_sound = pygame.mixer.Sound("audio/laser.wav")
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (255, 0, 0), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
    
    def alien_setup(self, rows, cols, x_distance = 40, y_distance = 28, x_offset = 50, y_offset = 70):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien("yellow", x, y)
                elif 1 <= row_index <= 2: alien_sprite = Alien("green", x, y)
                else: alien_sprite = Alien("red", x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    
    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["left", "right"]), SCREEN_WIDTH))
            self.extra_spawn_time = randint(400, 800)

    def collisions_checks(self):
        # ==== PLAYER LASERS ==== #
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()
        
        # ==== ALIEN LASERS ==== #
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()   
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
                    
    def display_lives(self): 
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f"SCORE: {self.score}", False, (255, 255, 255))
        score_rect = score_surf.get_rect(topleft = (10, 0))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render("YOU WON!", False, (255, 255, 255))
            victory_rect = victory_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(victory_surf, victory_rect)   

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collisions_checks()
        
        self.player.sprite.lasers.draw(screen) 
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load("graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        self.tv.set_alpha(150)
        screen.blit(self.tv, (0, 0))

if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SPACE INVADERS")
    clock = pygame.time.Clock()
    FPS = 60
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        crt.draw()

        pygame.display.update()
        clock.tick(FPS) 
