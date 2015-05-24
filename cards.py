from math import *
from random import *
from singlecard import single_card

"""
worlds simplest card class
may 2015
stevef
"""

class Cards():
    def __init__(self):
        pass

    def r(self,x):
        seed = random()
        y = seed * x
        return int(ceil((y)))


    def banner(self):
        print 'Zero player war'
        print '-- test game --'


    def cardstr(self, cardseed):
        suits = ('H', 'D', 'C', 'S')
        face = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        cardsuit = suits[cardseed // 13]
        cardvalue = cardseed % 13
        return face[cardvalue] + str(cardsuit)


    def opendeck(self):
        deck = []
        # dealt, ordinal, value, suit
        for x in range(0, 52):
            deck.append(single_card(is_dealt=False, order_in=x, value_of=x % 13, display=self.cardstr(x)))
        return deck


    def shuffledeck(self, deck):
        shuffled = []
        for _ in range(0, 52):
            flag = False
            while not flag:
                x = self.r(52) - 1
                if not deck[x].is_dealt:
                    deck[x].is_dealt = True
                    flag = True
                    shuffled.append(single_card(is_dealt=False, order_in=deck[x].order_in, value_of=deck[x].value_of, display=deck[x].display))

        return shuffled


    def deal(self, n, deck):
        hand = []
        for i in range(0, n):
            hand.append(deck[0])
            deck.remove(hand[i])
        return hand


    def printhand(self, hand):
        for i in range(0, len(hand)):
            print hand[i].display,
        print


    def play(self, p1, p2):
        if p1[0].value_of < p2[0].value_of:
            return 0, 1, 0
        elif p1[0].value_of > p2[0].value_of:
            return 1, 0, 0
        else:
            return 0, 0, 1


    def game(self):
        self.banner()
        deck = self.opendeck()
        print "un-shuffled deck:"
        self.printhand(deck)

        shuffled = self.shuffledeck(deck)
        print "shuffled deck: "
        self.printhand(shuffled)

        hand1 = self.deal(26, shuffled)
        hand2 = self.deal(26, shuffled)
        self.printhand(hand1)
        self.printhand(hand2)
        sc1 = 0
        sc2 = 0
        ties = 0

        for _ in range(0, 26):
            p1 = self.deal(1, hand1)
            p2 = self.deal(1, hand2)
            x, y, z = self.play(p1, p2)
            sc1 += x
            sc2 += y
            ties += z
            
        print sc1, ' ', sc2, ' ', ties

    def test_hand(self, tc):
        deck = self.opendeck()
        if tc == "straight flush":
            pass
        elif tc == "flush":
            deck[1] = deck[10]
        elif tc == "straight":
            deck[0] = deck[13]  # straight
        elif tc == "pair greater than ten":
            deck[0] = deck[8]  
            deck[2] = deck[21]
        elif tc == "three of a kind":
            deck[0] = deck[11]  
            deck[2] = deck[24]
            deck[4] = deck[37]
        elif tc == "four of a kind":
            deck[0] = deck[11]  
            deck[2] = deck[24]
            deck[4] = deck[37]
            deck[1] = deck[50]
        elif tc == "royal flush":
            deck[0] = deck[8]
            deck[1] = deck[9]
            deck[2] = deck[10]
            deck[3] = deck[11]
            deck[4] = deck[12]
        elif tc == "full house":
            deck[0] = deck[11]
            deck[1] = deck[24]
            deck[2] = deck[37]
            deck[3] = deck[6]
            deck[4] = deck[19]          
        elif tc == "two pair":
            deck[0] = deck[11]
            deck[1] = deck[24]
            deck[2] = deck[39]
            deck[3] = deck[6]
            deck[4] = deck[19]          
        elif tc == "bad flush bug":
            deck[1] = deck[24]
            
        else:
            pass
        return deck
        
def main():
    s = Cards()
    s.game()

if __name__ == "__main__":
    main()
