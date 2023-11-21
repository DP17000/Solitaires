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
pileSrc = None      # Source pile when moving a card
allMoves = []       # Records all moves made by user (needed for undo!)
resizeTime = time.time()

def Solitaire ():
    # Set up the graphical root
    root = tk.Tk()
    root.title('GrandFather')
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

    def double_click_handler (e):
        global cardToMove, pileSrc
        pileSrc = getPileAt (e.x, e.y)
        if pileSrc == None:
            cancelImageMove ("You can only double-click a card.")
            return
        cardToMove = pile[pileSrc].peekTopCard ()
        canvas.focus (cardToMove.id)
        if cardToMove.val == "A":
            # Move the ace to the ACEPILE
            pDest = Constant.INDEX_MAX_PP
            finalizeMove (pDest)
        else:
            # Find a possible pile where the card can be dropped
            for pDest in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP):
                if pile[pDest].checkDrop (cardToMove) >= 0:
                    finalizeMove (pDest)
                    break

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

    # Returns true if the game is won:
    def isWinner ():
        # The 4 aces are out
        win = pile[Constant.INDEX_MAX_PP].isComplete()
        # All other piles are either empty or have 3 following cards correct
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP):
            win = win and (pile[p].isComplete() or pile[p].isEmpty())
        return win

    # Verify we drop at an acceptable location and update both card location and image.
    def drop (e):
        global pile, pileSrc, cardToMove
        if cardToMove == None: return
        # Identify the destination pile
        pDest = getPileAt (e.x, e.y)
        if pDest == None: 
            cancelImageMove ("You can only drop a card on a pile.")
            return
        if pDest == pileSrc:
        # Drop on the same pile it came from. Cancel the move but no error message.
            cancelImageMove ("")
            return
        
        check = pile[pDest].checkDrop (cardToMove)

        if check == -1:
            cancelImageMove ("Only aces can go on this pile.")
            return
        if check == -11:
            cancelImageMove ("Pile is full.")
            return
        if check == -12:
            cancelImageMove ("Colors should alternate.")
            return
        if check == -13:
            cancelImageMove ("Values should increase.")
            return
        if check == -99:
            cancelImageMove ("Unspecific error!")
            return
        finalizeMove (pDest)

    # At this point, we can accept the move
    def finalizeMove (pDest):
        global pile, pileSrc, cardToMove

        pile[pileSrc].moveTopCard (pile[pDest])
        recordMove (pileSrc, pDest)
        # Make sure the image is well positioned
        cardToMove.adjustImageLocation()

        # Check for win
        if isWinner():
            messagebox.showinfo ("Solitaire", "You won!") 

        # Prepare for next user action
        cardToMove = None
        pileSrc = None

    # Prepare for a new games
    def resetGame ():
        # No piles created => nothing to do
        if len(pile) == 0: return
        # Empty all piles 
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP+1):
            pile[p].cards.clear()

        deck.reset()
        deck.shuffle()
        # Move card images out of the way
        for i in range (deck.remainCnt()):
            c = deck.peekAtRank (i)
            c.updateCoordinates (1000, 1000, 1000, 1000)
            c.adjustImageLocation()

    # Deal each card from the deck into the different piles
    # display the images
    def deal ():
        global startValue
        resetGame()
        # Populate play piles with 3 cards in each one except in the 2nd column 
        for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP):
            maxCards = 3
            if p % 4 == 1: maxCards = 2
            for cardCnt in range (maxCards):
                c = deck.draw()
                pile[p].addCard (c)
                c.adjustImageLocation()
                c.raiseImage()

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
    for p in range (Constant.INDEX_MIN_PP, Constant.INDEX_MAX_PP+1):
        pile.append (Pile (p))

    # Add buttons
    btn1 = Button (canvas, text="Deal", bd=10, bg="white", font=("Arial", 14), height=1, width=8, command=deal)
    canvas.addtag_withtag (btn1, "button")
    x1 = (Constant.PPILE_COLUMNS - 2) * (Constant.PILE_DELTA_X + Constant.PILE_WIDTH)
    y1 = Constant.PPILE_ROWS  * (Constant.PILE_DELTA_Y + Constant.PILE_HEIGHT) + 3 * Constant.PILE_DELTA_Y
    btn1.place (x=x1, y=y1)
    btn2 = Button (canvas, text="Undo", bd=10, bg="white", font=("Arial", 14), height=1, width=8, command=undoMove)
    canvas.addtag_withtag (btn2, "button")
    x2 = x1 + Constant.PILE_WIDTH + Constant.PILE_DELTA_X
    y2 = y1
    btn2.place (x=x2, y=y2)
    #btn3 = Button (canvas, text="Check", bd=10, bg="white", font=("Arial", 14), height=1, width=8, command=isWinner)
    #canvas.addtag_withtag (btn3, "button")
    #x3 = x2 + Constant.PILE_WIDTH + Constant.PILE_DELTA_X
    #y3 = y2
    #btn3.place (x=x3, y=y3)

    canvas.bind ("<Button-1>", click_handler)
    canvas.bind ("<Double-Button-1>", double_click_handler)
    canvas.bind ("<B1-Motion>", dragImage)
    canvas.bind ("<ButtonRelease-1>", drop)

    root.mainloop()

Solitaire()
