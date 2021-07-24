import pygame
from pygame.locals import *
import sys
import os
import time
from random import *
from options import *
from general_functions import *
from principal import *


def images(those_cards, type_cards):
    cards = {}

    for i in range(len(those_cards)):
        try:
            cards[those_cards[i]] = pygame.image.load(
                "images/" + type_cards + "/cards/" + those_cards[i]).convert_alpha()
        except:
            pass
    return (cards)


def golf(type_cards, game_size):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    # Definition of the rules
    rules = int(game_size / 4)
    # determine rows and columns using rules
def game_golf(rows, columns):
    game_golf(rules)

    windowX, windowY = 80 + (columns * 75) + ((columns - 1) * 45) + 80, 750
    window = pygame.display.set_mode((windowX, windowY))

    # Loading images
    background = pygame.image.load("images/background/background.png").convert()
    background = pygame.transform.scale(background, (windowX, windowY))
    select = pygame.image.load("images/select.png").convert_alpha()
    card_directory = ("images/" + type_cards + "/cards/")
    list_images = general_functions.random_game_generation(card_directory, rules, 1)
    say_cards = images(list_images, type_cards)

    # creation of a basic list, and mix of say_cards
    list_cards = [name for name in say_cards]
    shuffle(list_cards)
    table_cards = [list_cards[x:x + rows] for x in range(0, columns * rows, rows)]
    pick_cards = list_cards[columns * rows:]

    # the back of the say_cards (for the draw pile), empty card
    back = pygame.image.load("images/" + type_cards + "/back/back.png").convert_alpha()
    say_cards = add_empty_card(say_cards)
    pick_cards = "V00.png"

    mouseX, mouseY = (-1, -1)
    select_card = False
    coord_card = (-1, -1)
    pick = False
    myfont = pygame.font.SysFont("monospace", 20)
    allow_redo = False  # allows to limit the number of redo's the user has once
    redo = False  # if the user wants to go back with a movement
    last_move = ''  # take the values 'pick' or 'table' to indicate the last type of movement of the user
    game_rules = [rules, "start", "both+", "any", "hello", "golf"]  # to be used for the check_move function
    all_options = False

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                click_type, ind = check_mouse((mouseX, mouseY), table_cards, len(pick_cards), columns,
                                              (windowX, windowY))
                if click_type == "cards" and pick_cards != "V00.png":
                    coord_card = (mouseX - 80) // 120, len(table_cards[ind]) - 1
                    select_card = True
                    game_started = True
                    last_move = click_type
                elif click_type == "pick":
                    memory_pick = pick_card
                    pick_card = pick_cards.pop()
                    allow_redo = True
                    last_move = click_type
                elif selection == "menu":
                    principal.main()
                elif selection == "options":
                    type_cards, restart = options.options(window, type_cards, game_size, 1, all_options)
                    if restart:
                        golf(type_cards, game_size)
                    card_directory = "images/" + type_cards + "/cards/"
                    say_cards = images(list_images, type_cards)
                    say_cards = add_empty_card(say_cards)
                elif selection == "retour" and allow_redo:
                    start_time = pygame.time.get_ticks()
                    redo = True


            elif event.type == KEYDOWN:
                if event.key == K_p:
                    print(general_functions.order_values(rules, "start"))

        # poster background
        window.blit(back, (0, 0))

        # come back with a movement
        if redo:
            if last_move == 'cards':
                table_cards[memory_coord[0]].append(pick_cards)
                pick_cards = memory_pick
                redo = False
                allow_redo = False
            elif last_move == 'pick':
                pick_cards.append(pick_card)
                pick_card = memory_pick
                redo = False
                allow_redo = False

        # poster say_cards
        for x in range(columns):
            for y in range(rows):
                try:
                    window.blit(say_cards[table_cards[x][y]], (x * 120 + 80, y * 50 + 30))
                except:
                    break

        # pick poster
        for i in range(len(pick_cards)):
            window.blit(dos, (80 + i * 5, 400))

        # poster outline map (+1 for columns for the empty column at the start)
        if select_card:
            window.blit(select, (coord_card[0] * 120 + 80, coord_card[1] * 50 + 30))

        # show visible map
        window.blit(say_cards[pick_cards], (300, 400))

        # show buttons on the right
        selection = general_functions.side_bar(window, windowX, (mouseX, mouseY))

        pygame.display.flip()

        ## after the display flip so that the time.sleep is collectible
        if select_card:
            card_select = table_cards[coord_card[0]][coord_card[1]]
            if general_functions.check_move(card_select, pick_cards, game_rules):
                memory_pick = pick_card
                memory_coord = coord_card[0], coord_card[1]
                pick_card = table_cards[coord_card[0]][coord_card[1]]
                del (table_cards[coord_card[0]][coord_card[1]])
                allow_redo = True
            select_card = False
            time.sleep(0.2)

        check_end(table_cards, pick_card, pick_cards, game_rules)


def add_empty_card(say_cards):
    say_cards["V00.png"] = pygame.image.load("images/empty_card/V00.png").convert_alpha()
    return (say_cards)


def golf_size(rules):
    if rules == 13:
        columns = 7
        rows = 5
    elif rules == 7:
        columns = 6
        rows = 3
    elif rules == 8:
        columns = 6
        rows = 3
    elif rules == 14:
        columns = 6
        rows = 6
    elif rules == 16:
        columns = 7
        rows = 6
    else:
        columns = 7
        rows = 5

    return (rows, columns)


def check_mouse(mouse, table_cards, nb_pick, columns, screen_size):
    for i in range(columns):
        if len(table_cards[i]) > 0:
            if (i * 120) + 80 <= mouse[0] < (i * 120) + 80 + 75 and ((len(table_cards[i]) - 1) * 50) + 30 <= mouse[
                1] < ((len(table_cards[i]) - 1) * 50) + 30 + 118:
                return ("cards", i)

    if 80 <= mouse[0] < (nb_pick * 5) + 80 + 75 and 400 <= mouse[1] < 400 + 118:
        return ("pick", '')

    return ('', '')


def check_end(table_cards, pick_card, pick_cards, game_rules):
    # ENDGAME
    for i in range(len(table_cards)):
        if len(table_cards[i]) != 0:
            break
        if i == len(table_cards) - 1:
            end_game('win')

    if len(pick_cards) == 0:
        for i in range(len(table_cards)):
            test_coord = (i, -1)
            if len(table_cards[i]) != 0:
                if general_functions.check_move(table_cards[i][-1], pick_card, game_rules):
                    break
            if i == len(table_cards) - 1:
                end_game("loss")

def end_game(outcome):
    print(outcome)
    pygame.quit()
    sys.exit()


def main():
    golf('simpsons', 28)


# ==============================================================================
if __name__ == '__main__':
    main()