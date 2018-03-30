#!/usr/bin/env python

import pygame
import sys
from cards import Cards
from vp_odds import *


RED = (255, 0, 0)
GREEN = (100, 155, 100)
BLUE = (100,100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
    
class Game():
    """
        GAME - class
        class implements UI for videopoker in pygame.
    """
    def __init__(self):
        """
            INIT
        """
	# pygame - setup 
        pygame.init()
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.size = (600, 500)
        self.center = (300, 250)
        self.screen = pygame.display.set_mode(self.size)

        self.card_imgs= []
        self.balance = 100
        self.bet_amount = 5
        self.cm = Cards()
        
        self.reset()

        self.key_pressed = "stop"
        self.key_pressed_hold = ""
        self.player_rect_clip = pygame.Rect(0, 0, 75, 100)
        self.stage = 0
        self.step = 0
        self.last_mouse = (0, 0)

        # set up fonts
        self.basicFont = pygame.font.SysFont(None, 48)
        self.subFont = pygame.font.SysFont(None, 24)
        self.subsubFont = pygame.font.SysFont(None, 12)

        self.card_layout_play()


    def card_layout_play(self):
        self.card_rects = []
        self.card_rects.append(pygame.Rect(20, 10, 75, 100))
        self.card_rects.append(pygame.Rect(20, 105, 75, 100))
        self.card_rects.append(pygame.Rect(20, 200, 75, 100))
        self.card_rects.append(pygame.Rect(20, 295, 75, 100))
        self.card_rects.append(pygame.Rect(20, 390, 75, 100))

        self.deal_rect = pygame.Rect(200, 200, 75, 100)
        self.deal_card = pygame.transform.scale(pygame.image.load("cards/deal.png"),(72, 90))

        self.bet_rect = pygame.Rect(200, 105, 75, 100)
        self.bet_card = pygame.transform.scale(pygame.image.load("cards/5coin.png"),(72, 90))

        self.help_rect = pygame.Rect(200, 10, 75, 100)
        self.help_card = pygame.transform.scale(pygame.image.load("cards/help.png"),(72, 90))


    def reset(self):
        """
           RESET 
        """
        self.deck = self.cm.shuffledeck(self.cm.opendeck())

        # for testing, call for particular hands:
        # self.deck = self.cm.test_hand("four of a kind")

        self.card_imgs=[]
        for i in range (0,5):
            self.card_imgs.append(pygame.transform.scale(pygame.image.load("cards/back.png"),(72, 90)))


        self.hand =[None,None,None,None,None,]
        self.card_locks = [False, False, False, False, False]
        self.message = 'Set bet and click deal.'


    def handle_events(self):
        """
            HANDLE EVENTS - keys and mouse clicks
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            self.key_pressed = "esc"
                        elif event.key == pygame.K_F1:
                            self.key_pressed = "help"
                        elif event.key == pygame.K_SPACE:
                            self.key_pressed = "space"
                        else:
                            pass
            if event.type == pygame.MOUSEBUTTONUP:
                self.last_mouse = event.pos 
                self.key_pressed_hold = self.key_pressed
                self.key_pressed = "mouse"

    def cardN_button(self,n):
        """
            CARD pressed - flip card 
        """
        if self.step == 2 or self.step == 0:
           pass
        else:
           if self.hand[n].is_dealt:
                self.card_imgs[n] = pygame.transform.scale(pygame.image.load("cards/"+self.hand[n].display+".png"),(72, 90))
                self.card_locks[n] = True
                self.hand[n].is_dealt = False
           else:
                self.card_imgs[n] = pygame.transform.scale(pygame.image.load("cards/back.png"),(72, 90))
                self.card_locks[n] = False
                self.hand[n].is_dealt = True

    def score_hand(self):
        """
         SCORE HAND
        """
        vodds = vp_odds()
        x,s = vodds.calculate_payout(self.hand, self.bet_amount)
        self.message = s + ' pays: $'+ str(x)
        return x


    def deal_tapped(self):
        """
            DEAL button tapped.
        """
        if self.step == 2:
            self.reset()
            self.step = 0
            self.message = 'Set bet, press deal.'
        else:
            self.step += 1
            self.message = 'Pick, and deal.'
            hand = self.cm.deal(5,self.deck)
            for i in range(0,5):
                if not self.card_locks[i]:
                    self.hand[i] = hand[i]
                    self.card_imgs[i] = pygame.transform.scale(pygame.image.load("cards/"+hand[i].display+".png"),(72, 90))

            self.card_locks = [True, True, True, True, True]
            if self.step == 2:
                self.balance += self.score_hand()
            if self.balance <= 0:
                self.stage = 3 

    def bet_next(self):
        """
            BET changed
        """
        if self.step !=0:
            return

        if self.bet_amount == 5 :
            self.bet_amount = 10
            self.bet_card = pygame.transform.scale(pygame.image.load("cards/10coin.png"),(72, 90))
        elif self.bet_amount == 10:
            self.bet_amount = 20
            self.bet_card = pygame.transform.scale(pygame.image.load("cards/20coin.png"),(72, 90))
        elif self.bet_amount == 20:
            self.bet_amount = 5
            self.bet_card = pygame.transform.scale(pygame.image.load("cards/5coin.png"),(72, 90))
        else:
            pass


    def draw_stage1(self):
        """
            DRAW STAGE 1 - Play Screen
        """
        self.screen.fill(BLUE)
        
        for i in range(0, len(self.card_imgs)):
            self.screen.blit(self.card_imgs[i], self.card_rects[i], self.player_rect_clip)

        self.screen.blit(self.deal_card, self.deal_rect, self.player_rect_clip)
        self.screen.blit(self.bet_card, self.bet_rect, self.player_rect_clip)
        self.screen.blit(self.help_card, self.help_rect, self.player_rect_clip)
    
        for i in range(0, len(self.card_imgs)):
            if self.card_rects[i].collidepoint(self.last_mouse):
                self.cardN_button(i)
                self.last_mouse = (-1, -1)
                break

        if self.deal_rect.collidepoint(self.last_mouse):
            self.last_mouse = (-1, -1)
            self.deal_tapped()

        if self.bet_rect.collidepoint(self.last_mouse):
            self.last_mouse = (-1, -1)
            self.bet_next()

        if self.help_rect.collidepoint(self.last_mouse):
            self.last_mouse = (-1, -1)
            self.key_pressed ="help"

        self.stage1_text = self.basicFont.render(self.message, True, WHITE, BLUE)
        textRect = self.stage1_text.get_rect()
        textRect.x = 220
        textRect.y = 320
        self.screen.blit(self.stage1_text, textRect)
        
        balance = "Current balance is: " + str(self.balance)
        balance_text = self.subFont.render(balance, True, WHITE, BLUE)
        textRect = self.stage1_text.get_rect()
        textRect.x = 220
        textRect.y = 400
        self.screen.blit(balance_text, textRect)


    def draw_stage0(self):
        """
            DRAW STAGE 0 - Title/Splash 
        """
        # set up the text
        self.stage0_text = self.basicFont.render('Welcome to Video Poker', True, WHITE, BLACK)
        self.stage0_subtext1 = self.subFont.render('Press SPACE to Continue', True, WHITE, BLACK)
        self.stage0_subtext2 = self.subFont.render('F1 for help Or ESC to exit', True, WHITE, BLACK)

        self.screen.fill(BLACK)
        if self.key_pressed == "space":
            self.stage = 1

        textRect = self.stage0_text.get_rect()
        textRect.center = self.center
    
        textRect.centery -= 150
        self.screen.blit(self.stage0_text, textRect)        

        textRect.centery += 50
        self.screen.blit(self.stage0_subtext1, textRect)

        textRect.centery += 20
        self.screen.blit(self.stage0_subtext2, textRect)

    def draw_stage2(self):
        """
            DRAW STAGE 2 - Help
        """
        # set up the text
        self.stage2_text = self.basicFont.render('Video Poker - Help', True, WHITE, GREEN)
        self.stage2_subtext1 = self.subFont.render('Press SPACE to Continue', True, WHITE, BLACK)

        self.screen.fill(GREEN)

        if self.key_pressed == "space":
            self.stage = 1

        textRect = self.stage2_text.get_rect()
        textRect.center = self.center

        textRect.centery -= 200
        self.screen.blit(self.stage2_text, textRect)

        sub_text = "Press SPACE to Play"
        xtext_rect = self.subFont.render(sub_text, True, WHITE, GREEN)
        sub_text_rect = xtext_rect.get_rect()
        sub_text_rect.center = self.center
        sub_text_rect.centery -= 175
        self.screen.blit(xtext_rect, sub_text_rect)

        # get the list of odds from the odds machine
        v = vp_odds()
        odds = v.list_odds()
        for i in range(0, len(odds)):
            text  = odds[i]
            xtext = self.subFont.render(text, True, WHITE, GREEN)
            textRect = xtext.get_rect()
            textRect.x = 120
            textRect.y = 120 + i*30
            self.screen.blit(xtext, textRect)


    def draw_stage3(self):
        """
            DRAW STAGE 3 - Broke
        """
        self.screen.fill(BLUE)
        if self.key_pressed == "space":
            self.stage = 1
        notes = []
        notes.append("You have run out of money!")
        notes.append("I will credit you 100 dollars.")
        notes.append("Press space to continue")
        notes.append("or ESC to return to the title screen")
        for i in range(0, len(notes)):
            text  = notes[i]
            xtext = self.subFont.render(text, True, WHITE, BLUE)
            textRect = xtext.get_rect()
            textRect.x = 120
            textRect.y = 120 + i*30
            self.screen.blit(xtext, textRect)
        self.balance = 100


    @staticmethod
    def main():
        x = Game()
        x.run()

    def run(self):
        """
            RUN - main loop.
        """
        while True:
            self.handle_events()
            if self.key_pressed == "esc" and self.stage == 0:
                pygame.quit()
                sys.exit()
            if self.key_pressed == "esc" and self.stage != 0:
                self.key_pressed = "none"
                self.stage = 0
            if self.key_pressed == "help" and self.stage !=2:
                self.direcion = "none"
                self.stage = 2
            if self.stage == 0:
                self.draw_stage0()
            elif self.stage == 1:
                self.draw_stage1()
            elif self.stage == 2:
                self.draw_stage2()  
            elif self.stage == 3:
                self.draw_stage3()  
            else:
                pass

            self.clock.tick(self.FPS)
            pygame.display.update()
    
if __name__ == "__main__":
    Game.main()

