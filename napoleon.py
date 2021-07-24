import pygame
from pygame.locals import *
import sys
import os
import time
from random import *
from options import *
from general_functions import *
import principal


def images(those_cards, type_cards):
    cards = {}

    for i in range(len(those_cards)):
        try:
            cards[those_cards[i]] = pygame.image.load(
                "images/" + type_cards + "/cards/" + those_cards[i]).convert_alpha()
        except:
            pass
    return (cards)


def napoleon(type_cards, game_size):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    # Definition of rules
    rules = int(game_size / 4)

    windowX, windowY = (200 + (rules + 1) * 80, 750)
    window = pygame.display.set_mode((windowX, windowY))

    # Loading images
    back = pygame.image.load("images/back/back.png")
    back = pygame.transform.scale(back, (windowX, windowY))
    card_directory = ("images/" + type_cards + "/cards/")
    list_images = general_functions.random_game_generation(card_directory, rules, 1)
    number_cards = len(list_images)
    say_cards = images(list_images, type_cards)

    rows = 4
    columns = int(number_cards / rows)

    # creation of a basic list, and mix of say_cards
    list_cards = [name for name in say_cards]  # take each name of say_cards in the library

    # addition of empty say_cards at the end of the lists.
    say_cards = add_empty_card(say_cards)
    for i in range(rows):
        list_cards.append("V00.png")

    shuffle(list_cards)
    shuffled = [list_cards[x:x + columns + 1] for x in range(0, len(list_cards),
                                                             columns + 1)]  # creates a two-dimensional list (rows * columns) with the values of list_cards as value

    # select transparency
    select1 = pygame.image.load("images/select.png").convert_alpha()
    select2 = pygame.image.load("images/select2.png").convert_alpha()

    mouseX, mouseY = (-1, -1)
    select_depart = False  # variable if the departure card has been selected
    coord_depart = (-1, -1)
    select_dest = False  # variable if the destination card has been selected
    coord_dest = (-1, -1)
    myfont = pygame.font.SysFont("monospace", 20)
    game_started = False  # becomes true when the user starts playing! (used for options)
    allow_redo = False  # allows to limit the number of 'redo's the user has once
    redo = False  # if the user wants to go back one movement
    game_rules = [rules, "start", "sup", "same_symbol", "ace on empty", "napoleon"]
    all_options = False

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                # convert raw coordinates to array coordinates
                tableX, tableY = (mouseX - 30) // 80, (mouseY - 30) // 118
                if select_depart == False and 0 <= tableX < columns + 1 and 0 <= tableY < rows and \
                        shuffled[tableY][tableX] != "V00.png":  # for the departure card
                    coord_depart = tableauX, tableauY
                    select_depart = True
                # if the user clicks on a card instead of empty as a second choice
                elif select_dest == False and 0 <= tableX < columns + 1 and 0 <= tableY < rows and \
                        shuffled[tableY][tableX] != "V00.png":
                    coord_depart = tableX, tableY
                    select_depart = True
                elif select_dest == False and 0 <= tableX < columns + 1 and 0 <= tableY < rows and \
                        shuffled[tableY][tableX] == "V00.png":  # for the destination position
                    coord_dest = tableX, tableY
                    select_dest = True
                elif selection == "menu":
                    principal.main()
                elif selection == "options":
                    type_cards, restart = options.options(window, type_cards, game_size, 1, all_options)
                    if restart:
                        napoleon(type_cards, game_size)
                    card_directory = "images/" + type_cards + "/cards/"
                    say_cards = images(list_images, type_cards)
                    say_cards = add_empty_cards(say_cards)
                elif selection == "retour" and allow_redo:
                    redo = True

            elif event.type == KEYDOWN:
                if event.key == K_o:
                    shuffled = cheat_ordered(shuffled, rows, columns)
                    time.sleep(0.2)

        # poster background
        window.blit(back, (0, 0))

        # go back in a movement
        if redo:
            shuffled[memory_depart[1]][memory_depart[0]] = shuffled[memory_dest[1]][memory_dest[0]]
            shuffled[memory_dest[1]][memory_dest[0]] = "V00.png"
            redo = False
            allow_redo = False

        ## poster say_cards
        for y in range(rows):
            for x in range(columns + 1):  # + 1 to add the empty card at the end of each line
                window.blit(say_cards[shuffled[y][x]], (x * 80 + 30, y * 118 + 30))

        # departure card outline poster
        if select_depart:
            window.blit(select1, (coord_depart[0] * 80 + 30, coord_depart[1] * 118 + 30))  # select transparency

        ## destination location outline poster
        if select_dest:
            window.blit(select2, (coord_dest[0] * 80 + 30, coord_dest[1] * 118 + 30))  # select transparency

        # show buttons on the right
        selection = general_functions.lateral_bar(window, windowX, (mouseX, mouseY))

        pygame.display.flip()

        if select_dest:
            card_depart = shuffled[coord_depart[1]][coord_depart[0]]
            card_compare = shuffled[coord_dest[1]][coord_dest[0] - 1]
            game_rules[4] = coord_dest[0]
            if general_functions.check_move(card_depart, card_compare, game_rules):
                memory_card = shuffled[coord_depart[1]][coord_depart[0]]
                memory_depart = coord_depart
                memory_dest = coord_dest
                shuffled[coord_dest[1]][coord_dest[0]] = shuffled[coord_depart[1]][coord_depart[0]]
                shuffled[coord_depart[1]][coord_depart[0]] = "V00.png"
                game_started = True  # the game has started
                allow_redo = True
            select_depart, select_dest = False, False
            time.sleep(0.2)  # so that there is a small pause so that we can clearly see the colors of the outlines

        check_end(shuffled, rows, columns, rules)


