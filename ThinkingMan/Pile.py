from tkinter import Canvas
from Card import Card
import Constant

class Pile():
    # canvas where to draw the pile
    # and startValue for the first card in final piles
    canvas = None
    startValue = None

    # index of the pile (ex: 0, 1, 2 for buffer piles)
    def __init__ (self, index):
        self.id = None      # Id in the canvas around the pile
        self.index = index
        self.cards = []     # Cards in the pile
        self.xMin = 0       # Coordinates on the canvas
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0

        # Make sure that class variable is set
        if Pile.canvas == None: return

        if index >= Constant.INDEX_MIN_PP and index <= Constant.INDEX_MAX_PP: 
            self.type = Constant.PLAYPILE
            index -= Constant.INDEX_MIN_PP  # To start with index = 0
            # Define where the pile is located
            xBase = Constant.PPILE_XBASE
            yBase = Constant.PPILE_YBASE
            self.xMin = xBase + index * (Constant.CARD_WIDTH + Constant.PILE_DELTA_X)

            # Second row for play pile
            index_2nd_row = Constant.PPILE_CNT // 2
            if index > index_2nd_row:  
                yBase += Constant.PILE_HEIGHT + Constant.PILE_DELTA_Y
                self.xMin = xBase + (index - index_2nd_row - 1) * (Constant.CARD_WIDTH + Constant.PILE_DELTA_X)
            
            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.PILE_HEIGHT

            # Create the drawing for the pile
            self.id = Pile.canvas.create_rectangle(self.xMin, self.yMin, self.xMax, self.yMax, fill="green", outline="white", tags=("pile", str(self.index)))

        elif index >= Constant.INDEX_MIN_BP and index <= Constant.INDEX_MAX_BP: 
            self.type = Constant.BUFFERPILE
            index -= Constant.INDEX_MIN_BP  # To start with index = 0
            # Define where the pile is located
            xBase = Constant.BPILE_XBASE
            yBase = Constant.BPILE_YBASE
            self.xMin = xBase + index * (Constant.CARD_WIDTH + Constant.PILE_DELTA_X)
            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.PILE_HEIGHT

            # Create the drawing for the pile
            self.id = Pile.canvas.create_rectangle(self.xMin, self.yMin, self.xMax, self.yMax, fill='burlywood', tags=("pile", str(self.index)))

        elif index >= Constant.INDEX_MIN_FP and index <= Constant.INDEX_MAX_FP: 
            self.type = Constant.FINALPILE
            index -= Constant.INDEX_MIN_FP  # To start with index = 0
            # Define where the pile is located
            xBase = Constant.FPILE_XBASE
            yBase = Constant.FPILE_YBASE
            self.xMin = xBase + index * (Constant.CARD_WIDTH + Constant.PILE_DELTA_X)
            self.xMax = self.xMin + Constant.CARD_WIDTH
            self.yMin = yBase
            self.yMax = self.yMin + Constant.CARD_HEIGHT

            # Create the drawing for the pile
            self.id = Pile.canvas.create_rectangle(self.xMin, self.yMin, self.xMax, self.yMax, fill='beige', tags=("pile", str(self.index)))
        else: return

    # Used when resizing the canvas
    def updateCoordinates (self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax

    # Adjust card coordinates to be exactly aligned within the pile
    def adjustCardCoordinates (self, c):
        if Pile.canvas == None: return

        # Change coordinates of the card: same xMin and xMax than the pile
        # yMin and yMax depend on the position of the card within the pile
        pile_height = self.yMax - self.yMin
        overlap = pile_height // 5
        card_height = 3 * overlap
        if self.type == Constant.FINALPILE:
            c.updateCoordinates (self.xMin, self.xMax, self.yMin, self.yMin + card_height)
        else:
            i = self.cards.index (c)
            c.updateCoordinates (self.xMin, self.xMax, self.yMin + i*overlap, self.yMin + i*overlap + card_height)

    # Add card to the pile
    def addCard (self, c):
        if self.isFull() : return
        self.cards.append (c)
        self.adjustCardCoordinates (c)

    def isEmpty (self):
        return len (self.cards) == 0

    def isFull (self):
        maxCards = 3
        if self.type == Constant.FINALPILE :
            maxCards = 13
        return len (self.cards) == maxCards

    def peekTopCard (self):
        if self.isEmpty() : return
        return self.cards[-1]

    # Peek at card rank r
    def peekCard (self, r):
        if self.isEmpty() : return
        if r > len(self.cards) : return None
        return self.cards[r]

    def getTopCard (self):
        if self.isEmpty() : return None
        return self.cards.pop ()
    
    # Move top card from one pile to another but
    # do not check the validity of the move.
    def moveTopCard (self, toPile):
        if self.isEmpty() : return
        if toPile.isFull() : return
        c = self.getTopCard ()
        toPile.addCard (c)        

    # Display starting value (valid only on final piles)
    def displayStartingValue (self, sv):
        if self.type != Constant.FINALPILE: return
        x = self.xMin + (self.xMax - self.xMin)//2
        y = self.yMin + (self.yMax - self.yMin)//2
        Pile.canvas.create_text(x, y, text=sv, fill="black", font=('Helvetica 15 bold'), tags="text")


    def __str__ (self):
        # Make sure that class variable is set
        if Pile.canvas == None: return
        s = "Pile #: " + str (self.index) + " id: " + str (self.id)
        if self.type == Constant.PLAYPILE : s += " PLAYPILE "
        elif self.type == Constant.BUFFERPILE : s += " BUFFERPILE "
        elif self.type == Constant.FINALPILE : s += " FINALPILE "
        xMin, yMin, xMax, yMax = Pile.canvas.bbox(self.id)
        s += "\n\t bbox:       "
        s += " xMin: " + str(xMin) + " xMax: " + str(xMax)
        s += " yMin: " + str(yMin) + " yMax: " + str(yMax)
        s += "\n\t coordinates:"
        s += " xMin: " + str(self.xMin) + " xMax: " + str(self.xMax)
        s += " yMin: " + str(self.yMin) + " yMax: " + str(self.yMax)
        s += "\n\t contains " + str(len (self.cards)) + " cards.\n"
        for c in self.cards:
            s += "\t" + c.__str__() + "\n"
        return s

    # Check if card c can be dropped on FINAL pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDrop (self, c):
        if self.type == Constant.FINALPILE: return self.checkDropFinal (c)
        elif self.type == Constant.BUFFERPILE: return self.checkDropBuffer (c)
        elif self.type == Constant.PLAYPILE: return self.checkDropPlay (c)
        # Unspecific
        return -99
        
    # Check if card c can be dropped on FINAL pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDropFinal (self, c):
        if self.type != Constant.FINALPILE: return -99
        # If pile is empty, c should have the starting value    
        if self.isEmpty():
            if c.val != Pile.startValue: return -1
        else: 
        # Card should have the same suit as any card in the pile            
            expectedSuit = self.peekTopCard().suit
            if c.suit != expectedSuit: return -2
            # Card should have value immediately above the top one 
            expectedValue = self.peekTopCard().valNum + 1
            if expectedValue > 13 : expectedValue = 1
            if c.valNum != expectedValue: return -3
        return 0

    # Check if card c can be dropped on PLAY pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDropPlay (self, c):
        if self.type != Constant.PLAYPILE: return -99
        # Pile should not be empty    
        if self.isEmpty(): return -10
        # Pile should not be full    
        if self.isFull(): return -11
        # Card should have different color than previous one            
        expectedColor = self.peekTopCard().color
        if c.color == expectedColor: return -12
        # Card should have value immediately less than previous one 
        expectedValue = self.peekTopCard().valNum - 1
        if expectedValue < 1 : expectedValue = 13
        if c.valNum != expectedValue: return -13
        return 0
        
    # Check if card c can be dropped on BUFFER pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDropBuffer (self, c):
        if self.type != Constant.BUFFERPILE: return -99
        # If pile is empty, no problem    
        if self.isEmpty(): return 0
        # Pile should not be full    
        if self.isFull(): return -11
        # Card should have different color than previous one            
        expectedColor = self.peekTopCard().color
        if c.color == expectedColor: return -12
        # Card should have value immediately less than previous one 
        expectedValue = self.peekTopCard().valNum - 1
        if expectedValue < 1 : expectedValue = 13
        if c.valNum != expectedValue: return -13
        return 0