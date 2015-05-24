"""
video poker odds payout

"""
from singlecard import single_card

class vp_odds():
    def __init__(self):
        pass    


    def is_royal_flush(self, hand):
        if self.is_flush(hand):
            v=[]
            for i in range(0, len(hand)):
                v.append(hand[i].value_of)
            vs = sorted(v)
            if vs == [8, 9, 10, 11, 12] :
                return True 
        return False

    def is_straight_flush(self,hand):
        if self.is_flush(hand) and self.is_straight(hand):
            return True
        return False
        
    def is_three_of_a_kind(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].value_of)
        vs = sorted(v)
        if vs[0] == vs[1] and vs[1] == vs[2]:
            self.marked = vs[0]
            return True
        if vs[1] == vs[2] and vs[2] == vs[3]:
            self.marked = vs[1]
            return True
        if vs[2] == vs[3] and vs[3] == vs[4]:
            self.marked = vs[2]
            return True

        return False

    def is_four_of_a_kind(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].value_of)
        vs = sorted(v)
        if vs[0] == vs[1] and vs[1] == vs[2] and vs[2] == vs[3]:
            return True
        if vs[1] == vs[2] and vs[2] == vs[3] and vs[3] == vs[4]:
            return True
        return False

    def is_full_house(self, hand):
        if self.is_three_of_a_kind(hand):
            v = []
            for i in range(0, len(hand)):
                if hand[i].value_of != self.marked:
                    v.append(hand[i].value_of)
            if v[0] == v[1] :
                return True
 
        return False

    def is_flush(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].order_in)
        vs = [v[0]//13, v[1]//13, v[2]//13, v[3]//13, v[4]//13]
        if vs[0] == vs[1] and vs[1] == vs[2] and vs[2] == vs[3] and vs[3] == vs[4] :
            return True
        return False

    def is_straight(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].value_of)
        vs = sorted(v)
        if (vs == [0,1,2,3,4]  or vs == [1,2,3,4,5] or vs == [2,3,4,5,6] or
           vs == [3,4,5,6,7]  or vs == [4,5,6,7,8] or vs == [5,6,7,8,9] or
           vs == [6,7,8,9,10]  or vs == [7,8,9,10,11] or vs == [8,9,10,11,12]) :
            return True
        return False


    def is_pair_greater_than_10(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].value_of)
        vs = sorted(v)
        if vs[0] == vs[1] and vs[0]>=8:
            return True
        if vs[1] == vs[2] and vs[1]>=8:
            return True
        if vs[2] == vs[3] and vs[2]>=8:
            return True
        if vs[3] == vs[4] and vs[3]>=8:
            return True

        return False
    
    def is_pair(self, hand):
        v = []
        for i in range(0, len(hand)):
            v.append(hand[i].value_of)
        vs = sorted(v)
        for i in range(0,len(vs)-1):
            if vs[i]==vs[i+1]:
                self.marked = vs[i]
                return True             
        return False 
        
    def is_two_pair(self, hand):
        if self.is_pair(hand):
            v = []
            for i in range(0, len(hand)):
                if hand[i].value_of != self.marked:
                    v.append(hand[i])
            if self.is_pair(v):
                return True
        return False
        
    def dummy(self, hand, bet):
        return 5
        
        
    def calculate_payout(self, hand, bet):
        if len(hand) != 5:
            return -500, 'cheated?'
        if self.is_royal_flush(hand):
            # e.g. 10H JH QH KH AH
            return bet * 250, 'royal flush'
        elif self.is_straight_flush(hand):
            # e.g. 5D 6D 7D 8D 9D
            return bet * 9, 'straight flush'
        elif self.is_four_of_a_kind(hand):
            # e.g. 6C 6D 6S 6H 10D
            return bet * 5, '4 of a kind'
        elif self.is_full_house(hand):
            # e.g. 8D 8C KH KS KD
            return bet * 3, 'full house'
        elif self.is_flush(hand):
            # e.g. 4H 7H 8H JH KH
            return bet * 2, 'flush'
        elif self.is_straight(hand):
            # e.g. 4H 5C 6C 7D 8S
            return bet * 2, 'straight'
        elif self.is_three_of_a_kind(hand):
            # e.g. 6D 4H 4D 4C KS
            return bet * 2, '3 of a kind'
        elif self.is_two_pair(hand):
            return bet * 2, 'two pair'
        elif self.is_pair_greater_than_10(hand):
            # e.g. AD AH 3C 6D QC
            return bet, 'pair > 10'
        else:
            return -bet, 'loss' # you lose.

    def list_odds(self):
            odds = []
            odds.append("1:250 Royal Flush")
            odds.append("1:9   Straight Flush")
            odds.append("1:5   Four of a Kind")
            odds.append("1:3   Full House")
            odds.append("1:2   Flush")
            odds.append("1:2   Straight")
            odds.append("1:2   Three of a Kind")
            odds.append("1:2   Two Pairs")
            odds.append("1:1   Pair Greater than Ten")
            return odds
            

