import random
from Card import Card

class Deck():
    def __init__ (self):
        self.cards = []
        self.build()

    def build(self):
        for v in ["A", "2", "3","4","5","6","7","8","9","10","J","Q","K"]:
            for s in ["C","D","H","S"]:
                self.cards.append (Card(v,s))

    def shuffle (self):
        n = len(self.cards)
        for i in range (n):
            r = random.randrange(i, n)
            tmp = self.cards[r]
            self.cards[r] = self.cards[i]
            self.cards[i] = tmp

    def remainCnt (self):
        return len (self.cards)

    def draw (self):
        if len(self.cards) > 0:
            return self.cards.pop()
    
    def reset (self):
        self.cards = []
        self.build()
        