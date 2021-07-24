import pygame
from pygame.locals import *
import sys
import os
import time
from random import *


def main():
    pygame.init()
    window = pygame.display.set_mode((1200, 675))
    options(window, 'simpsons', 52, 1, True)
    pygame.quit()
    sys.exit()


def options(window, type_cards, game_size, number_packs, all_options):
    windowX, windowY = window.get_size()

    list_images = os.listdir("images/menu_option/")

    say_images = {}

    for element in list_images:
        say_images[element] = pygame.image.load("images/menu_option/" + element).convert_alpha()

    say_images["blur.png"] = pygame.transform.scale(say_images["blur.png"], (windowX, windowY))

    restart = False

    # hide the game in progress, we blame it here so that it doesn't crash many times
    if not all_options:
        window.blit(say_images["blur.png"], (0, 0))

    while True:

        mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if 50 <= mouseX <= 350 and 170 <= mouseY <= 390:
                    if type_cards != "simpsons":
                        type_cards = "simpsons"
                elif 350 <= mouseX <= 650 and 170 <= mouseY <= 390:
                    if type_cards != "pokemon":
                        type_cards = "pokemon"
                elif 50 <= mouseX <= 350 and 420 <= mouseY <= 740:
                    if type_cards != "classic":
                        type_cards = "classic"
                # for the restart button
                elif not all_options and 650 <= mouseX <= 775 and 550 <= mouseY <= 675:
                    if restart:
                        restart = False
                    else:
                        restart = True
                # for the arrow back to play
                elif 730 <= mouseX <= 760 and 40 <= mouseY <= 70:
                    if all_options:
                        return (type_cards, game_size, number_packs)
                    else:
                        return (type_cards, restart)

                ## if all_options, for the size of the game
                elif all_options and 800 <= mouseX <= 900 and 180 <= mouseY <= 330:
                    game_size = 28
                elif all_options and 1000 <= mouseX <= 1100 and 180 <= mouseY <= 330:
                    game_size = 32
                elif all_options and 900 <= mouseX <= 1000 and 335 <= mouseY <= 485:
                    game_size = 52
                elif all_options and 800 <= mouseX <= 900 and 490 <= mouseY <= 640:
                    game_size = 56
                elif all_options and 1000 <= mouseX <= 1100 and 490 <= mouseY <= 640:
                    game_size = 64

                # for the number of packages
                elif 430 <= mouseX <= 480 and 510 <= mouseY <= 560:
                    number_packs = 1
                elif 540 <= mouseX <= 590 and 510 <= mouseY <= 560:
                    number_packs = 2
                elif 430 <= mouseX <= 480 and 575 <= mouseY <= 625:
                    number_packs = 3
                elif 540 <= mouseX <= 590 and 575 <= mouseY <= 625:
                    number_packs = 4

        # poster background
        if all_options:
            window.blit(say_images["full_back.png"], (0, 0))

        # display the text
        if all_options:
            window.blit(say_images["full_text.png"], (0, 0))
        else:
            window.blit(say_images["text.png"], (0, 0))

        # Displays the back arrow
        window.blit(say_images["retour.png"], (730, 40))
        # Displays if the mouse is over the back arrow
        if 730 <= mouseX <= 760 and 40 <= mouseY <= 70:
            window.blit(say_images["retour_select.png"], (730, 40))

        # show the simpsons
        if type_cards == "simpsons":
            window.blit(say_images["options_simpsons_color.png"], (50, 170))
        else:
            window.blit(say_images["options_simpsons_gray.png"], (50, 170))
        if 50 <= mouseX <= 350 and 170 <= mouseY <= 390:
            window.blit(say_images["options_simpsons_color.png"], (50, 170))

            # displays the pokemon
        if type_cards == "pokemon":
            window.blit(say_images["options_pokemon_color.png"], (350, 170))
        else:
            window.blit(say_images["options_pokemon_gray.png"], (350, 170))
        if 350 <= mouseX <= 650 and 170 <= mouseY <= 390:
            window.blit(say_images["options_pokemon_color.png"], (350, 170))

        # displays the classic
        if type_cards == "classic":
            window.blit(say_images["options_classic_color.png"], (50, 420))
        else:
            window.blit(say_images["options_classic_gray.png"], (50, 420))
        if 50 <= mouseX <= 350 and 420 <= mouseY <= 740:
            window.blit(say_images["options_classic_color.png"], (50, 420))

        # if all_options, display card packs
        if all_options:
            # displays 28 cards
            if game_size == 28:
                window.blit(say_images["28_color.png"], (800, 180))
                window.blit(say_images["32_gray.png"], (1000, 180))
                window.blit(say_images["52_gray.png"], (900, 335))
                window.blit(say_images["56_gray.png"], (800, 490))
                window.blit(say_images["64_gray.png"], (1000, 490))
            # displays 32 cards
            elif game_size == 32:
                window.blit(say_images["28_gray.png"], (800, 180))
                window.blit(say_images["32_color.png"], (1000, 180))
                window.blit(say_images["52_gray.png"], (900, 335))
                window.blit(say_images["56_gray.png"], (800, 490))
                window.blit(say_images["64_gray.png"], (1000, 490))
            # displays 52 cards
            elif game_size == 52:
                window.blit(say_images["28_gray.png"], (800, 180))
                window.blit(say_images["32_gray.png"], (1000, 180))
                window.blit(say_images["52_color.png"], (900, 335))
                window.blit(say_images["56_gray.png"], (800, 490))
                window.blit(say_images["64_gray.png"], (1000, 490))
            # displays 56 cards
            elif game_size == 56:
                window.blit(say_images["28_gray.png"], (800, 180))
                window.blit(say_images["32_gray.png"], (1000, 180))
                window.blit(say_images["52_gray.png"], (900, 335))
                window.blit(say_images["56_color.png"], (800, 490))
                window.blit(say_images["64_gray.png"], (1000, 490))
            # displays 64 cards
            elif game_size == 64:
                window.blit(say_images["28_gray.png"], (800, 180))
                window.blit(say_images["32_gray.png"], (1000, 180))
                window.blit(say_images["52_gray.png"], (900, 335))
                window.blit(say_images["56_gray.png"], (800, 490))
                window.blit(say_images["64_color.png"], (1000, 490))
            # displays if the mouse is over it
            if 800 <= mouseX <= 900 and 180 <= mouseY <= 330:
                window.blit(say_images["28_color.png"], (800, 180))
            elif 1000 <= mouseX <= 1100 and 180 <= mouseY <= 330:
                window.blit(say_images["32_color.png"], (1000, 180))
            elif 900 <= mouseX <= 1000 and 335 <= mouseY <= 485:
                window.blit(say_images["52_color.png"], (900, 335))
            elif 800 <= mouseX <= 900 and 490 <= mouseY <= 640:
                window.blit(say_images["56_color.png"], (800, 490))
            elif 1000 <= mouseX <= 1100 and 490 <= mouseY <= 640:
                window.blit(say_images["64_color.png"], (1000, 490))

            # for the number of packages
            elif 430 <= mouseX <= 480 and 510 <= mouseY <= 560:
                pygame.draw.rect(window, (150, 150, 150), (430, 510, 50, 50), 3)
            elif 540 <= mouseX <= 590 and 510 <= mouseY <= 560:
                pygame.draw.rect(window, (150, 150, 150), (540, 510, 50, 50), 3)
            elif 430 <= mouseX <= 480 and 575 <= mouseY <= 625:
                pygame.draw.rect(window, (150, 150, 150), (430, 575, 50, 50), 3)
            elif 540 <= mouseX <= 590 and 575 <= mouseY <= 625:
                pygame.draw.rect(window, (150, 150, 150), (540, 575, 50, 50), 3)

            # displays number of packages
            if number_packs == 1:
                pygame.draw.rect(window, (255, 255, 255), (430, 510, 50, 50), 3)
            elif number_packs == 2:
                pygame.draw.rect(window, (255, 255, 255), (540, 510, 50, 50), 3)
            elif number_packs == 3:
                pygame.draw.rect(window, (255, 255, 255), (430, 575, 50, 50), 3)
            elif number_packs == 4:
                pygame.draw.rect(window, (255, 255, 255), (540, 575, 50, 50), 3)

        # displays the restart button if all_options == False
        if not all_options:
            if not restart:
                window.blit(say_images["restart_off.png"], (650, 550))
            elif restart:
                window.blit(say_images["restart_on.png"], (650, 550))
            if not restart and 650 <= mouseX <= 775 and 550 <= mouseY <= 675:
                window.blit(say_images["restart_hover.png"], (650, 550))

        pygame.display.flip()


# ==============================================================================
if __name__ == '__main__':
    main()
