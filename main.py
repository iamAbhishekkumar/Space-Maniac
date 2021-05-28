try:
    import players as pl
    import pygame
    import os
    import colors
    from configs import *
    from sounds import *
    import pygame_menu
except ImportError:
    print("Please ....fulfil requirements")

pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Maniac")

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def render_text(text):
    DISPLAY_TEXT = pygame.font.SysFont(
        'comicsans', 100).render(str(text), True, colors.WHITE)
    WIN.blit(DISPLAY_TEXT, (WIDTH // 2 - DISPLAY_TEXT.get_width() //
                            2, HEIGHT // 2 - DISPLAY_TEXT.get_height() // 2))
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


def start_the_game():
    clock = pygame.time.Clock()
    blue_player = pl.BlueShip()
    red_player = pl.RedShip()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_player.bullets) < pl.MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue_player.player.x + blue_player.width, blue_player.player.y + blue_player.height // 2 - 2, 10, 5)
                    blue_player.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_player.bullets) < pl.MAX_BULLETS:
                    bullet = pygame.Rect(
                        red_player.player.x, red_player.player.y + red_player.height // 2 - 2, 10, 5)
                    red_player.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pl.RED_HIT:
                BULLET_HIT_SOUND.play()
                red_player.health -= 1

            if event.type == pl.BLUE_HIT:
                BULLET_HIT_SOUND.play()
                blue_player.health -= 1

        keys_pressed = pygame.key.get_pressed()

        blue_player.blue_movement(keys_pressed)
        red_player.red_movement(keys_pressed)
        blue_player.handle_bullets(red_player.player)
        red_player.handleBullets(blue_player.player)

        if who_wins(red_player, blue_player) == 1:
            break
        draw_window(red_player, blue_player)
    start_the_game()


def main():
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.display.update()

    menu = pygame_menu.Menu(MENU_WIDTH, MENU_HEIGHT,
                            'Welcome', theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :', default='Your Name')
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN)


if __name__ == '__main__':
    main()
