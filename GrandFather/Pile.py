from tkinter import Canvas
from Card import Card
import Constant

class Pile():
    # canvas where to draw the pile
    # and startValue for the first card in final piles
    canvas = None

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
        if index == Constant.INDEX_MAX_PP:
            # Aces pile
            self.type = Constant.ACEPILE
            index = Constant.PPILE_COLUMNS -1
            row = Constant.PPILE_ROWS -1
            # Define where the pile is located
            self.xMin = Constant.PPILE_XBASE + index * (Constant.PILE_WIDTH + Constant.PILE_DELTA_X)
            self.xMax = self.xMin + Constant.CARD_WIDTH + 3 * Constant.CARD_OVERLAP
            self.yMin = Constant.PPILE_YBASE + row * (Constant.PILE_HEIGHT + Constant.PILE_DELTA_Y)
            self.yMax = self.yMin + Constant.PILE_HEIGHT
            # Create the drawing for the pile
            self.id = Pile.canvas.create_rectangle(self.xMin, self.yMin, self.xMax, self.yMax, fill="beige", outline="white", tags=("pile", str(self.index)))

            # Indicate ACE pile
            x = self.xMin + (self.xMax - self.xMin)//2
            y = self.yMin + (self.yMax - self.yMin)//2
            Pile.canvas.create_text(x, y, text="ACES", fill="black", font=('Helvetica 15 bold'), tags="text")
        else:
            row = index // Constant.PPILE_COLUMNS    
            self.type = Constant.PLAYPILE
            index = index % Constant.PPILE_COLUMNS
            # Define where the pile is located
            self.xMin = Constant.PPILE_XBASE + index * (Constant.PILE_WIDTH + Constant.PILE_DELTA_X)
            self.xMax = self.xMin + Constant.PILE_WIDTH
            self.yMin = Constant.PPILE_YBASE + row * (Constant.PILE_HEIGHT + Constant.PILE_DELTA_Y)
            self.yMax = self.yMin + Constant.PILE_HEIGHT
            # Create the drawing for the pile
            self.id = Pile.canvas.create_rectangle(self.xMin, self.yMin, self.xMax, self.yMax, fill="green", outline="white", tags=("pile", str(self.index)))



    # Used when resizing the canvas
    def updateCoordinates (self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax

    # Adjust card coordinates to be exactly aligned within the pile
    def adjustCardCoordinates (self, c):
        if Pile.canvas == None: return

        # Change coordinates of the card: same yMin and yMax than the pile
        # xMin and xMax depend on the position of the card within the pile
        pile_width = self.xMax - self.xMin
        overlap = pile_width // 5
        card_width = 3 * overlap
        i = self.cards.index (c)
        c.updateCoordinates (self.xMin + i*overlap, self.xMin + i*overlap + card_width, self.yMin, self.yMax)

    # Add card to the pile
    def addCard (self, c):
        if self.isFull() : return
        self.cards.append (c)
        self.adjustCardCoordinates (c)

    def isEmpty (self):
        return len (self.cards) == 0

    def isFull (self):
        maxCards = 3
        if self.type == Constant.ACEPILE :
            maxCards = 4
        return len (self.cards) == maxCards

    def isComplete (self):
        if self.type == Constant.ACEPILE :
            return len (self.cards) == 4
        else:
            if len (self.cards) != 3: return False
            colorCondition = self.cards[0].color == self.cards[2].color and \
                             self.cards[0].color != self.cards[1].color
            valueCondition = self.cards[0].valNum == self.cards[1].valNum - 1 and \
                             self.cards[1].valNum == self.cards[2].valNum - 1
            return colorCondition and valueCondition
        
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

    def __str__ (self):
        # Make sure that class variable is set
        if Pile.canvas == None: return
        s = "Pile #: " + str (self.index) + " id: " + str (self.id)
        if self.type == Constant.PLAYPILE : s += " PLAYPILE "
        elif self.type == Constant.ACEPILE : s += " ACEPILE "
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

    # Check if card c can be dropped on a pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDrop (self, c):
        if self.type == Constant.ACEPILE: 
            if c.val == "A": 
                return 0
            else:
                return -1
        elif self.type == Constant.PLAYPILE: return self.checkDropPlay (c)
        # Unspecific
        return -99
        
    # Check if card c can be dropped on PLAY pile.
    # Returns 0 if YES
    #         < 0 if NOT
    def checkDropPlay (self, c):
        if self.type != Constant.PLAYPILE: return -99
        # Pile empty is OK    
        if self.isEmpty(): return 0
        # Pile should not be full    
        if self.isFull(): return -11
        # Card should have different color than previous one            
        expectedColor = self.peekTopCard().color
        if c.color == expectedColor: return -12
        # Card should have value immediately above the previous one 
        expectedValue = self.peekTopCard().valNum + 1
        if c.valNum != expectedValue: return -13
        return 0
        