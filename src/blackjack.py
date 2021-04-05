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

        self.early_blackjack = False
        self.bet = 0
        self.bust = False
        self.dealer_bust = False
        self.command = ""

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

        self.initiate_game()

        while not game_over:
            self.initialize_round()
            self.take_bets()
            self.deal_cards()
            if not self.early_blackjack:
                while not self.stop_decision():
                    self.window.paint_prompt(3)
                    self.command = self.window.get_input()
                    self.player_decision()

                if self.bust:
                    self.dealer_win()
                else:
                    self.dealer_draw()
                    if self.dealer_bust:
                        self.player_win()
                    else:
                        self.compare_scores()

            if self.end():
                break

    def stop_decision(self):
        player_score = self.player.get_score()
        if self.command == "STAND":
            return True
        elif player_score > 21:
            self.bust = True
            return True
        elif player_score == 21:
            return True
        else:
            return False

    def initiate_game(self):
        self.window.paint_prompt(0)
        self.player.set_money(int(self.window.get_input()))
        self.window.draw_info(self.player.money)
        self.command = ""

    def initialize_round(self):
        self.early_blackjack = False
        self.bust = False
        self.dealer_bust = False
        self.command = ""
        self.window.info.clear()
        self.window.draw_info(self.player.get_money())

        self.window.refresh()

    def take_bets(self):
        self.window.paint_prompt(1)
        self.bet = self.window.get_input()
        self.update_balance(self.bet)
        self.window.draw_info(self.player.get_money(), self.bet)
        self.window.info.refresh()

    def deal_cards(self):
        self.window.paint_prompt(2)
        top_card = self.draw_card()
        self.dealer.deal(top_card)
        self.window.paint_card(self.window.dealer_side,
                               2, -12+13*len(self.dealer.hand), top_card)
        self.window.paint_dealer_score(self.dealer.get_score())
        self.window.dealer_side.refresh()
        time.sleep(1)

        top_card = self.draw_card()
        self.player.deal(top_card)
        self.window.paint_card(self.window.player_side,
                               self.window.height//2-10-len(self.player.hand), -4+5*len(self.player.hand), top_card)
        self.window.paint_player_score(self.player.get_score())
        self.window.player_side.refresh()
        time.sleep(1)

        top_card = self.draw_card()
        self.dealer.deal(top_card)
        self.window.paint_back(3, 2+13*len(self.dealer.hand))
        self.window.dealer_side.refresh()
        time.sleep(1)

        top_card = self.draw_card()
        self.player.deal(top_card)
        self.window.paint_card(self.window.player_side,
                               self.window.height//2-10-len(self.player.hand), -4+5*len(self.player.hand), top_card)
        self.window.paint_player_score(self.player.get_score())
        self.window.player_side.refresh()
        time.sleep(1)

        blackjack = self.check_for_blackjack()
        if any(blackjack):
            if blackjack[0] == True and blackjack[1] == False:
                self.player_win()
            elif blackjack[0] == False and blackjack[1] == True:
                self.dealer_win()
            else:
                self.push()
            self.early_blackjack = True

    def player_decision(self):
        if self.command == "HIT":
            top_card = self.draw_card()
            self.player.deal(top_card)
            self.window.paint_card(self.window.player_side,
                                   self.window.height//2-10-len(self.player.hand), -4+5*len(self.player.hand), top_card)
            self.window.paint_player_score(self.player.get_score())
            self.window.refresh()
            self.window.player_side.refresh()
        else:
            return

    def dealer_draw(self):
        self.window.paint_prompt(4)
        time.sleep(1)
        hidden_card = self.dealer.hand[1]
        self.window.paint_card(self.window.dealer_side,
                               2, -12+13*len(self.dealer.hand), hidden_card)
        self.window.paint_dealer_score(self.dealer.get_score())
        self.window.dealer_side.refresh()
        while self.dealer.get_score() < 17:
            time.sleep(1)
            top_card = self.draw_card()
            self.dealer.deal(top_card)
            self.window.paint_card(self.window.dealer_side,
                                   2, -12+13*len(self.dealer.hand), top_card)
            self.window.paint_dealer_score(self.dealer.get_score())
            self.window.dealer_side.refresh()
        if self.dealer.get_score() > 21:
            self.dealer_bust = True

    def compare_scores(self):
        if self.player.get_score() > self.dealer.get_score():
            self.player_win()
        elif self.player.get_score() < self.dealer.get_score():
            self.window.paint_prompt(21)
            self.dealer_win()
        else:
            self.window.paint_prompt(22)
            self.push()
        self.window.info.refresh()

    def end(self):
        end = False
        self.window.paint_prompt(30)
        command = self.window.get_input()
        if command == "NO":
            end = True
        self.window.player_side.clear()
        self.window.dealer_side.clear()
        return end

    def update_balance(self, bet):
        temp = int(self.player.get_money())
        temp -= int(bet)
        self.player.set_money(temp)
        self.window.draw_info(self.player.get_money(), bet)

    def draw_card(self):
        top_card = self.deck.draw()
        self.window.paint_decksize()
        self.window.refresh()
        return top_card

    def player_win(self):
        self.window.paint_prompt(20)
        self.player.hand = []
        self.dealer.hand = []
        self.player.set_money(self.player.get_money() + 2*int(self.bet))
        self.bet = 0
        self.window.draw_info(self.player.get_money())
        self.window.refresh()
        time.sleep(3)

    def dealer_win(self):
        self.player.hand = []
        self.dealer.hand = []
        self.bet = 0
        if self.bust == True:
            self.window.paint_prompt(10)
        self.window.draw_info(self.player.get_money())
        self.window.info.refresh()
        time.sleep(3)

    def push(self):
        self.player.hand = []
        self.dealer.hand = []
        self.player.money += int(self.bet)
        self.bet = 0
        self.window.draw_info(self.player.get_money())
        self.window.refresh()


def start(stdscr):
    blackjack = Blackjack(stdscr)
    blackjack.play()


curses.wrapper(start)
