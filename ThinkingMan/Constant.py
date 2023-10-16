#card images:
CARD_DIR = "../CardImages/"
CARD_WIDTH = 70
CARD_HEIGHT = 100
CARD_OVERLAP = 40

# Type of piles
PLAYPILE = 1
BUFFERPILE = 2
FINALPILE = 3

# Piles characteristics used for placement
PILE_WIDTH = 100
PILE_HEIGHT = 200
PPILE_CNT = 15
PPILE_XBASE = 10
PPILE_YBASE = 10
BPILE_XBASE = 10 + 9 * PILE_WIDTH
BPILE_YBASE = 50
FPILE_XBASE = 10 + 4 * PILE_WIDTH
FPILE_YBASE = 50 + 2 * PILE_HEIGHT

# Index value (min, max) for each type of pile
INDEX_MIN_PP = 0                    # 0
INDEX_MAX_PP = PPILE_CNT -1         # 14
INDEX_MIN_BP = INDEX_MAX_PP + 1     # 15
INDEX_MAX_BP = INDEX_MIN_BP + 2     # 17
INDEX_MIN_FP = INDEX_MAX_BP + 1     # 18
INDEX_MAX_FP = INDEX_MIN_FP + 3     # 21


