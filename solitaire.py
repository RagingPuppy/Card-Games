import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from options import *
from random import *
from general_functions import *
from principal import *


############################################################################################
############################################################################################
############################################################################################

def random_ground_game(those_cards, number_packs):
    # Create the game board, based on the random cards
    # and the number of packages.
    number_packs = len(those_cards)

    i = 0
    j = 0

    card = []
    line = []
    game = []  # Output variable

    # BOARD
    # We start by creating the n columns of the main table.
    # The first will have 1 card, the second will have 2, etc. We stop
    # when the sum is greater than half of the total number
    # Cards.
    while j < int(len(those_cards) / 2):
        for k in range(j, j + i):
            card.append(those_cards[k])
            card.append(0)
            line.append(card)
            card = []
        card.append(those_cards[j + i])
        card.append(1)
        line.append(card)
        game.append(line)
        i = i + 1
        j = j + i
        card = []
        line = []

    # ARRIVAL
    # We then add the locations of the arrival, corresponding
    # to 4 times the number of packages.
    for i in range(number_packs * 4):
        game.append([])

    # PICK
    # Finally, we place the rest of the cards in the draw pile, and we
    # adds a last list corresponding to the overturned pick.
    while j < int(len(those_cards)):
        card.append(those_cards[j])
        card.append(1)
        line.append(card)
        card = []
        j = j + 1
    game.append(line)
    game.append([])

    return (game)


############################################################################################
############################################################################################
############################################################################################

def window_size(game):
    # Set window size based on location
    # of the last column of the game board.
    for i in range(len(game) - 2):
        for j in range(len(game[i])):
            # We only look for columns where at least
            # a card is turned over at the start of the game.
            if game[i][j][1] == 0:
                pass
            else:
                last_column = i * 85 + 400

    return (last_column)


############################################################################################
############################################################################################
############################################################################################

def cardclick(mouse_coord, game, last_column, number_packs):
    # Returns the selected map, its position in pixels, its
    # position in game, and whether we can flip it or not.

    card_select = ""
    pos = []
    cardplace = []
    both_sides = 0

    # Select a card from the table
    for i in range(int((last_column - 400) / 85) + 1):
        # Select column
        if i * 85 + 400 < mouse_coord[0] < i * 85 + 475:
            # Select the card on the column
            for j in range(len(game[i])):
                if j * 25 + 213 < mouse_coord[1] < j * 25 + 326 and game[i][j][1] == 1:
                    card_select = game[i][j][0]
                    cardplace = [i, j, 0]
                    pos = [i * 85 + 400, j * 25 + 213]
                if game[i][-1][1] == 0:
                    both_sides = 1
                    cardplace = [i, j, 0]
            # If there is no card in the column, then we return
            # an empty card.
            if len(game[i]) == 0:
                card_select = "V00.png"
                cardplace = [i, 0, 0]

    # Selecting a card from the draw pile
    if 135 < mouse_coord[0] < 210 and 50 < mouse_coord[1] < 163:
        cardplace = [len(game) - 1, len(game[-1]) - 1, 0]
        card_select = game[-1][-1][0]
        pos = [135, 50]

    # Selection of an arrival card
    if 50 < mouse_coord[1] < 163:
        for i in range(number_packs * 4):
            if last_column - i * 85 < mouse_coord[0] < last_column + 75 - i * 85:
                cardplace = [len(game) - 3 - i, len(game[-3 - i]) - 1, 0]
                try:
                    card_select = game[-3 - i][-1][0]
                except:
                    pass
                if card_select == "":
                    card_select = "V00.png"
                else:
                    pass
                pos = [last_column - i * 85, 50]

    return (card_select, pos, cardplace, both_sides)


############################################################################################
############################################################################################
############################################################################################

def record_list(lists):
    # Used to save the game board from the previous round.

    prov1 = []
    prov2 = []
    prov3 = []

    for i in range(len(lists)):
        for j in range(len(lists[i])):
            for k in range(len(lists[i][j])):
                prov3.append(lists[i][j][k])
            prov2.append(prov3)
            prov3 = []
        prov1.append(prov2)
        prov2 = []

    return (prov1)


############################################################################################
############################################################################################
############################################################################################

