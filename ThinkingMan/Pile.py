from Card import Card
import Constant

class Pile():
    def __init__ (self, nb):
        self.pileNb = nb
        self.cards = []     # Cards in the pile
        self.xMin = 0       # Top Left coordinates of the pile
        self.yMin = 0
        self.xMax = 0       # Bottom Right coordinates of the pile
        self.yMax = 0
        self.type = None
        if (nb >= Constant.INDEX_MIN_PP and nb <= Constant.INDEX_MAX_PP): self.type = Constant.PLAYPILE
        if (nb >= Constant.INDEX_MIN_BP and nb <= Constant.INDEX_MAX_BP): self.type = Constant.BUFFERPILE
        if (nb >= Constant.INDEX_MIN_FP and nb <= Constant.INDEX_MAX_FP): self.type = Constant.FINALPILE

        if self.type == Constant.PLAYPILE: 
        # Define where the pile is located
            xBase = Constant.PPILE_XBASE
            yBase = Constant.PPILE_YBASE
            self.xMin = xBase + (self.pileNb) * Constant.PILE_WIDTH

            if nb > 7:  
                yBase += Constant.PILE_HEIGHT
                self.xMin = xBase + (self.pileNb - 8) * Constant.PILE_WIDTH

            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.CARD_HEIGHT + 2*Constant.CARD_OVERLAP

        elif self.type == Constant.BUFFERPILE:
            # Define where the pile is located
            xBase = Constant.BPILE_XBASE
            yBase = Constant.BPILE_YBASE
            self.xMin = xBase + (self.pileNb - Constant.INDEX_MIN_BP) * Constant.PILE_WIDTH

            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.CARD_HEIGHT + 2*Constant.CARD_OVERLAP

        elif self.type == Constant.FINALPILE:
            # Define where the pile is located
            xBase = Constant.FPILE_XBASE
            yBase = Constant.FPILE_YBASE
            self.xMin = xBase + (self.pileNb - Constant.INDEX_MIN_FP) * Constant.PILE_WIDTH

            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.CARD_HEIGHT + 2*Constant.CARD_OVERLAP
        else: return


    def isEmpty (self):
        return len (self.cards) == 0

    def isFull (self):
        maxCards = 3
        if self.type == Constant.FINALPILE :
            maxCards = 13
        return len (self.cards) == maxCards

    def updateTopCardId (self, id):
        if self.isEmpty() : return
        self.cards[-1].setImageId (id)

    def peekTopCard (self):
        if self.isEmpty() : return
        return self.cards[-1]

    def getTopCard (self):
        if self.isEmpty() : return None
        #c = self.cards[-1]
        return self.cards.pop ()
        #return c
    
    # Move top card from one pile to another but
    # do not check the validity of the move.
    def moveTopCard (self, toPile):
        if self.isEmpty() : return
        if toPile.isFull() : return
        #if self.type == Constant.FINALPILE : return
        #if toPile.isEmpty():
        #    print ("moveTopCard. Before move, top card pile", self.pileNb, "=", self.peekTopCard().name, "pile", toPile.pileNb, "is empty.")
        #else:    
        #    print ("moveTopCard. Before move, top card pile", self.pileNb, "=", self.peekTopCard().name, "top card pile", toPile.pileNb, "=", toPile.peekTopCard().name)
        c = self.getTopCard ()
        #print (c.name)
        c.pile = toPile
        toPile.addCard (c)        
        #if self.isEmpty():
        #    print ("moveTopCard. After move, pile", self.pileNb, "is empty.", "top card pile", toPile.pileNb, "=", toPile.peekTopCard().name)
        #else:    
        #    print ("moveTopCard. After move, top card pile", self.pileNb, "=", self.peekTopCard().name, "top card pile", toPile.pileNb, "=", toPile.peekTopCard().name)

    def __str__ (self):
        if self.pileNb < 0: return ""
        s = "Pile #: " + str (self.pileNb)
        if self.type == Constant.PLAYPILE : s += " PLAYPILE "
        elif self.type == Constant.BUFFERPILE : s += " BUFFERPILE "
        elif self.type == Constant.FINALPILE : s += " FINALPILE "
        s += " contains " + str(len (self.cards)) + " cards:"
        for c in self.cards:
            s += " " + c.name + " pile: " + str(c.pile) + " id: " + str (c.imageId)
        s += " xMin: " + str(self.xMin) + " xMax: " + str(self.xMax)
        s += " yMin: " + str(self.yMin) + " yMax: " + str(self.yMax)
        return s

    def addCard (self, c):
        if self.isFull() : return
        self.cards.append (c)
        c.setPile (self.pileNb)

    def getTopCardXY (self):
        if self.isEmpty() : return
        x = self.xMin
        if self.type == Constant.FINALPILE : 
            y = self.yMin
        else:
            y = self.yMin + (len (self.cards) - 1)* Constant.CARD_OVERLAP
        return x, y