def cheat_ordered(shuffled, rows, columns):
    ordered = [[], [], [], []]
    empty_index = 0
    for y in range(rows):
        for x in range(columns + 1):
            if shuffled[y][x][0] == "C":
                ordered[0].append(shuffled[y][x])
            elif shuffled[y][x][0] == "D":
                ordered[1].append(shuffled[y][x])
            elif shuffled[y][x][0] == "H":
                ordered[2].append(shuffled[y][x])
            elif shuffled[y][x][0] == "S":
                ordered[3].append(shuffled[y][x])
            elif shuffled[y][x][0] == "V":
                ordered[empty_index].append(shuffled[y][x])
                empty_index += 1

    ordered[0].sort()
    ordered[1].sort()
    ordered[2].sort()
    ordered[3].sort()

    return (ordered)


def add_empty_card(say_cards):
    say_cards["V00.png"] = pygame.image.load("images/empty_card/V00.png").convert_alpha()
    return (say_cards)


def check_end(shuffled, rows, columns, rules):  # TO CHECK

    # if the game is lost
    dead_end = 0
    for y in range(rows):
        for x in range(columns + 1):
            if shuffled[y][x] == "V00.png":
                if int(shuffled[y][x - 1][1:3]) == 13:
                    dead_end += 1
                elif shuffled[y][x - 1] == "V00.png":
                    dead_end += 1
    if dead_end == 4:
        end_game("loss")

    # if the game is won
    temp = 0
    break_loop = False
    num1 = 0
    num2 = 0
    type1 = ""
    type2 = ""

    order = general_functions.order_values(rules, "start")

    for y in range(rows):
        for x in range(columns - 1):  # -1 to be able to compare one by one
            # the try except allow to eliminate the error or it looks at the empty boxes (because num_cases empty = 0 and 0 not in order)
            try:
                num1 = order.index(int(shuffled[y][x][1:3]))
            except ValueError:
                num1 = -1
            try:
                num2 = order.index(int(shuffled[y][x + 1][1:3]))
            except ValueError:
                num2 = -1
            type1 = shuffled[y][x][0]
            type2 = shuffled[y][x + 1][0]
            if not (type1 == type2 and (num1 + 1) == num2):
                return
    end_game("win")


def end_game(outcome):
    print(outcome)
    pygame.quit()
    sys.exit()


def main():
    napoleon('simpsons', 52)


# ==============================================================================
if __name__ == '__napoleon__':
    napoleon()
