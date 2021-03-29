import pygame
import os
import colors
from main import WIDTH,HEIGHT

SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

VEL = 5
BULLET_VEL = 7



YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

class YellowPlayer():
    def __init__(self):
        self.YELLOW_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_yellow.png'))
        self.YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            self.YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
        self.player = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.x = self.player.x
        self.y = self.player.y
        self.width = self.player.width
        self.height = self.player.height
        self.bullets = []
        self.health = 10

    def draw(self,WIN):
        WIN.blit(self.YELLOW_SPACESHIP, (self.x, self.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, colors.YELLOW, bullet)
        healthBar = pygame.Rect(0,15, self.health * 15, 20)
        pygame.draw.rect(WIN, colors.RED, healthBar)

    def yellow_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x - VEL > 0:  # LEFT
            self.x -= VEL
        if keys_pressed[pygame.K_d] and self.x + VEL + self.width < BORDER.x:  # RIGHT
            self.x += VEL
        if keys_pressed[pygame.K_w] and self.y - VEL > 0:  # UP
            self.y -= VEL
        if keys_pressed[pygame.K_s] and self.y + VEL + self.width < HEIGHT:  # DOWN
            self.y += VEL

    def handle_bullets(self, red_player):
        for bullet in self.bullets:
            bullet.x += BULLET_VEL
            if red_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.bullets.remove(bullet)
            elif bullet.x > WIDTH:
                self.bullets.remove(bullet)


class RedPlayer():
    def __init__(self):
        self.RED_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_red.png'))
        self.RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(self.RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
        self.player = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.x = self.player.x
        self.y = self.player.y
        self.width = self.player.width
        self.height = self.player.height
        self.bullets = []
        self.health = 10

    def draw(self,WIN):
        WIN.blit(self.RED_SPACESHIP, (self.x, self.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, colors.RED, bullet)

    def red_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.x - VEL > BORDER.x:  # LEFT
            self.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and self.x + VEL + self.width < WIDTH:  # RIGHT
            self.x += VEL
        if keys_pressed[pygame.K_UP] and self.y - VEL > 0:  # UP
            self.y -= VEL
        if keys_pressed[pygame.K_DOWN] and self.y + VEL + self.width < HEIGHT:  # DOWN
            self.y += VEL

    def handleBullets(self, yellow_player):
        for bullet in self.bullets:
            bullet.x -= BULLET_VEL
            if yellow_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                self.bullets.remove(bullet)
            elif bullet.x < 0:
                self.bullets.remove(bullet)