import game
import neat
import pickle
import random
import json
import time


class blackjack:
    def __init__(self):
        self.cards2int = json.load(open('cards2int.json'))
        self.game = game.blakjak()

    def cards_to_index(self, cards):
        int_cards = []
        for i in cards:
            int_cards.append(self.cards2int[i])
        while len(int_cards) < 11:
            # card 0 means no card
            int_cards.append(0)
        return int_cards

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        meowing = True
        while meowing:
            # time.sleep(.5)
            # making decision
            player_cards = self.cards_to_index(self.game.player_deck)
            dealer_cards = self.cards_to_index(self.game.player_deck)
            output = net.activate((player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                   player_cards[4], player_cards[5], player_cards[6], player_cards[7],
                                   player_cards[8], player_cards[9], player_cards[10],
                                   dealer_cards[0]))
            # output = net.activate((
            #     self.game.get_value(self.game.player_deck),
            #     self.game.get_value([self.game.dealer_deck[0]])
            # ))
            # print(self.game.dealer_deck)
            # print(self.game.get_value([self.game.dealer_deck[0]]))

            # turning decision into list of integers
            decision = output.index(max(output))
            # print(decision)

            # looping the game
            game_info = self.game.player_turn(decision)

            # print(self.game.show_game(self.game.dealer_deck, self.game.player_deck))
            # if decision == 0:
            #     print('stand')
            # else:
            #     print('hit')
            # input()

            # checking if the game is over
            if self.game.player_done:
                meowing = False
        return self.game.player_lost

    def calculate_fitness(self, genome, state):
        # print(counts)
        # genome.fitness += int(game_info.score*20 - (counts/(game_info.score + 1)))
        if state == 'draw':
            genome.fitness += .5
        elif state == 'player_win':
            genome.fitness += 1
        else:
            # print('lost')
            genome.fitness -= 1
        # print(genome.fitness)

    def dealer_turn(self, verbose=False):
        # print('dealer turn')
        # show_game(self.dealer_deck, self.player_deck)
        meowing = True
        while meowing:
            dealer_value = self.game.get_value(self.game.dealer_deck)
            player_value = self.game.get_value(self.game.player_deck)
            # print(player_value)
            # print(dealer_value)
            # print('dealer')
            if verbose:
                self.game.show_game(self.game.dealer_deck, self.game.player_deck)
                input()
            if dealer_value <= player_value and dealer_value < 16:
                try:
                    self.game.dealer_deck.append(self.game.pick_cards(self.game.deck)[0])
                except IndexError:
                    # print('reshuffling deck')
                    self.game.deck = self.game.default_deck
                    self.game.dealer_deck.append(self.game.pick_cards(self.game.deck)[0])
            else:
                meowing = False

        # calculate who won
        dealer_value = self.game.get_value(self.game.dealer_deck)
        player_value = self.game.get_value(self.game.player_deck)

        if dealer_value == player_value:
            self.game.draw = True
        if dealer_value > 21:
            self.game.dealer_lost = True
            self.game.dealer_done = True
            self.game.player_lost = False
        elif dealer_value > player_value:
            self.game.dealer_lost = False
            self.game.player_lost = True
            self.game.dealer_done = True

    def test_ai(self, net):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
        # ai turn
        print("\nAI turn\n")
        meowing = True
        while meowing:
            player_cards = self.cards_to_index(self.game.player_deck)
            dealer_cards = self.cards_to_index(self.game.player_deck)
            output = net.activate((player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                   player_cards[4], player_cards[5], player_cards[6], player_cards[7],
                                   player_cards[8], player_cards[9], player_cards[10],
                                   dealer_cards[0]))
            # output = net.activate((
            #     self.game.get_value(self.game.player_deck),
            #     self.game.get_value([self.game.dealer_deck[0]])
            # ))
            choice = output.index(max(output))
            self.game.show_game(self.game.dealer_deck, self.game.player_deck)
            if choice == 0:
                print('stand')
            else:
                print('hit')
            input()
            self.game.player_turn(choice)

            if self.game.player_done:
                meowing = False
        print('\ndealer turn\n')
        # dealer turn
        if not self.game.player_lost:
            self.dealer_turn(verbose=True)
        if self.game.draw:
            self.game.show_game(self.game.dealer_deck, self.game.player_deck)
            print('\n\nits a draw')
        if not self.game.player_lost:
            self.game.show_game(self.game.dealer_deck, self.game.player_deck)
            print('\n\nplayer won')
        else:
            self.game.show_game(self.game.dealer_deck, self.game.player_deck)
            print('\n\ndealer won')


def eval_genomes(genomes, config):
    # window = pygame.display.set_mode([width, height])
    # print(genomes)
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0.0
        bj_game = blackjack()
        for m in range(50):
            player_lost = bj_game.train_ai(genome, config)
            if not player_lost:
                bj_game.dealer_turn()

            if bj_game.game.draw:
                bj_game.calculate_fitness(genome, 'draw')
            if not player_lost:
                bj_game.calculate_fitness(genome, 'player_win')
            else:
                bj_game.calculate_fitness(genome, 'dealer_win')


def run_neat(config):
    # to load checkpoint:
    # comment out the p = neat.Populaition(Config) line
    # replace it with p = neat.Checkpointer.restore_checkpoint('neat checkpoint filename')

    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-954')

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(500))

    winner = p.run(eval_genomes, 10000)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = blackjack()
    game.test_ai(winner_net)


if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 'neat.config.Config')
    # run_neat(config)
    test_ai(config)
