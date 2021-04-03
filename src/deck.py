from card import Card
import requests


class Deck():
    def __init__(self):
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                card = Card(rank, suit)
                self.cards.append(card)
        self.size = self.current_size()

    # Randomly generated sequence of values ranging from 0 to current decksize
    def create_link(self):
        link = "https://www.random.org/sequences/?min=0&max=" + \
            str(self.current_size() - 1) + "&col=1&format=plain&rnd=new"
        return link

    # TODO: ADD TESTS TO SEE IF ALL CARDS ARE REPRESENTED
    def shuffle(self):
        self.link = self.create_link()
        response = requests.get(url=self.link)
        # Split the request on b"\n" and delete last element which is b"'"
        order = response._content.split(b'\n')[:-1]
        # Turn the byte array into an int array with values ranging from 0 to 51
        for i in range(len(order)):
            order[i] = int(order[i])

        for i in range(self.current_size()-1, -1, -1):
            for j in order:
                self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self):
        top = self.cards.pop()
        return top

    def current_size(self):
        return len(self.cards)

    def add_deck(self):
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                card = Card(rank, suit)
                self.cards.append(card)
        self.shuffle()
        return self.cards
