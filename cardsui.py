import ui
from cards import Cards
from vp_odds import *

"""
  Cards UI - steve falcigno, may 2015
  single_card(is_dealt=False, order_in=deck[x].order_in, value_of=deck[x].value_of, display=deck[x].display))
"""
class MyView(ui.View):

    def cardN_button(self,n):
        if self.step == 2 or self.step == 0:
            pass
        else:
            if self.hand[n].is_dealt:
                self.card_imgs[n] = self.make_button(self.card_button[n], 'cards/'+self.hand[n].display+'.png') 
                self.card_locks[n] = True
                self.hand[n].is_dealt = False
            else:
                self.card_imgs[n] = self.make_button(self.card_button[n], 'cards/back.png')
                self.card_locks[n] = False
                self.hand[n].is_dealt = True
        self.set_needs_display()
    
    def card1_button(self, sender):
        self.cardN_button(0)

    def card2_button(self, sender):
        self.cardN_button(1)

    def card3_button(self, sender):
        self.cardN_button(2)

    def card4_button(self, sender):
        self.cardN_button(3)

    def card5_button(self, sender):
        self.cardN_button(4)

    def set_bet_5(self, sender):
        if self.step ==0:
            self.bet_amount = 5
            self.play_coin = self.make_button(self.set_bet_10, "cards/5coin.png")
            self.set_needs_display()

    def set_bet_10(self, sender):
        if self.step ==0:
            self.bet_amount = 10
            self.play_coin = self.make_button(self.set_bet_20, "cards/10coin.png")
            self.set_needs_display()

    def set_bet_20(self, sender):
        if self.step ==0:
            self.bet_amount = 20
            self.play_coin = self.make_button(self.set_bet_5, "cards/20coin.png")
            self.set_needs_display()

        
    def __init__(self):
        """
            INIT
        """     
        self.bet_amount = 5 # default bet is 5
        
        self.stage = "title"  # play, title, help
        
        self.title_b = self.make_button(self.goto_play_screen, "cards/play.png")
        self.help_b = self.make_button(self.goto_play_screen, "cards/play.png")
        self.play_b = self.make_button(self.goto_help_screen, "cards/help.png")
        self.play_coin = self.make_button(self.set_bet_10, "cards/5coin.png")
        

        self.message = "Click deal."
        self.balance = 100
        self.cm = Cards()
        self.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
        self.card_imgs=[]
        self.buttons=[]
        self.step = 0
        self.card_button = [self.card1_button, self.card2_button, self.card3_button, self.card4_button, self.card5_button,]
        self.reset()
    
        self.buttons.append(self.make_button(self.button_tapped, "cards/deal.png"))     
        
        self.score_label  = ui.Label()
        self.score_label.x = 150
        self.score_label.y = 450
        self.score_label.height = 30
        self.score_label.width = 100
        self.score_label.text = "Balance: "

        self.score_value_label  = ui.Label()
        self.score_value_label.x = 250 
        self.score_value_label.y = 450
        self.score_value_label.height = 30
        self.score_value_label.width =75
        self.score_value_label.text = "$" + str(self.balance)
        self.score_value_label.background_color = (55,55,55)

        self.winning_label  = ui.Label()
        self.winning_label.x = 250 
        self.winning_label.y = 350
        self.winning_label.height = 30
        self.winning_label.width =175
        self.winning_label.text = self.message
        #self.winning_label.background_color = (55,55,55)
        
    def score_hand(self):
        """
            SCORE HAND
        """
        vodds = vp_odds()
        x,s = vodds.calculate_payout(self.hand, self.bet_amount)
        self.message = s + ' pays: $'+ str(x)
        return x
        
        
    def button_tapped(self, sender):        
        if self.step == 2:
            self.reset()
            self.step = 0
            self.message = 'Deal for next hand.'
        else:
            self.step += 1
            self.message = 'Pick, and deal.'
            hand = self.cm.deal(5,self.deck)
            
            for i in range(0,5):        
                if not self.card_locks[i]:
                    self.hand[i] = hand[i]
                    self.remove_subview(self.card_imgs[i])
                    self.card_imgs[i] = self.make_button(self.card_button[i], 'cards/'+hand[i].display+'.png')

            self.card_locks = [True, True, True, True, True]
            if self.step == 2:
                self.balance += self.score_hand()
                if self.balance <= 0:
                    self.stage = 'broke'
                self.score_value_label.text = "$" + str(self.balance)

        self.set_needs_display()
        
    def make_button(self, callback, image):
        button = ui.Button()     
        button.width = 72
        button.height = 90
        button.background_image = ui.Image.named(image)
        button.flex = 'LRTB'                                  
        button.action = callback
        return button                      

    def reset(self):
        """
            RESET 
        """
        self.deck = self.cm.shuffledeck(self.cm.opendeck())
        
        # for testing, call for particular hands:
        # self.deck = self.cm.test_hand("four of a kind")
        
        self.card_imgs=[]
        for i in range (0,5):
            self.card_imgs.append(self.make_button(self.card_button[i], "cards/back.png"))

        self.hand =[None,None,None,None,None,]
        self.card_locks = [False, False, False, False, False]
        self.message = 'Click deal.'
        

    def did_load(self):
        pass
    
    def will_close(self):
        pass
        
    def goto_play_screen(self, sender):
        self.stage = "play"
        self.set_needs_display()

    def goto_help_screen(self, sender):
        self.stage = "help"
        self.set_needs_display()
        
    def draw(self):
        """
            DRAW
        """
        # self.bounds =(0,0,320,504)
        # print self.width,',',self.height
        path = ui.Path.rect(0,0,self.width, self.height)
        ui.set_color('brown')
        path.fill()
        # ui.set_color('green')
        # path.line_width=30
        # path.stroke()
        
        # Remove all the current sub views.
        for i in self.subviews:
            self.remove_subview(i)
            
        if self.stage == "play":
            
            
            for i in range(0,len(self.card_imgs)):
                self.card_imgs[i].center = (82, 50+100*i)
                self.add_subview(self.card_imgs[i])
            x = self.width * 0.5 + 100
            y = self.height * 0.5 
            for i in range(0,len(self.buttons)):
                self.buttons[i].center = (x, y + 100*i) 
                self.add_subview(self.buttons[i])

            self.add_subview(self.score_label)
            self.score_value_label.x = 225
            self.add_subview(self.score_value_label)
            self.winning_label.x = 150
            self.winning_label.text = self.message
            
            self.add_subview(self.winning_label)
            
            self.play_coin.center = (x,y-100)
            self.add_subview(self.play_coin)
            
            self.play_b.center = (x,y-200)
            self.add_subview(self.play_b)
            
        if self.stage == "help":
            # add in our views
            self.add_subview(self.help_b)
            tit = ui.Label()
            tit.x = 100
            tit.y = 0
            tit.height = 60
            tit.width = 500
            tit.text = "Video Poker - Help"
            self.add_subview(tit)
            
            v = vp_odds()
            list_odds = v.list_odds()
            for i in range(0, len(list_odds)):
                x = ui.Label()
                x.x = 10
                x.y = 100 + i*30
                x.height = 30
                x.width = 350
                x.text = list_odds[i]
                self.add_subview(x)
                
        
        if self.stage == "title":
            tit = ui.Label()
            tit.x = 100
            tit.y = 0
            tit.height = 60
            tit.width = 500
            tit.text = "- Video Poker - "
            self.add_subview(tit)

            self.add_subview(self.title_b)
        
        if self.stage == 'broke':
            tit = ui.Label()
            tit.x = 100
            tit.y = 0
            tit.height = 60
            tit.width = 500
            tit.text = "- Video Poker - "
            self.add_subview(tit)

            self.add_subview(self.title_b)
            self.balance = 100
            self.score_value_label.text = "$" + str(self.balance)
            list_text = ['You are broke!','I will credit you 100 dollars,','Press play to continue.']
            for i in range(0, len(list_text)):
                x = ui.Label()
                x.x = 10
                x.y = 100 + i*30
                x.height = 30
                x.width = 350
                x.text = list_text[i]
                self.add_subview(x)
            
            
    def layout(self):
        pass
    
    def touch_began(self, touch):
        pass
    
    def touch_moved(self, touch):
        pass
    
    def touch_ended(self, touch):
        pass
        
    def keyboard_frame_will_change(self,frame):
        pass
    
    def keyboard_frame_did_change(self, frame):
        pass


view = MyView()
view.present('sheet')
    
        
        
        
        
        
        
        
        
