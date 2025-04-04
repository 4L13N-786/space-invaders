import pygame # type: ignore
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraints, speed):
        super().__init__()
        self.image = pygame.image.load("graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraints
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 500

        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound("audio/laser.wav")
        self.laser_sound.set_volume(0.5)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
    
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
        
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, 8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
        

        
