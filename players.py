import pygame
import os
import colors
from configs import *

pygame.init()

SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
MAX_HEALTH = 10

HEART_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'heart.png')), (40, 40))


SHIP_VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_health_bar(WIN, X, Y, health):
    bg = pygame.Rect(X, Y, 150, 20)
    pygame.draw.rect(WIN, colors.RED, bg, border_radius=3)

    health_bar = pygame.Rect(X, Y, health * 15, 20)
    pygame.draw.rect(WIN, colors.GREEN, health_bar, border_radius=3)

    WIN.blit(HEART_IMAGE, (X + 150 - HEART_IMAGE.get_width() // 2, Y))


class BlueShip():
    def __init__(self):
        self.BLUE_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_blue.png'))
        self.BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            self.BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
        self.player = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.width = self.player.width
        self.height = self.player.height
        self.bullets = []
        self.health = MAX_HEALTH

    def draw(self, WIN):
        WIN.blit(self.BLUE_SPACESHIP, (self.player.x, self.player.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, colors.YELLOW, bullet)

        draw_health_bar(WIN, 15, 15, self.health)

    def blue_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.player.x - SHIP_VEL > 0:  # LEFT
            self.player.x -= SHIP_VEL
        if keys_pressed[pygame.K_d] and self.player.x + SHIP_VEL + self.width < BORDER.x:  # RIGHT
            self.player.x += SHIP_VEL
        if keys_pressed[pygame.K_w] and self.player.y - SHIP_VEL > 0:  # UP
            self.player.y -= SHIP_VEL
        if keys_pressed[pygame.K_s] and self.player.y + SHIP_VEL + self.width < HEIGHT:  # DOWN
            self.player.y += SHIP_VEL

    def handle_bullets(self, red_player):
        for bullet in self.bullets:
            bullet.x += BULLET_VEL
            if red_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.bullets.remove(bullet)
            elif bullet.x > WIDTH:
                self.bullets.remove(bullet)


class RedShip():
    def __init__(self):
        self.RED_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_red.png'))
        self.RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(self.RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
        self.player = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.width = self.player.width
        self.height = self.player.height
        self.bullets = []
        self.health = MAX_HEALTH

    def draw(self, WIN):
        WIN.blit(self.RED_SPACESHIP, (self.player.x, self.player.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, colors.RED, bullet)

        draw_health_bar(WIN, WIDTH - 15 * MAX_HEALTH - HEART_IMAGE.get_width(), 15, self.health)

    def red_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.player.x - SHIP_VEL > BORDER.x:  # LEFT
            self.player.x -= SHIP_VEL
        if keys_pressed[pygame.K_RIGHT] and self.player.x + SHIP_VEL + self.width < WIDTH:  # RIGHT
            self.player.x += SHIP_VEL
        if keys_pressed[pygame.K_UP] and self.player.y - SHIP_VEL > 0:  # UP
            self.player.y -= SHIP_VEL
        if keys_pressed[pygame.K_DOWN] and self.player.y + SHIP_VEL + self.width < HEIGHT:  # DOWN
            self.player.y += SHIP_VEL

    def handleBullets(self, blue_player):
        for bullet in self.bullets:
            bullet.x -= BULLET_VEL
            if blue_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(BLUE_HIT))
                self.bullets.remove(bullet)
            elif bullet.x < 0:
                self.bullets.remove(bullet)
