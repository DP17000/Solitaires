import tkinter as tk
from tkinter import Canvas, messagebox, Button
import time
from PIL import Image
from PIL import ImageTk
from Deck import Deck
import Constant
from Pile import Pile
from Card import Card

pile = []           # Piles of cards on the table
cardToMove = None   # Card to be moved
#startValue = 0      # Start value on Final piles
pileSrc = None      # Source pile when moving a card
allMoves = []       # Records all moves made by used (needed for undo!)
resizeTime = time.time()

def Solitaire ():
    # Set up the graphical root
    root = tk.Tk()
    root.title('Thinking Man')
    iconp = Image.open (Constant.CARD_DIR + 'honors_spade-14.png')
    iconPhoto = ImageTk.PhotoImage(iconp)
    root.iconphoto (False, iconPhoto)
    root.geometry(f"{Constant.CANVAS_WIDTH}x{Constant.CANVAS_HEIGHT}")
    root.configure(background="green")

    deck = Deck()

    def dumpCanvas ():
        print ("Dump canvas:")
        for id in canvas.find_all():
            print ("\t", id, canvas.gettags(id), canvas.bbox (id))

    # Not implemented yet
    def resizeCanvas (e):
        global resizeTime
        curr_time = time.time()
        if (curr_time - resizeTime) < 1:
            resizeTime = curr_time
            return
        w, h = canvas.winfo_width(), canvas.winfo_height()
        print ("Canvas size:", w, "x", h)
        wratio = float (e.width / w)
        hratio = float (e.height / h)
        # resize canvas
        canvas.config (width = w, height = h)
        resizeTime = curr_time

    # Record move of card from pile pSrc to pile pDest
    def recordMove (pileSrc, pileDest):
        global allMoves
        allMoves.append ([pileSrc, pileDest])

    # Undo the last move recorded
    def undoMove ():
        global allMoves
        if len(allMoves) == 0: return

        # Get last move made (source pile and dest pile)
        pSrc, pDest = allMoves.pop()

        # Card was move from pSrc to pDest and is now the top card of pDest
        # Move the card back to the source pile
        pile[pDest].moveTopCard(pile[pSrc])

        # Move the image at the right place
        topCard = pile[pSrc].peekTopCard()
        topCard.adjustImageLocation()

        # The card should be forward others in display list
        canvas.tag_raise(topCard.id)

    # Find the pile that overlap the cursor (x, y)
    # Give it a little meat to accept close by 
    def getPileAt (x, y):
        meat = 20
        allWidgets = canvas.find_overlapping (x, y, x+meat, y+meat)
        for w in allWidgets:
            tags = canvas.gettags(w)
            if tags[0] == "pile":
                return int (tags[1])
        return None
    
    def click_handler (e):
        global cardToMove, pileSrc
        pileSrc = getPileAt (e.x, e.y)
        if pileSrc == None:
            cancelImageMove ("You must click on a card to move it.")
            return
        cardToMove = pile[pileSrc].peekTopCard ()
        canvas.focus (cardToMove.id)

    # The card to move has been identified during click_handler.
    # We only need to get its current position and move it
    # to the current position of the mouse is located: e.x, e.y
    def dragImage (e):
        global firstTime, cardToMove
        if cardToMove == None: return
        xMin, yMin, xMax, yMax = canvas.bbox (cardToMove.id)
        dx = e.x - xMin
        dy = e.y - yMin
        cardToMove.moveImageTo (dx, dy)
        cardToMove.raiseImage()

    # If the drop is incorrect, the move is canceled.
    # Indicate (messagebox) to the user why the move is incorrect
    # then move the image of the card back to its initial position.
    def cancelImageMove(msg):
        global cardToMove, pileSrc
        if len(msg) > 0: messagebox.showerror("Solitaire", msg) 
        if cardToMove == None: return

        # Coordinates have not been updated yet. We only need
        # to restore the image
        cardToMove.adjustImageLocation()

        cardToMove = None
        pileSrc = None

    # Returns true if all the final piles are full.
    def isWinner ():
        win = True
        for p in range (Constant.INDEX_MIN_FP, Constant.INDEX_MAX_FP+1):
            win = win and pile[p].isFull()
        return win

    # Verify we drop at an acceptable location and update both card location and image.
    def drop (e):
        global pile, pileSrc, cardToMove
        if cardToMove == None: return
        # Identify the destination pile
        p = getPileAt (e.x, e.y)
        if p == None: 
            cancelImageMove ("You can only drop a card on a pile.")
            return
        if p == pileSrc:
        # Drop on the same pile it came from. Cancel the move but no error message.
            cancelImageMove ("")
            return
        
        check = pile[p].checkDrop (cardToMove)

        if check == -1:
            cancelImageMove ("Wrong value for first card on final pile.")
            return
        if check == -2:
            cancelImageMove ("Final piles contain cards of the same suit.")
            return
        if check == -3:
            cancelImageMove ("Final piles are sorted in ascending order.")
            return
        if check == -10:
            cancelImageMove ("Empty play piles can't be reused.")
            return
        if check == -11:
            cancelImageMove ("Pile is full.")
            return
        if check == -12:
            cancelImageMove ("Colors should alternate.")
            return
        if check == -13:
            cancelImageMove ("Values should decrease.")
            return
        if check == -99:
            cancelImageMove ("Unspecific error!")
            return


        # At this point, we can accept the move
        pile[pileSrc].moveTopCard (pile[p])
        recordMove (pileSrc, p)
        # Make sure the image is well positioned
        cardToMove.adjustImageLocation()

        # Check for win
        if pile[p].type == Constant.FINALPILE and isWinner():
            messagebox.showinfo ("Solitaire", "You won!") 
        
        # Prepare for next user action
        cardToMove = None
        pileSrc = None

    # Prepare for a new games
    def resetGame ():
        # No piles created => nothing to do
        if len(pile) == 0: return
        # Empty piles
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_FP+1):
            pile[p].cards.clear()

        deck.reset()
        deck.shuffle()
        # Move card images out of the way
        for i in range (deck.remainCnt()):
            c = deck.peekAtRank (i)
            c.updateCoordinates (1000, 1000, 1000, 1000)
            c.adjustImageLocation()

        # Delete the starting value in final piles
        canvas.delete ("text")

    # Deal each card from the deck into the different piles
    # display the images and get the startValue
    def deal ():
        global startValue
        resetGame()
        # Populate play piles with 3 cards in each one
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP+1):
            for cardCnt in range (3):
                c = deck.draw()
                pile[p].addCard (c)
                c.adjustImageLocation()
                c.raiseImage()

        # Populate 3 buffer piles with 2 cards in each one
        for p in range (Constant.INDEX_MIN_BP, Constant.INDEX_MAX_BP+1):
            for cardCnt in range (2):
                c = deck.draw()
                pile[p].addCard (c)
                c.adjustImageLocation()
                c.raiseImage()

        # Populate the first final pile with one card showing
        c = deck.draw()
        p = Constant.INDEX_MIN_FP
        pile[p].addCard (c)
        c.adjustImageLocation()
        c.raiseImage()

        Pile.startValue = c.val
        for p in range (Constant.INDEX_MIN_FP+1, Constant.INDEX_MAX_FP+1):
            pile[p].displayStartingValue (c.val)

        root.update_idletasks()
        root.update()


    # Create the user interface
    canvas = Canvas (root, width=Constant.CANVAS_WIDTH, height=Constant.CANVAS_HEIGHT, background="green")
    canvas.place (x=0,y=0, anchor='nw')
    Card.canvas = canvas
    Pile.canvas = canvas
    w, h = canvas.winfo_width(), canvas.winfo_height()
    id = canvas.create_rectangle(0, 0, w-1, h-1,outline="white")

    # Create the piles
    for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_FP+1):
        pile.append (Pile (p))

    # Add buttons
    btn1 = Button (canvas, text="Deal random", bd=10, bg="white", font=("Arial", 14), height=1, width=10, command=deal)
    canvas.addtag_withtag (btn1, "button")
    x1 = Constant.FPILE_XBASE + (Constant.PPILE_CNT // 2 + 1) * Constant.CARD_WIDTH
    y1 = Constant.FPILE_YBASE - Constant.CARD_OVERLAP
    btn1.place (x=x1, y=y1)
    btn2 = Button (canvas, text="Undo", bd=10, bg="white", font=("Arial", 14), height=1, width=10, command=undoMove)
    canvas.addtag_withtag (btn2, "button")
    x2 = Constant.FPILE_XBASE + (Constant.PPILE_CNT // 2 + 1) * Constant.CARD_WIDTH
    y2 = Constant.FPILE_YBASE + Constant.CARD_OVERLAP
    btn2.place (x=x2, y=y2)

    canvas.bind ("<Button-1>", click_handler)
    canvas.bind ("<B1-Motion>", dragImage)
    canvas.bind ("<ButtonRelease-1>", drop)
    #canvas.bind ("<Configure>", resizeCanvas)

    root.mainloop()

Solitaire()
