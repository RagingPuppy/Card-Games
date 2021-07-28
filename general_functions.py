import pygame
import pickle
from pygame . locals import *
import sys
import os
import time
from random import *

################################################# #########################################
################################################# #########################################
################################################# #########################################

def value_order(number_cards,place_as):
    # Automatically returns an order list of values, depending on the number of
    # cards in the rules. Works for number_cards = 7, 8, 13, 14 and 16:
    # 28-card deck (4 * 7): 7, 8, 9, 10, J, Q, K
    # Set of 32 cards (4 * 8): 1, 7, 8, 9, 10, J, Q, K
    # 52-card deck (4 * 13): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
    # Set of 56 cards (4 * 14): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, C, Q, K
    # Deck of 64 cards (4 * 16): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, J, C, Q, K
    # The place_as variable is used to define whether the 1 must be at the beginning or
    # at the end of the package.

    # Definition of the order of value of the cards according to their file number:
    # 15 and 16 correspond to 11 and 12, and 14 to the jumper.
    order_value_cards = [1,2,3,4,5,6,7,8,9,10,15,16,11,14,12,13]

    # Definition of the priority in which the cards will be taken according to the number
    # of cards requested in the game.
    order_priority_cards = [7,8,9,10,11,12,13,1,2,3,4,5,6,14,15,16]

    # Output variable
    order_according_to_rules = []

    # We only take the cards we need: if we play with 8 cards, we take
    # the first 8 values of order_priority_cards, i.e. the cards from 7 to 10,
    # Jack, Queen, King and Ace.
    card_priority_order = card_priority_order [0 : number_cards]

    # Sort the cards chosen in their order of value.
    # If we take 14 cards, this places the knight between the jack and the queen.
    for i in range(len(order_value_cards)):
        if order_value_cards[i] in order_value_cards :
            order_according_to_rules.append(order_value_cards[i])

    # Place of the ace in the game. By default it is before 2. If we want to place it after
    # the king, "place_as" must be equal to "end".
    if order_according_to_rules and place_as == "end":
        order_according_to_rules.insert(number_cards -1, rule_order.pop(0))

    # We return the order of the cards.
    return(order_according_to_rules)

################################################# #########################################
################################################# #########################################
################################################# #########################################

def check_move(departure_card,comparison_card,rules):
    # Returns True or False depending on whether the selected card can be placed on / after
    # the target card, according to the list of rules:
    # rules = [number_cards, place_as, correspond_number, correspond_color, first_card]

    # number_cards: number of cards in the deck.
    # Takes the values 7, 8, 13, 14 or 16.

    # place_as: place of the ace, before 2 or after K.
    # Takes the values: "start" or "end".

    # correspond_number: checks if the difference that must have the card_departure
    # with the card_compare. If we want to place a 6 on a 7, the compare_card
    # is therefore less than the card_departure, we use "inf".
    # Takes the values: "inf", "sup", "same" or "both".

    # correspond_color: checks the color that the map_compare can take
    # for her to check the rules of the game.
    # Takes the values: "same_symbol", "same_color", "diff_color" or "any".

    # first_card: checks which card can be placed on an empty slot.
    # Takes the values: "king" or "ace".

    # By default, everything is considered to be false so as not to validate the movement.
    valid_number = False
    valid_color = False
    valid = False

    # Get the order of the cards with the order_values function.
    order_according_to_rules = order_values(rules[0],rules[1])

    # We place a "0" in order_according_to_rules to define which card is placed on
    # an empty slot.
    if rules[4] == "king":
        order_according_to_rules.append(0)
    elif rules[4] == "ace":
        order_according_to_rules.insert(0,0)

    # Retrieval of the symbol (C,D,H,S) and the number of the starting card.
    departure_card_type = departure_card[0]
    starting_card_num = int(starting_card[1:3])

    # Retrieval of the symbol (C,D,H,S) and the number of the compared card.
    comparison_card_type = comparison_card[0]
    comparison_card_num = int(comparison_card[1:3])

    # Subtract the numbers of the compared to the starting card.
    try:
        compare = order_according_to_rules.index(starting_card_num) - order_according_to_rules.index(card_num_compare)
    except ValueError:
        compare = -100

    # Definition of lists corresponding to the possibilities of differences between the cards.
    correspond_number = {"inf": [-1], "sup": [1], "same" : [0], "both" : [-1,1], "both +": [-1,1,rules[0]-1,-(rules[0]-1)]}

    # Creation of red and black variables to check if a card is red
    # (diamond or heart) or black (clubs or spades).
    red = ["D", "H"]
    black = ["C", "S"]

    # Creation of color1 variables corresponding to the same color as the starting card,
    # and color2 corresponding to the opposite color.
    if starting_card_type in red:
        color1 = red
        color2 = black
    else:
        color1 = black
        color2 = red

    # Definition of lists corresponding to the color possibilities of the compared_card.
    correspond_color = {"same_symbol" : [type_card_departure], "same_color" : color1, "diff_color" : color2, "any" : ["C","D","H","S"]}

    # Checking the validity of the number.
    if compare in correspond_number[rules[2]]:
        valid_number = True

    # Checking the validity of the color.
    if type_compare_card in correspond_color[rules[3]] or type_compare_card == "V":
        valid_color = True

    # Checking the validity of the trip.
    if valid_number == True and valid_color == True:
        valid = True

    # for the napoleon if there are >= 2 empty side by side
    if compare_card == "V00.png" and num_card_departure != order_according_to_rules [0] and rules[5] == "napoleon":
        valid = True

    if num_card_departure == order_according_to_rules[0] and rules[4] == 0:
        valid = True


    # Return of the validity of the move: True or False.
    return (valid)

