
class Card():

    ranks = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
             '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
    suits = {'CLUBS': '♣', 'DIAMONDS': '♦', 'HEARTS': '♥', 'SPADES': '♠'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.full_name = self.generate_full_name()

    def generate_full_name(self):
        names = {'A': 'ACE', 'J': 'JACK', 'Q': 'QUEEN', 'K': 'KING'}
        name = ""
        if str(self.rank) in names:
            name = names[self.rank]
        else:
            name = str(self.rank)

        full_name = name + " OF " + str(self.suit)
        return full_name

    def get_value(self):
        return self.ranks[self.rank]

    def draw(self):

        print("┌───────┐")
        print(f"│ {self.rank:<2}    │")
        print("│       │")
        print(f"│   {self.suits[self.suit]}   │")
        print("│       │")
        print(f"│    {self.rank:>2} │")
        print("└───────┘")
