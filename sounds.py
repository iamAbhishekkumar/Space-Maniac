import pygame
import os
pygame.init()
pygame.mixer.init()


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'damage.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gunFire.wav'))
SPACE_EXPLOSION = pygame.mixer.Sound(os.path.join('Assets', 'explosion.wav'))