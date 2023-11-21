# Type of piles
PLAYPILE = 1
ACEPILE = 2

# Card images:
CARD_DIR = "../CardImages/"
CARD_HEIGHT = 120
CARD_WIDTH = 90
CARD_OVERLAP = 30

# Piles characteristics used for placement
PILE_WIDTH = CARD_WIDTH + 2 * CARD_OVERLAP
PILE_HEIGHT = CARD_HEIGHT
PILE_DELTA_X = 20                                   # Separation between piles
PILE_DELTA_Y = 10                                   # Separation between piles
PPILE_COLUMNS = 4                                   # 4 Piles per row
PPILE_ROWS = 5                                      # 5 rows
PPILE_CNT = PPILE_COLUMNS * PPILE_ROWS              # 20 piles - of 3 cards each = 60 cards
                                                    # But last pile is empty (57 cards)
                                                    # And 2nd column has only 2 cards (57 - 5 = 52)
PPILE_XBASE = 100                                   # First one is at (100, 10)
PPILE_YBASE = 10

# Index value (min, max) for each type of pile
INDEX_MIN_PP = 0                                # 0
INDEX_MAX_PP = PPILE_CNT -1                     # 19

# Canvas initial size
CANVAS_WIDTH = (1 + PPILE_COLUMNS) * (PILE_DELTA_X + PILE_WIDTH)
CANVAS_HEIGHT = (1 + PPILE_ROWS) * (PILE_DELTA_Y + PILE_HEIGHT)