def blitimages(window, game, number_packs, last_column, type_cards, type_back):
    back = pygame.image.load("images/classic/back/" + type_back + ".png")
    empty = pygame.image.load("images/empty_card/V00.png")
    say_images = images("images/" + type_cards + "/cards/")

    # Display of game cards
    # Display of board cards
    for i in range(len(game) - (2 + number_packs * 4)):

        # Display of an empty card if there is no more card
        if game[i] == []:
            window.blit(empty, (i * 85 + 400, 213))

        for j in range(len(game[i])):
            # Display of the back of the cards if they are back
            if game[i][j][1] == 0:
                window.blit(back, (i * 85 + 400, j * 25 + 213))

            # Display of the map if they are front side
            else:
                window.blit(say_images[game[i][j][0]], (i * 85 + 400, j * 25 + 213))

                # Display of arrival cards
                # Display of empty cards
    for i in range(number_packs * 4):
        window.blit(empty, (last_column - (85 * i), 50))

    # Display of row cards
    for i in range(number_packs * 4):
        for j in range(len(game[-3 - i])):
            window.blit(say_images[game[-3 - i][j][0]], (last_column - i * 85, 50))

    # We display the last card of the pile turned upside down
    try:
        window.blit(say_images[game[-1][-1][0]], (135, 50))

    # Otherwise we display an empty card
    except:
        window.blit(empty, (135, 50))

    # Display an empty card if there are no more cards in the deck
    if game[-2] == []:
        window.blit(empty, (50, 50))
    else:
        window.blit(dos, (50, 50))


############################################################################################
############################################################################################
############################################################################################

