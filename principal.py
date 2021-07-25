import pygame
from pygame import *
from pygame.locals import *
import time
import sys
from pygame import mixer
from pygame import surface
import napoleon
from golf import *
from solitaire import *
from general_functions import *
import options


def golf(window):
    mixer.music.load('C:/Users/djjen/PycharmProjects/pythonProject2/Music/Melbourne_Bounce_2.wav')
    mixer.music.play(-1)

def napoleon(window):
    mixer.music.load('C:/Users/djjen/PycharmProjects/pythonProject2/Music/My_Song.ogg')
    mixer.music.play(-1)

def solitaire(window):
    mixer.music.load('C:/Users/djjen/PycharmProjects/pythonProject2/Music/Comback_Rewind.wav')
    mixer.music.play(-1)


def credit(window):
    mixer.music.load("credits.wav")
    mixer.music.play(-1)

    say_images = images("images/credits/")
    list_images = list(say_images)
    print(say_images, list_images)

    for i in range(len(say_images)):
        for j in range(255, 0, -4):
            window.blit(say_images[list_images[i]], (0, 0))
            window.fill((j, j, j), special_flags=BLEND_RGB_SUB)
            pygame.time.delay(15)
            pygame.display.flip()
        pygame.time.delay(5000)
        for j in range(0, 255, 4):
            window.fill(0x040404, special_flags=BLEND_RGB_SUB)
            pygame.time.delay(15)
            pygame.display.flip()
        pygame.time.delay(2000)

    main()


def main():
    pygame.init()
    pygame.display.set_caption("MIASHS")

    window = pygame.display.set_mode((1200, 675))

    say_images = images("images/menus/")

    back = pygame.image.load("images/back/back.png").convert()

    # default values
    type_cards = 'simpsons'
    game_size = 52
    number_packs = 1

    all_options = True

    while True:
        for event in pygame.event.get():
            mouseX, mouseY = pygame.mouse.get_pos()

            window.blit(say_images["back.png"], (0, 0))
            window.blit(say_images["klondike_off.png"], (50, 105))
            window.blit(say_images["napoleon_off.png"], (550, 105))
            window.blit(say_images["golf_off.png"], (50, 370))
            window.blit(say_images["coin_off.png"], (550, 395))

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:

                if 100 < mouseX < 500 + (150 * (1 - ((mouseY - 130) / 225))) and 130 < mouseY < 355:
                    print("klondike")
                    solitaire(window)
                if 500 + (200 * (1 - ((mouseY - 130) / 225))) < mouseX < 1100 and 130 < mouseY < 355:
                    print("napoleon")
                    napoleon(type_cards, game_size)
                if 100 < mouseX < 500 + (150 * (1 - ((mouseY - 405) / 225))) and 405 < mouseY < 630:
                    print("golf")
                    golf(type_cards,game_size)
                if 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 405 < mouseY < 466:
                    print("options")
                    type_cards, game_size, number_packs = options.options(window, type_cards, game_size, number_packs, all_options)
                if 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 487 < mouseY < 548:
                    print("credits")
                    credit(window)
                if 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 569 < mouseY < 630:
                    print("quitter")
                    pygame.quit()
                    sys.exit()

            elif event.type == MOUSEMOTION:
                if 100 < mouseX < 500 + (150 * (1 - ((mouseY - 130) / 225))) and 130 < mouseY < 355:
                    window.blit(say_images["klondike_on.png"], (50, 105))
                elif 500 + (200 * (1 - ((mouseY - 130) / 225))) < mouseX < 1100 and 130 < mouseY < 355:
                    window.blit(say_images["napoleon_on.png"], (550, 105))
                elif 100 < mouseX < 500 + (150 * (1 - ((mouseY - 405) / 225))) and 405 < mouseY < 630:
                    window.blit(say_images["golf_on.png"], (50, 370))
                elif 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 405 < mouseY < 466:
                    window.blit(say_images["coin_on1.png"], (550, 395))
                elif 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 487 < mouseY < 548:
                    window.blit(say_images["coin_on2.png"], (550, 395))
                elif 500 + (200 * (1 - ((mouseY - 405) / 225))) < mouseX < 1100 and 569 < mouseY < 630:
                    window.blit(say_images["coin_on3.png"], (550, 395))

        pygame.display.flip()


if __name__ == '__main__':
    main()
