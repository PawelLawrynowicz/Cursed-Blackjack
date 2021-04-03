from deck import Deck
from player import Player
from table import Window
import time
import curses


class Blackjack:
    def __init__(self, stdscr):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player(False, 0, self.deck)
        self.dealer = Player(True, 0, self.deck)
        self.window = Window(stdscr, 0, 0, self.deck)

    def deal_round(self):
        for i in range(2):
            self.player.deal()
            # time.sleep(0.5)
            self.dealer.deal()
        # time.sleep(0.5)
        print("Your hand is: ")
        self.player.display()
        print("\nDealer's hand is: ")
        self.dealer.display()

    def check_for_blackjack(self):
        player_BJ = False
        dealer_BJ = False
        if self.player.get_score() == 21:
            player_has_blackjack = True
        if self.dealer.get_score() == 21:
            dealer_has_blackjack = True
        return player_BJ, dealer_BJ

    # Main game loop

    def play(self):
        game_over = False

        self.phase_zero()

        while not game_over:
            self.window.refresh()
            self.phase_one()
            self.phase_two()

    def phase_zero(self):
        self.window.paint_prompt(0)
        self.player.money = self.window.get_input()
        self.window.draw_info(self.player.money)
        self.window.refresh()

    def phase_one(self):
        self.window.paint_prompt(1)
        bet = self.window.get_input()
        self.update_balance(bet)
        self.window.draw_info(self.player.money, bet)

    def phase_two(self):
        self.window.paint_prompt(2)
        top_card = self.draw_card()
        self.dealer.deal(top_card)
        # 3, 2+13*len(self.dealer.hand)
        self.window.paint_card(self.window.dealer_side,
                               2, -12+13*len(self.dealer.hand), top_card)

    def update_balance(self, bet):
        temp = int(self.player.money)
        temp -= int(bet)
        self.player.money = str(temp)
        self.window.draw_info(self.player.money, bet)

    def draw_card(self):
        top_card = self.deck.draw()
        self.window.paint_decksize()
        return top_card


def start(stdscr):
    blackjack = Blackjack(stdscr)
    blackjack.play()


curses.wrapper(start)
