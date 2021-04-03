import players as pl
import pygame
import os
import colors
from window_configs import *
from sounds import *

pygame.init()
pygame.font.init()


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Maniac")

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def render_text(text):
    DISPLAY_TEXT = pygame.font.SysFont(
        'comicsans', 100).render(str(text), True, colors.WHITE)
    WIN.blit(DISPLAY_TEXT, (WIDTH//2 - DISPLAY_TEXT.get_width() //
                            2, HEIGHT//2 - DISPLAY_TEXT.get_height()//2))
    pygame.display.update()


def who_wins(redPlayer, bluePlayer):
    winner = ""
    if redPlayer.health <= 0:
        winner = "Blue Wins!"

    if bluePlayer.health <= 0:
        winner = "Red Wins!"

    if winner != "":
        SPACE_EXPLOSION.play()
        render_text(winner)
        pygame.time.delay(1000)
        draw_window(redPlayer, bluePlayer)
        COUNTDOWN = 5
        while COUNTDOWN >= 0:
            render_text(f"Restart in {COUNTDOWN}")
            pygame.time.delay(1000)
            draw_window(redPlayer, bluePlayer)
            COUNTDOWN -= 1
        return 1
    return 0


def draw_window(redPlayer, bluePlayer):

    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    bluePlayer.draw(WIN)
    redPlayer.draw(WIN)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    bluePlayer = pl.BluePlayer()
    redPlayer = pl.RedPlayer()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bluePlayer.bullets) < pl.MAX_BULLETS:
                    bullet = pygame.Rect(
                        bluePlayer.x + bluePlayer.width, bluePlayer.y + bluePlayer.height//2 - 2, 10, 5)
                    bluePlayer.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(redPlayer.bullets) < pl.MAX_BULLETS:
                    bullet = pygame.Rect(
                        redPlayer.x, redPlayer.y + redPlayer.height//2 - 2, 10, 5)
                    redPlayer.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pl.RED_HIT:
                BULLET_HIT_SOUND.play()
                redPlayer.health -= 1

            if event.type == pl.BLUE_HIT:
                BULLET_HIT_SOUND.play()
                bluePlayer.health -= 1

        keys_pressed = pygame.key.get_pressed()

        bluePlayer.blue_movement(keys_pressed)
        bluePlayer.handle_bullets(redPlayer.player)

        redPlayer.red_movement(keys_pressed)
        redPlayer.handleBullets(bluePlayer.player)

        if who_wins(redPlayer, bluePlayer) == 1:
            break
        draw_window(redPlayer, bluePlayer)
    main()


if __name__ == '__main__':
    main()
