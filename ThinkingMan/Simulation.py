from tkinter import Canvas
from Card import Card
from Pile import Pile
import Constant
import time

class Simulation ():
    pile = []        # Piles of cards used for checking if the game is winnable
    allMoves = []    # Records all moves for checking if the game is winnable
    allCards = []    # Records all cards for checking if the game is winnable
    canvas = None
    #cnt = 0

    def __init__ (self, pile):
        self.pile = pile.copy()
        Simulation.canvas.create_text (100, 100, text="Hello", tags="blabla")
        #self.dumpCanvas()
        #time.sleep (1)
        #c = self.pile [0].peekTopCard()
        #Simulation.canvas.move (c.id, 130, 130)
        #time.sleep (1)
        #Simulation.cnt = 0

    def dumpCanvas (self):
        print ("Dump canvas:")
        for id in Simulation.canvas.find_all():
            print ("\t", id, Simulation.canvas.gettags(id), Simulation.canvas.bbox (id))

    def nextMovePossible (self, pSrc, pDest):
        if self.pile [pSrc].isEmpty(): return False
        c = self.pile [pSrc].peekTopCard()
        while pDest < Constant.INDEX_MAX_FP:
            pDest += 1
            if self.pile [pDest].checkDrop(c) == 0:
                # Card can be moved from pSrc to pDest. Move it
                if self.pile[pDest].isEmpty():
                    print (c.name, "moved to empty pile #", pDest)
                else:
                    print (c.name, "moved to ", self.pile[pDest].peekTopCard().name, "on pile #", pDest)
                self.pile[pSrc].moveTopCard (self.pile[pDest])
                # Record it
                self.allMoves.append ([pSrc, pDest])
                self.allCards.append (c)
                c.adjustImageLocation()
                Simulation.canvas.tag_raise(c.id)
                time.sleep (.5)

                return True
        #print ("\t", c.name, " has no nextMovePossible")
        return False

    def win (self):
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_BP+1):
            if not self.pile[p].isEmpty(): return False
        return True
    
    def isWinnable (self):
        pSrc = 0
        pDest = 0
        while not self.nextMovePossible (pSrc, pDest) and pSrc < Constant.INDEX_MIN_FP: 
            pSrc += 1
            pDest = 0
        if pSrc == Constant.INDEX_MIN_FP: 
            print ("No card can be moved")
            return False  # No card can be moved.
        else:
            c = self.allCards[0]
            pSrc, pDest = self.allMoves[0]
            print ("1st Move ", c.name, "from pile #", pSrc, "to pile #", pDest)
        pSrc = 0
        pDest = 0

        while len(self.allMoves) > 0 and not self.win():
            while len(self.allMoves) > 0 and not self.win() and pSrc < Constant.INDEX_MIN_FP:
                if self.nextMovePossible (pSrc, pDest):
                    pSrc = 0
                    pDest = 0
                else:
                    pSrc += 1
                    pDest = Constant.INDEX_MIN_BP
                #Simulation.cnt += 1
                #if Simulation.cnt % 10 == 0:
                #    YN = input("Continue Y/N?")
                #    if YN == "N" or YN == "n": exit()

            if pSrc == Constant.INDEX_MIN_FP:
                # Unmove
                pSrc, pDest = self.allMoves.pop()
                c = self.allCards.pop()
                print ("\t", c.name, "moved BACK from pile #", pDest, "to pile #", pSrc)
                self.pile[pDest].moveTopCard(self.pile[pSrc])
                c.adjustImageLocation()
                Simulation.canvas.tag_raise(c.id)
                time.sleep (.1)

                pDest += 1
        if self.win ():
            print ("Winning moves:")
            while len (self.allCards) > 0:
                c = Simulation.allCards.pop(0)
                pSrc, pDest = Simulation.allMoves.pop(0)
                print ("\tMove ", c.name, "from pile #", pSrc, "to pile #", pDest)
            return True
        else:
            return False    