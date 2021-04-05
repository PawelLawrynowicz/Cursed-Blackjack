from deck import Deck
from card import Card


class Player:
    def __init__(self, dealer, money, deck):
        self.dealer = dealer
        self.hand = []
        self.money = money
        self.deck = deck
        self.score = 0

    def deal(self, card):
        self.hand.append(card)

    def declare_bet(self, bet):
        return bet

    def hit(self):
        self.hand.append(self.deck.draw())
        self.check_score()
        if self.score > 21:
            return
        return 0

    def stand(self):
        return True

    def check_score(self):
        self.score = 0
        aces = 0
        for card in self.hand:
            value = card.get_value()
            if value == 1:
                aces += 1
            self.score += value
        if aces > 0 and self.score <= 11:
            self.score += 10

    def get_score(self):
        self.check_score()
        return self.score

    def display(self):
        if self.dealer:
            print("hidden")
            print(self.hand[1].full_name)
        else:
            for card in self.hand:
                print(card.full_name)
            print("Value: ", self.get_score())

    def clear_hand(self):
        self.hand = []

    # TODO:
    def double_down(self):
        pass

    # TODO:
    def split(self):
        pass


# deck = Deck()
# player = Player(False, 100, deck)
# player.hand.append(deck.cards.pop(13))
# print(player.get_score())
