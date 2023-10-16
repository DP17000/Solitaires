from PIL import Image
from PIL import ImageTk
import Constant

class Card():
    
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
        self.name = val + suit
        self.fileName = Constant.CARD_DIR + self.name + ".png"
        self.color = ""
        self.pile = None
        self.imageId = None
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

        self.image = self.resizeImg()

    def __str__ (self):

        return self.name + " " + self.color + " " + str(self.valNum)
        
    def resizeImg (self):
        card_img = Image.open (self.fileName)
        card_img_resized = card_img.resize ((Constant.CARD_WIDTH, Constant.CARD_HEIGHT),Image.Resampling.LANCZOS)
        global photoImg
        photoImg = ImageTk.PhotoImage (card_img_resized)
        return photoImg
    
    def setImageId (self, id):
        self.imageId = id

    def setPile (self, nb):
        self.pile = nb