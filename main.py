"""
blakjak

Description:
"""
import json
import random


def pick_cards(deck, amount=1):
    picks = []
    for _ in range(amount):
        m = random.choice(deck)
        picks.append(m)
        deck.remove(m)
    return tuple(picks)


def get_value(cards):
    values = {
        "ace": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "jack": 10,
        "queen": 10,
        "king": 10
    }

    value = 0
    for i in cards:
        value += values[i.split("_")[1]]
    return value


def pretty_print(hand):
    suits = {
        "diamond": "Diamonds",
        "heart": "Hearts",
        "clubs": "Clubs",
        "spades": "Spades",
        "ace": "Ace",
        "two": "Two",
        "three": "Three",
        "four": "Four",
        "five": "Five",
        "six": "Six",
        "seven": "Seven",
        "eight": "Eight",
        "nine": "Nine",
        "ten": "Ten",
        "jack": "Jack",
        "queen": "Queen",
        "king": "King"
    }

    hand_str = ""
    for i in hand:
        # print(i)
        # print(hand)
        suit, value = i.split("_")
        hand_str += suits[value] + " of " + suits[suit] + ", "
    return hand_str[:-2]


def show_game(dealer_deck, player_deck):
    print("Dealer Hand")
    print(pretty_print(dealer_deck))
    print(get_value(dealer_deck))

    print("\nPlayer Hand")
    print(pretty_print(player_deck))
    print(get_value(player_deck))
    print()


default_deck = json.load(open('cards.json'))
deck = default_deck
dealer_deck = []
dealer_deck.extend(pick_cards(deck, 2))

player_deck = []
player_deck.extend(pick_cards(deck, 2))
# player_deck = ['heart_king', 'heart_queen', 'heart_ace']
print('blakjak')

lost = False
meowing = True
while meowing:
    show_game(dealer_deck, player_deck)

    choice = int(input('1 = hit\n2 = stand\n'))
    if choice == 1:
        try:
            player_deck.append(pick_cards(deck)[0])
        except IndexError:
            print('reshuffling deck')
            deck = default_deck
    else:
        meowing = False
    if get_value(player_deck) > 21:
        print('player bust')
        lost = True
        meowing = False

# dealer turn
if not lost:
    dealer_lost = False
    meowing = True
    while meowing:
        show_game(dealer_deck, player_deck)
        dealer_value = get_value(dealer_deck)
        player_value = get_value(player_deck)
        if dealer_value < player_value and dealer_value < 21:
            dealer_deck.append(pick_cards(deck)[0])
        if dealer_value > 21:
            meowing = False
            dealer_lost = True
        elif dealer_value > player_value:
            meowing = False
            dealer_lost = False
else:
    dealer_lost = True

show_game(dealer_deck, player_deck)

if lost == True or dealer_lost == False:
    print('\n\ndealer win')
elif lost == False or dealer_lost == True:
    print('\n\nplayer win')
