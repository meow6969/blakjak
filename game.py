import random
import json
import neat


def pick_cards(deck, amount=1):
    picks = []
    for _ in range(amount):
        m = random.choice(deck)
        picks.append(m)
        deck.remove(m)
    return tuple(picks)


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


def show_game(dealer_deck, player_deck):
    print("\nDealer Hand")
    print(pretty_print(dealer_deck))
    print(f"{get_value(dealer_deck)} ({get_value([dealer_deck[0]])})")

    print("\nPlayer Hand")
    print(pretty_print(player_deck))
    print(get_value(player_deck))
    print()


class blakjak:
    def __init__(self):
        self.default_deck = json.load(open('cards.json'))
        # print(self.default_deck)
        self.deck = self.default_deck
        # print(self.default_deck)
        self.dealer_deck = []
        self.dealer_deck.extend(pick_cards(self.deck, 2))

        self.player_deck = []
        self.player_deck.extend(pick_cards(self.deck, 2))
        self.player_lost = False
        self.dealer_lost = False
        self.player_done = False
        self.dealer_done = False

        self.pick_cards = pick_cards
        self.get_value = get_value
        self.show_game = show_game
        self.draw = False

    def player_turn(self, choice):
        # lost = False
        # meowing = True
        # print('player turn')

        # show_game(self.dealer_deck, self.player_deck)

        # choice = int(input('1 = hit\n2 = stand\n'))
        # print('player')
        if choice == 1:
            try:
                self.player_deck.append(pick_cards(self.deck)[0])
            except IndexError:
                # print('reshuffling deck')
                # print(self.default_deck)
                # self.deck = self.default_deck
                # print(self.default_deck)
                self.deck = json.load(open('cards.json'))
                self.player_deck.append(pick_cards(self.deck)[0])
        else:
            self.player_done = True
        if get_value(self.player_deck) > 21:
            # print('player bust')
            self.player_lost = True
            self.player_done = True
        return

    def test_ai(self, winner, config):
        net = neat.nn.FeedForwardNetwork.create(winner, config)
        counts = 0
        meowing = True
        while meowing:
            # time.sleep(.5)
            # making decision
            if not self.player_done:
                # player_cards = self.cards2int(self.game.player_deck)
                # dealer_cards = self.cards2int(self.game.player_deck)
                # output = net.activate((player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                #                        player_cards[4], player_cards[5], player_cards[6], player_cards[7],
                #                        player_cards[8], player_cards[9], player_cards[10],
                #                        dealer_cards[0], dealer_cards[1], dealer_cards[2], dealer_cards[3],
                #                        dealer_cards[4], dealer_cards[5], dealer_cards[6], dealer_cards[7],
                #                        dealer_cards[8], dealer_cards[9], dealer_cards[10]))
                output = net.activate((
                    self.get_value(self.player_deck),
                    self.get_value(self.dealer_deck)
                ))

                # turning decision into list of integers
                decision = output.index(max(output))
                # print(decision)

            # looping the game
            if not self.player_done:
                game_info = self.player_turn(decision)
            else:
                game_info = self.dealer_turn()

            # checking if the snake is dead
            counts += 1
            if self.player_done and self.dealer_done or self.player_lost:
                # print('game ended')
                # self.calculate_fitness(genome, self.game.player_lost, False)
                if self.player_lost:
                    print(f'ai lost')
                else:
                    print('ai won')
                break
            if self.draw:
                # print('game ended')
                # self.calculate_fitness(genome, self.game.player_lost, True)
                print('ai tied')
                break
        # self.calculate_fitness(genome, self.game.player_lost)

