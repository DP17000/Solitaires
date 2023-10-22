from PIL import Image
from PIL import ImageTk
import Constant

class Card():
    # canvas where to draw the card defined as class variable
    canvas = None
    
    def __init__(self, val, suit):
        # Make sure that class variable is set
        if Card.canvas == None: return

        self.id = None
        self.val = val
        self.suit = suit
        self.name = val + suit
        self.fileName = Constant.CARD_DIR + self.name + ".png"
        self.color = ""
        # These should equal the values for the bbox of the
        # image when the image of the card is not moved !
        self.xMin = 0
        self.xMax = 0
        self.yMin = 0
        self.yMax = 0

        if val == "J":
            self.valNum = 11
        elif val == "Q":
            self.valNum = 12
        elif val == "K":
            self.valNum = 13
        elif val == "A":
            self.valNum = 1
        else:
            self.valNum = int (val)

        if suit == "D" or suit == "H" : self.color = "red"
        if suit == "C" or suit == "S": self.color = "black"

        self.photoImg = self.resizedImage (Constant.CARD_WIDTH, Constant.CARD_HEIGHT)

        # And publish the picture on the canvas at coordinates 0, 0
        self.id = Card.canvas.create_image (0, 0, anchor='nw', image=self.photoImg, tags=("card", self.name))

    def resizedImage (self, width, height):
        global photoImg                 # Needs to be global (bug in PhotoImage????)
        img = Image.open (self.fileName)
        img_resized = img.resize ((width, height),Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage (img_resized)

    # Moves the image up in the display list for overlays
    def raiseImage (self):
        # Make sure that class variable is set
        if Card.canvas == None: return
        Card.canvas.tag_raise(self.id)

    def dumpImage (self):
        # Make sure that class variable is set
        if Card.canvas == None: return
        dic = Card.canvas.itemconfigure (self.id)
        for x, y in dic.items():
            print (x, y)

    # Move the image to a specific location
    def moveImageTo(self, dx, dy):
        # Make sure that class variable is set
        if Card.canvas == None: return
        Card.canvas.move (self.id, dx, dy)

    # Move the image from its current location
    # To xMin, xMax, yMin, yMax
    def adjustImageLocation (self):
        # Make sure that class variable is set
        if Card.canvas == None: return
        xMin_curr, yMin_curr, xMax_curr, yMax_curr = Card.canvas.bbox (self.id)
        dx = self.xMin - xMin_curr
        dy = self.yMin - yMin_curr
        self.moveImageTo (dx, dy)

    def __str__ (self):
        s = "id: " + str(self.id) 
        s += " " + self.name + " " + self.color + " " + str(self.valNum)
        xMin, yMin, xMax, yMax = Card.canvas.bbox(self.id)
        s += "\n\t bbox:       "
        s += " xMin: " + str(xMin) + " xMax: " + str(xMax)
        s += " yMin: " + str(yMin) + " yMax: " + str(yMax)
        s += "\n\t coordinates:"
        s += " xMin: " + str(self.xMin) + " xMax: " + str(self.xMax)
        s += " yMin: " + str(self.yMin) + " yMax: " + str(self.yMax)
        return s
        
    # Set coordinates
    def updateCoordinates (self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
