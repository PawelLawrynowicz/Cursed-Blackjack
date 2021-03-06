import curses
import curses.textpad
import time
from card import Card
from deck import Deck


class Window:

    def __init__(self, stdscr, y, x, deck):
        self.deck = deck

        self.height, self.width = stdscr.getmaxyx()

        # self.get_input(stdscr)
        self.window = curses.newwin(self.height, self.width, y, x)
        self.window.box()
        self.window.hline(self.height//2, 1,
                          curses.ACS_HLINE, self.width-2)
        self.addstr(0, self.width//2, "BLACKJACK")
        self.addstr(0, 1, "DEALER")
        self.addstr(self.height//2, 1, "PLAYER")

        curses.curs_set(0)

        self.prompt = self.window.derwin(
            1, self.width//2 - 1, self.height//2, self.width//2)

        self.dealer_side = self.window.derwin(
            self.height//2 - 1, self.width-15, 1, 14)

        self.player_side = self.window.derwin(
            self.height//2 - 2, self.width-15, self.height//2 + 1, 14
        )

        self.cards_x = 15
        self.dealer_cards_y = 3
        self.player_cards_y = self.height//2+3

        self.paint_decksize()
        self.paint_back(3, 2)
        #self.card = Card("10", "SPADES")
        #self.paint_card(3, 15, self.card)
        #self.paint_card(3 + 1, 20, self.card)
        #self.paint_card(3 + 2, 25, self.card)

        self.window.refresh()

        self.info_width = self.width//2 - 10
        self.info = self.window.derwin(
            1, self.info_width, self.height//2, 10)

        time.sleep(1)
        # while self.window.getch():

    def clear(self):
        for y in range(3, self.window.getmaxyx()[0]-1):
            self.window.move(y, 2)
            self.window.clrtoeol()
        self.window.box()

    def addstr(self, y, x, string, attr=0):
        self.window.addstr(y, x, string, attr)

    def refresh(self):
        self.window.refresh()

    def paint_card(self, side, y, x, card):
        side.addstr(y, x, "┌───────┐")
        side.addstr(y+1, x, f"│ {card.rank:<2}    │")
        side.addstr(y+2, x, "│       │")
        side.addstr(y+3, x, f"│   {card.suits[card.suit]}   │")
        side.addstr(y+4, x, "│       │")
        side.addstr(y+5, x, f"│    {card.rank:>2} │")
        side.addstr(y+6, x, "└───────┘")

    def paint_back(self, y, x):
        self.window.addstr(y, x,   "┌───────┐")
        for i in range(5):
            self.window.addstr(y+i+1, x, "│       │")

        self.window.addstr(y+6, x, "└───────┘")

    def paint_decksize(self):
        y = 2
        x = 1
        self.window.addstr(y, x, f"DECKSIZE:    ")
        self.window.addstr(y, x, f"DECKSIZE: {self.deck.current_size()}")

    def get_input(self):
        prompt = self.window.derwin(1, self.width-2, self.height-2, 1)
        prompt.clear()
        prompt.addstr(0, 0, "INPUT: ")
        textbox = curses.textpad.Textbox(prompt, insert_mode=False)
        edit = textbox.edit()
        edit = edit.replace(" ", "\n")
        edit = edit.split('\n')
        return str(edit[1])

    def draw_info(self, balance, bet=0):
        self.info.clear()
        self.info.hline(0, 10, curses.ACS_HLINE, self.info_width)

        self.info.addstr(0, 0, "[BALANCE: " + str(balance) + "]")
        if bet == 0:
            bet = ""
        self.info.addstr(0, 14 + len(str(balance)), "[BET: " + str(bet) + "]")

    def paint_prompt(self, stage):
        """
            0 - declare starting money
            1 - bet / round start
            2 - deal
            3 - player decision
            4 - dealer drawing
            5 - comparing scores
        """
        stages = {0: "DECLARE YOUR BALANCE", 1: "PLACE YOUR BET", 2: "DEALING CARDS",
                  3: "HIT OR STAND?", 4: "DEALER DRAWING", 20: "YOU WIN", 21: "DEALER WINS", 22: "PUSH", 30: "PLAY AGAIN?", 10: "BUST, TOO MANY!"}

        self.prompt.clear()
        self.prompt.hline(0, 0, curses.ACS_HLINE, self.width//2-1)
        self.prompt.addstr(0, 0, stages[stage])
        self.prompt.refresh()

    def paint_dealer_score(self, score):
        height, width = self.dealer_side.getmaxyx()
        self.dealer_side.addstr(height-1, width//2-7,
                                "DEALER SCORE: " + str(score))

    def paint_player_score(self, score):
        height, width = self.player_side.getmaxyx()
        self.player_side.addstr(0, width//2-7,
                                "PLAYER SCORE: " + str(score))
