# Type of piles
PLAYPILE = 1
BUFFERPILE = 2
FINALPILE = 3

# Piles characteristics used for placement
PILE_WIDTH = 80
PILE_HEIGHT = 200
PILE_DELTA_X = 20                               # Separation between piles
PILE_DELTA_Y = 10                               # Separation between piles
PPILE_CNT = 15                                  # Play piles
PPILE_XBASE = 10                                # First one is at (10, 10)
PPILE_YBASE = 10
BPILE_CNT = 3                                   # Buffer piles
BPILE_XBASE = (PPILE_CNT // 2 + 1) * (PILE_WIDTH + PILE_DELTA_X) + PILE_WIDTH
BPILE_YBASE = 10
FPILE_CNT = 4                                   # Final piles
FPILE_XBASE = 10 + 4 * PILE_WIDTH
FPILE_YBASE = 50 + 2 * PILE_HEIGHT

# Card images:
CARD_DIR = "../CardImages/"
CARD_WIDTH = PILE_WIDTH                         # 80
CARD_OVERLAP = PILE_HEIGHT // 5                 # 40
CARD_HEIGHT = 3 * CARD_OVERLAP                  # 120

# Index value (min, max) for each type of pile
INDEX_MIN_PP = 0                                # 0
INDEX_MAX_PP = PPILE_CNT -1                     # 14
INDEX_MIN_BP = INDEX_MAX_PP + 1                 # 15
INDEX_MAX_BP = INDEX_MIN_BP + BPILE_CNT - 1     # 17
INDEX_MIN_FP = INDEX_MAX_BP + 1                 # 18
INDEX_MAX_FP = INDEX_MIN_FP + FPILE_CNT - 1     # 21

# Canvas initial size
CANVAS_WIDTH = PPILE_CNT * CARD_WIDTH
CANVAS_HEIGHT = 3 * PILE_HEIGHT