def solitaire(type_cards, game_size, number_packs):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    # Loading images
    back = pygame.image.load("images/back/back.png")
    image_select1 = pygame.image.load("images/select.png")
    image_select2 = pygame.image.load("images/select2.png")
    image_select_top = pygame.image.load("images/select_top.png")

    # Definition of the game
    number_cards = int(game_size / 4)

    # Stacking rules in the table
    game_rules = [number_cards, "start", "inf", "diff_color", "king", "solitaire"]

    # Stacking rules in the finish
    stack_rules = [number_cards, "start", "sup", "same_symbol", "ace", "solitaire"]

    # Default card directory
    type_cards = "classic"
    type_back = "back6"

    # Generating a random game
    those_cards = random_game_generation("images/" + type_cards + "/cards/", number_cards, number_packs)

    # Generation of the game board
    game = random_ground_game(those_cards, number_packs)

    # Creation of the image dictionary
    say_images = images("images/" + type_cards + "/cards/")

    # Creation of the game window
    last_column = window_size(game)
    windowX, windowY = last_column + 150, 750
    window = pygame.display.set_mode((windowX, windowY))
    back = pygame.transform.scale(back, (windowX, windowY))
    window.blit(back, (0, 0))

    # Creation of game variables
    card_select1 = ""  # Card selection
    card_select2 = ""  # Comparison map
    both_sides = 0  # Defines whether a card can be returned or not
    to_move = []  # Defines the set of cards to be moved
    cardplace1 = []  # Defines the location in game of map 1
    cardplace2 = []  # Defines the location in game of map 2
    selection = ""  # Set the icon selected in the sidebar
    save = []  # Record of the game board in the previous round

    # Game loop
    while True:
        for event in pygame.event.get():

            # Get mouse coordinates
            mouse_coord = pygame.mouse.get_pos()

            # Bottom display
            window.blit(back, (0, 0))

            # Display of the game board
            blitimages(window, game, number_packs, last_column, type_cards, type_back)

            # Closing event
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Sidebar display
            selection = lateral_bar(window, windowX, mouse_coord)

            # Refreshing the sidebar
            if event.type == MOUSEMOTION:
                mouse_coord = pygame.mouse.get_pos()
                selection = lateral_bar(window, windowX, mouse_coord)

            # Click management
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if selection == "menu":
                    principal.main()
                if selection == "options":
                    type_cards, restart = options.options(window, type_cards, number_cards * 4, number_packs,
                                                           False)
                    if restart == True:
                        solitaire()
                if selection == "retour":
                    if not save == []:
                        game = record_list(save)
                        save = []

                # Click in the inverted draw pile
                if 50 < mouse_coord[0] < 125 and 50 < mouse_coord[1] < 163:
                    save = record_list(game)

                    # Package management
                    # Removed a card from the hidden draw pile and added another to the displayed draw pile
                    try:
                        game[-1].append(game[-2][-1])
                        game[-2].pop()

                    # Otherwise there are no more cards in the hidden draw pile, the displayed draw pile becomes hidden draw pile.
                    except:
                        game[-1].reverse()
                        game[-2] = game[-1]
                        game[-1] = []

                    card_select1 = ""
                    pos1 = []
                    cardplace1 = []

                ## If no card is selected
                if card_select1 == "":

                    ## Then we can select a card
                    try:
                        card_select1, pos1, cardplace1, both_sides = cardclick(mouse_coord, game, last_column,
                                                                               number_packs)
                        ## We return the card if possible
                        if both_sides == 1:
                            game[cardplace1[0]][cardplace1[1]][1] = 1
                            card_select1 = ""
                            pos1 = []
                            cardplace1 = []

                    except:
                        card_select1 = ""
                        pos1 = []
                        cardplace1 = []

                ## If a card is already selected
                else:
                    valid = False

                    ## We select a second card
                    card_select2, pos2, cardplace2, both_sides = cardclick(mouse_coord, game, last_column,
                                                                           number_packs)

                    ## We return the card if possible
                    if both_sides == 1:
                        try:
                            game[cardplace2[0]][cardplace2[1]][1] = 1
                        except:
                            pass

                    try:
                        if len(game) - 3 - number_packs * 4 < cardplace2[0] < len(game) - 2:
                            valid = check_move(card_select1, card_select2, stack_rules)
                        else:
                            valid = check_move(card_select1, card_select2, game_rules)
                    except:
                        pass

                    ## Deselect the card if you click on it again
                    if card_select1 == card_select2:
                        card_select1 = ""
                        card_select2 = ""
                        pos1 = []
                        pos2 = []
                        cardplace1 = []
                        cardplace2 = []

            ## Right click management
            if event.type == MOUSEBUTTONDOWN and event.button == 3:

                ## Select a card
                try:
                    card_select1, pos1, cardplace1, both_sides = cardclick(mouse_coord, game, last_column,
                                                                           number_packs)
                except:
                    card_select1 = ""
                    pos1 = []
                    cardplace1 = []

                ## Checking if a location is available on arrival
                for i in range(number_packs * 4):
                    try:
                        card_select2 = game[len(game) - 2 - number_packs * 4 + i][-1][0]
                    except:
                        card_select2 = "V00.png"
                    cardplace2 = [len(game) - 2 - number_packs * 4 + i, -1, 0]
                    pos2 = []
                    try:
                        valid = check_move(card_select1, card_select2, stack_rules)
                    except:
                        pass
                    if valid == True:
                        break

            ## Checking the validity of the movement
            if not card_select1 == "" and not card_select2 == "":

                if valid == True and cardplace2[0] < len(game) - 2:
                    save = record_list(game)
                    to_move = game[cardplace1[0]][cardplace1[1]:]
                    to_move.reverse()
                    for i in range(len(tomove)):
                        game[cardplace2[0]].append(to_move[-1])
                        to_move.pop()
                        game[cardplace1[0]].pop()
                    card_select1 = ""
                    cardplace1 = []
                    pos1 = []
                    valid = False

                ## Otherwise, the second card becomes the selected card
                else:
                    card_select1 = card_select2
                    pos1 = pos2
                    cardplace1 = cardplace2

                card_select2 = ""
                pos2 = []
                cardplace2 = []

            ## If the selected card is an empty card (in the finish line), then nothing is selected
            if card_select1 == "V00.png":
                card_select1 = ""
                pos1 = []
                cardplace1 = []

            ## Display of selection contours
            try:
                if cardplace1[1] == len(game[cardplace1[0]]) - 1 or cardplace[0] == len(game) - 2:
                    window.blit(image_select1, (pos1[0], pos1[1]))
            except:
                pass
            try:
                if not cardplace1[1] == len(game[cardplace1[0]]) - 1 or cardplace[0] == len(game) - 2:
                    window.blit(image_select_top, (pos1[0], pos1[1]))
                window.blit(image_select2, (pos2[0], pos2[1]))
            except:
                pass

            ## Checking the end of the game
            try:
                win = 1
                for i in range(number_packs * 4):
                    if not int(game[len(game) - 2 - number_packs * 4 + i][-1][0][1:3]) == 13:
                        win = 0
                if win == 1:
                    print("You Win !")
            except:
                pass

            pygame.display.flip()