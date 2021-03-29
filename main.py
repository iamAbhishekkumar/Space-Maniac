# TODO : fix health bars,rematch in 5 seconds dialog


import players as pl
import pygame
import os
import colors
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

FPS = 60
MAX_BULLETS = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Maniac")

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'damage.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gunFire.wav'))
SPACE_EXPLOSION = pygame.mixer.Sound(os.path.join('Assets', 'explosion.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
HEART_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'heart.png')), (30, 30))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, colors.WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()


def who_wins(red_health, yellow_health):
    winner = ""
    if red_health <= 0:
        winner = "Yellow Wins!"

    if yellow_health <= 0:
        winner = "Red Wins!"

    if winner != "":
        # SPACE_EXPLOSION.play()
        draw_winner(winner)

        return 1
    return 0


def draw_window(redPlayer, yellowPlayer):
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    yellowPlayer.draw(WIN)
    redPlayer.draw(WIN)

    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    yellowPlayer = pl.YellowPlayer()
    redPlayer = pl.RedPlayer()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowPlayer.bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellowPlayer.x + yellowPlayer.width, yellowPlayer.y + yellowPlayer.height//2 - 2, 10, 5)
                    yellowPlayer.bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(redPlayer.bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        redPlayer.x, redPlayer.y + redPlayer.height//2 - 2, 10, 5)
                    redPlayer.bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            if event.type == pl.RED_HIT:
                # BULLET_HIT_SOUND.play()
                redPlayer.health -= 1

            if event.type == pl.YELLOW_HIT:
                # BULLET_HIT_SOUND.play()
                yellowPlayer.health -= 1

        keys_pressed = pygame.key.get_pressed()

        yellowPlayer.yellow_movement(keys_pressed)
        yellowPlayer.handle_bullets(redPlayer.player)

        redPlayer.red_movement(keys_pressed)
        redPlayer.handleBullets(yellowPlayer.player)

        if who_wins(redPlayer.health, yellowPlayer.health) == 1:
            pygame.time.delay(5000)
            break
        draw_window(redPlayer, yellowPlayer)
    main()


if __name__ == '__main__':
    main()