################################################# #########################################
################################################# #########################################
################################################# #########################################

def random_game_generation(card_directory, number_cards,number_packs):
    # Return a random deck based on the number of cards in the deck
    # and the number of packages.

    # Retrieving the names of the image files in the corresponding directory
    raw_image_list = os.listdir(card_directory)

    # Output variable
    list_images_rules=[]

    # Loading cards i times, depending on the number of packs used
    for i in range (number_packets):

        # Register j cards, depending on the number of in a pack
        for i in range (len(raw_image_list)):

            # We take from character [1] to character [2] to get the card number
            cardnumber=raw_image_list[j][1:3]

            # We retrieve the list of cards used (we do not take the jumper
            # when we have 13 cards, for example)
            list_cards=order_values(number_cards,"end")

            # We add the only if it is in the list. The try
            # allows not to take the temp files
            try:
                if int(cardnumber)in card_list:
                    list_images_rules.append(raw_image_list[j])

            except:
                pass

    # We shuffle the list to generate a random game
    shuffle(list_images_rules)

    # Return of the list
    return (rule_image_list)

################################################# #########################################
################################################# #########################################
################################################# #########################################

def images (card_directory):
    # Return a dictionary of images based on card names.

    # Retrieving cards and placing in a list
    raw_image_list=os.listdir(card_directory)

    # Definition of the output variable
    say_images ={}

    # We place the pygame load in front of each "X ##. Png" image. The try allows to
    # ignore temp files.
    for i in range(len(raw_image_list)):
        try:
            say_images[raw_image_list[i]]=pygame.image.load(card_directory+raw_image_list[i]).convert_alpha()
        except:
            pass

    # Return of the output dictionary
    return (say_images)

################################################# #########################################
################################################# #########################################
################################################# #########################################

def sidebar(window, windowX, mouse_coord):
    say_images_bar=images("images/options/")
    selection=""

    window.blit(say_images_bar["menu_off.png"],(windowX-50,50))
    window.blit(say_images_bar["options_off.png"], (windowX-50,100))
    window.blit(say_images_bar["retour_off.png"],(windowX-50,150))

    if windowX - 50 < mouse_coord[0] < windowX - 20 and 50 < mouse_coord[1] < 80:
        window.blit(say_images_bar["menu_on.png"], (windowX - 50, 50))
        selection = "menu"
    if windowX - 50 < mouse_coord[0] < windowX - 20 and 100 < mouse_coord[1] < 130:
        window.blit(say_images_bar["options_on.png"], (windowX - 50, 100))
        selection = "options"
    if windowX - 50 < mouse_coord[0] < windowX - 20 and 150 < mouse_coord[1] < 180:
        window.blit(say_images_bar["retour_on.png"], (windowX - 50, 150))
        selection = "return"

    return (selection)

################################################# #########################################
################################################# #########################################
################################################# #########################################