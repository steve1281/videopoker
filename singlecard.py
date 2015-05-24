"""
class to encapsulate a single card.

a card is an array of four elements:
  is_dealt : boolean indicating whether or not the card was assigned in a non-destructive way
  order_in : a cards position in a fresh (sorted hearts, diamonds, clubs, spades) deck
  value_of : the value of the card: 2,3,4,5,6,7,8,9,10,J,Q,K,A
  display  : the textual represenation of the card (eg:  10H )

This class stores this information is a more generic format.

"""
class single_card():
    def __init__(self,**kw):
        try:
            self._is_dealt = kw['is_dealt'] 
        except Exception:
            self._is_dealt = False
        try:
            self._order_in = kw['order_in'] 
        except Exception:
            self._order_in = 0
        try:
            self._value_of = kw['value_of'] 
        except Exception:
            self._value_of = 0
        try:
            self._display = kw['display'] 
        except Exception:
            self._value_of = '' 


    def raw_assign(self, acard):
        self._is_dealt = acard[0]
        dself._order_in = acard[1]
        self._value_of = acard[2]
        self._display =  acard[3]
        self._is_set = True

    def get_is_dealt(self):
        return self._is_dealt
    def get_order_in(self):
        return self._order_in
    def get_value_of(self):
        return self._value_of
    def get_display(self):
        return self._display


    def set_is_dealt(self, x):
        self._is_dealt = x
    def set_order_in(self, x):
        self._order_in = x
    def set_value_of(self, x):
        self._value_of = x
    def set_display(self, x):
        self._display = x


    is_dealt = property(get_is_dealt, set_is_dealt)
    order_in = property(get_order_in, set_order_in)
    value_of = property(get_value_of, set_value_of)
    display = property(get_display, set_display)



          
