import tkinter as tk
from tkinter import Canvas, messagebox, Button
import copy
from PIL import Image
from PIL import ImageTk
from Deck import Deck
import Constant
from Pile import Pile

pile = []           # Piles of cards on the table
cardToMove = None   # Card to be moved
startValue = 0      # Start value on Final piles
firstTime = True
allMoves = []

def Solitaire ():
    root = tk.Tk()
    root.title('Thinking Man')
    iconp = Image.open (Constant.CARD_DIR + 'honors_spade-14.png')
    iconPhoto = ImageTk.PhotoImage(iconp)
    root.iconphoto (False, iconPhoto)
    root.geometry("1200x600")
    root.configure(background="green")
    root.resizable(False,False)

    deck = Deck()
    deck.shuffle()

    def dumpPile(title, index):
        global pile
        print (title + " Pile #" + str (index))
        for c in pile[index].cards:
            print ("\t", c.name, "[" + str(c.pile) + "]", "imageId:", c.imageId, end="")
        s = ""
        topCard = pile[index].getTopCard() 
        if not (topCard is None):
            name = topCard.name 
            s += "   Top card: " + topCard.name + " imageId: " + str (topCard.imageId)
        else:
            s += "   Top card is None"
        s += " xMin: " + str(pile[index].xMin) + " xMax: " + str(pile[index].xMax)
        s += " yMin: " + str(pile[index].yMin) + " yMax: " + str(pile[index].yMax)
        print (s)

    def dumpCanvas ():
        print ("Dump canvas:")
        for id in canvas.find_all():
            print ("\t", id, canvas.gettags(id), canvas.bbox (id))

    # Record move of card from pSrc to pDest
    def recordMove (pileSrc, pileDest):
        global allMoves
        allMoves.append ([pileSrc, pileDest])

    def undoMove ():
        global allMoves
        if len(allMoves) == 0: return
        oneMove = allMoves.pop()
        pSrc = oneMove[0]
        pDest = oneMove[1]
        # Card was move from pSrc to pDest and is now the top card of pDest
        print (pile[pDest].peekTopCard(), "was moved from pile:", pSrc, "to pile:", pDest)
        pile[pDest].moveTopCard(pile[pSrc])

        topCard = pile[pSrc].peekTopCard()
        newX, newY = pile[pSrc].getTopCardXY()
        print (topCard)
        moveCardImageTo (topCard, newX, newY)
        # The card should be forward others
        canvas.tag_raise(topCard.imageId)


    def getCardToMove (x, y):
        global pile
        for p in range (len(pile) + 1):
            if  pile[p].xMin <= x and pile[p].xMax >= x and \
                pile[p].yMin <= y and pile[p].yMax >= y :
                    return pile[p].peekTopCard()
        return None
    
    def moveCardImageTo (card, newX, newY):
        if card == None: return
        oldX1, oldY1, oldX2, oldY2 = canvas.bbox (card.imageId)
        dx = newX - oldX1
        dy = newY - oldY1
        canvas.move (card.imageId, dx, dy)

    # To drag, we identify what card is being moved, create a clone (cardToMove)
    # and hide the original card. This has to be done only once.
    # Then we move the image of cardToMove to where the mouse is located: e.x, e.y
    def drag (e):
        global cardToMove
        global firstTime
        if firstTime :
            topCard = getCardToMove (e.x, e.y)
            #print ("Click on ", topCard.name, "imageId:", topCard.imageId)
            cardToMove = copy.copy (topCard)
            canvas.itemconfigure(topCard.imageId, state='hidden')
            img = cardToMove.resizeImg()
            cardToMove.imageId = canvas.create_image (e.x, e.y, image=img, tags=('MOVING CARD', cardToMove.name))
            firstTime = False
        if cardToMove == None : return 
        moveCardImageTo (cardToMove, e.x, e.y)

    # If the drop is incorrect, the move is canceled.
    # Indicate (messagebox) to the user why the move is incorrect
    # then delete the clone (cardToMove) and its image
    # and reset the original card as visible
    def cancelMove(msg):
        messagebox.showerror("Solitaire", msg) 
        global cardToMove
        # Delete the image of the card moved
        canvas.delete (cardToMove.imageId)
        # Make the initial card visible again
        p = cardToMove.pile
        canvas.itemconfigure(pile[p].peekTopCard().imageId, state='normal')
        cardToMove = None

    # Returns true if all the final piles are full.
    def isWinner ():
        win = True
        for p in range (Constant.INDEX_MIN_FP, Constant.INDEX_MAX_FP+1):
            win = win and pile[p].isFull()
        return win
    
    # Drop the clone (cardToMove)
    def drop (event):
        global pile
        global cardToMove
        global firstTime
        firstTime = True
        found = False
        delta = 10
        if cardToMove == None: return
        # Identify the destination pile
        for p in range (len(pile)):
            if  pile[p].xMin - delta <= event.x and pile[p].xMax + delta >= event.x and \
                pile[p].yMin - delta <= event.y and pile[p].yMax + delta >= event.y :
                    found = True
                    break
        if not found: 
             cancelMove("Not a destination pile.")
             return
        else:
            #print ("Dropping cardToMove = ", cardToMove.name, " imageId = ", cardToMove.imageId)
            # For final piles
            if pile[p].type == Constant.FINALPILE:
                if pile[p].isEmpty() and cardToMove.val != startValue:
                    cancelMove ("Final pile starts with a " + str (startValue))
                    return
                if not pile[p].isEmpty():
                    topCard = pile[p].peekTopCard()
                    if cardToMove.color != topCard.color:
                        cancelMove ("Final piles should contain cards of the same color.")
                        return
                    expectedValue = topCard.valNum + 1
                    if topCard.valNum == 13 : expectedValue = 1
                    if cardToMove.valNum != expectedValue:
                        cancelMove ("Final piles should contain cards in ascending order.")
                        return
            else:
            # For play or buffer piles
                if pile[p].isEmpty() and pile[p].type == Constant.PLAYPILE:
                    cancelMove("Empty space can't be used on the play ground.")
                    return
                if pile[p].isFull():
                    cancelMove("Destination pile is full.")
                    return
                # Buffer file can be empty but not play piles
                if not pile[p].isEmpty():
                    topCard = pile[p].peekTopCard()
                    if topCard.color == cardToMove.color:
                        cancelMove("Color should alternate.")
                        return
                    expectedValNum = topCard.valNum - 1
                    if topCard.valNum == 1 : expectedValNum = 13
                    tmpList = ["A","2", "3","4","5","6","7","8","9","10","J","Q","K"]
                    expected = tmpList [expectedValNum-1]
                    if cardToMove.valNum != expectedValNum:
                        cancelMove("Value should be a " + expected)
                        return

            # At this point, we can accept the move
            oldPileNb = cardToMove.pile
            pile[oldPileNb].moveTopCard (pile[p])
            recordMove (oldPileNb, p)
            # The card should be forward others
            canvas.tag_raise(pile[p].peekTopCard().imageId)
            # Restore visibility
            canvas.itemconfigure(pile[p].peekTopCard().imageId, state='normal')
            # We don't need cardToMove image any more 
            canvas.delete (cardToMove.imageId)

            # Card moved is now at the top of pile[p]
            topCard = pile[p].peekTopCard()
            newX, newY = pile[p].getTopCardXY()
            #print ("Dropping ", topCard.name, "id:", topCard.imageId, " on pile ", p, " at x=", newX, " y=", newY)
            #dumpCanvas()
            moveCardImageTo (topCard, newX, newY)
            cardToMove = None

            # Check for win
            if pile[p].type == Constant.FINALPILE and isWinner():
                messagebox.showinfo ("Solitaire", "You won!") 

    def resetGame ():
        # No piles created => nothing to do
        if len(pile) == 0: return
        # Erase images and empty piles
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_FP+1):
            while not pile[p].isEmpty():
                c = pile[p].getTopCard()
                canvas.delete (c.imageId)
        deck.reset()
        deck.shuffle()

    def deal ():
        global pile
        global startValue
        resetGame()
        # Create play piles with 3 cards in each one
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP+1):
            pile.append (Pile (p))
            for cardCnt in range (3):
                c = deck.draw()
                pile[p].addCard (c)
                # display the card added
                x, y = pile[p].getTopCardXY()
                id = canvas.create_image (x, y, anchor='nw', image=c.image, tags=(c.name))
                pile[p].updateTopCardId (id)
            #print (pile[p])

        # Create 3 buffer piles with 2 cards in each one
        for p in range (Constant.INDEX_MIN_BP, Constant.INDEX_MAX_BP+1):
            pile.append (Pile (p))
            for cardCnt in range (2):
                c = deck.draw()
                pile[p].addCard (c)
                # display the card added
                x, y = pile[p].getTopCardXY()
                id = canvas.create_image (x, y, anchor='nw', image=c.image, tags=(c.name))
                pile[p].updateTopCardId (id)
            #print (pile[p])

        # Create the first final pile with one card showing
        pile.append (Pile (Constant.INDEX_MIN_FP))
        c = deck.draw()
        pile[Constant.INDEX_MIN_FP].addCard (c)
        # display the card added
        x, y = pile[Constant.INDEX_MIN_FP].getTopCardXY()
        id = canvas.create_image (x, y, anchor='nw', image=c.image, tags=(c.name))
        pile[Constant.INDEX_MIN_FP].updateTopCardId (id)
        startValue = c.val

        # Create remaining final piles with no cards in each one
        for p in range (Constant.INDEX_MIN_FP+1, Constant.INDEX_MAX_FP+1):
            pile.append (Pile (p))

        root.update_idletasks()
        root.update()

    canvas = Canvas (root, width=13*Constant.PILE_WIDTH, height=3*Constant.PILE_HEIGHT, background="green")
    canvas.place (x=0,y=0, anchor='nw')

    # Place a rectangle around each buffer pile
    x = Constant.BPILE_XBASE
    y = Constant.BPILE_YBASE
    width = Constant.CARD_WIDTH
    height = Constant.CARD_HEIGHT + 2*Constant.CARD_OVERLAP
    canvas.create_rectangle(x, y, x+width, y+height, fill='burlywood')
    x += Constant.PILE_WIDTH
    canvas.create_rectangle(x, y, x+width, y+height, fill='burlywood')
    x += Constant.PILE_WIDTH
    canvas.create_rectangle(x, y, x+width, y+height, fill='burlywood')
    x += Constant.PILE_WIDTH

    # Place a rectangle around each final pile
    x = Constant.FPILE_XBASE
    y = Constant.FPILE_YBASE
    width = Constant.CARD_WIDTH
    height = Constant.CARD_HEIGHT
    canvas.create_rectangle(x, y, x+width, y+height, fill='beige')
    x += Constant.PILE_WIDTH
    canvas.create_rectangle(x, y, x+width, y+height, fill='beige')
    x += Constant.PILE_WIDTH
    canvas.create_rectangle(x, y, x+width, y+height, fill='beige')
    x += Constant.PILE_WIDTH
    canvas.create_rectangle(x, y, x+width, y+height, fill='beige')

    btn1 = Button (canvas, text="Deal random", bd=10, bg="white", font=("Arial", 14), height=1, width=10, command=deal)
    x1 = Constant.FPILE_XBASE + 7*Constant.CARD_WIDTH
    y1 = Constant.FPILE_YBASE + Constant.CARD_OVERLAP
    btn1.place (x=x1, y=y1)
    btn2 = Button (canvas, text="Undo", bd=10, bg="white", font=("Arial", 14), height=1, width=10, command=undoMove)
    x2 = Constant.FPILE_XBASE + 7*Constant.CARD_WIDTH
    y2 = Constant.FPILE_YBASE - Constant.CARD_OVERLAP
    btn2.place (x=x2, y=y2)

    canvas.bind ("<B1-Motion>", drag)
    canvas.bind ("<ButtonRelease-1>", drop)

    root.mainloop()

Solitaire()
