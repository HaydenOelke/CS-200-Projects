"""Boggler:  Boggle game solver. CS 210, Fall 2023.
Hayden Oelke
Credits:
"""
import doctest
import config
import sys
import board_view


GRAPHIC_VIEW = True
TEXT_VIEW = True 
TEXT_VIEW_EACH_MOVE = False
TEXT_VIEW_EACH_BACK = False
TEXT_VIEW_EACH_MOVE = True
DICT_PATH = "data/dict.txt"

def read_dict(path: str) -> list[str]:
    """Returns ordered list of valid, normalized words from dictionary.

    >>> read_dict("data/shortdict.txt")
    ['ALPHA', 'BED', 'BETA', 'DELTA', 'GAMMA', 'OMEGA']
    """
    words = []
    with open(path, 'r') as file:
        for line in file:
            word = line.strip()
            if allowed(word):
                words.append(normalize(word))
    return sorted(words)

def allowed(s: str) -> bool:
    """Is s a legal Boggle word?

    >>> allowed("am")  ## Too short
    False

    >>> allowed("de novo")  ## Non-alphabetic
    False

    >>> allowed("about-face")  ## Non-alphabetic
    False
    """
    if len(s) < config.MIN_WORD:
        return False
    return s.isalpha()


def normalize(s: str) -> str:
    """Canonical for strings in dictionary or on board
    >>> normalize("filter")
    'FILTER'
    """
    return s.upper()

# Possible search outcomes
NOPE = "Nope"       # Not a match, nor a prefix of a match
MATCH = "Match"     # Exact match to a valid word
PREFIX = "Prefix"   # Not an exact match, but a prefix (keep searching!)


def search(candidate: str, word_list: list[str]) -> str:
    """Determine whether candidate is a MATCH, a PREFIX of a match, or a big NOPE
    Note word list MUST be in sorted order.

    >>> search("ALPHA", ['ALPHA', 'BETA', 'GAMMA']) == MATCH
    True

    >>> search("BE", ['ALPHA', 'BETA', 'GAMMA']) == PREFIX
    True

    >>> search("FOX", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True

    >>> search("ZZZZ", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True
    """
    low = 0
    high = len(word_list) - 1
    NOPE = "Nope"
    MATCH = "Match"
    PREFIX = "Prefix"

    while low <= high: 
        mid = (low + high) // 2
        mid_word = word_list[mid]
        if mid_word == candidate:
            return MATCH
        elif mid_word < candidate:
            low = mid + 1
        else: 
            high = mid -1

    if low < len(word_list) and word_list[low].startswith(candidate):
        return PREFIX
    return NOPE


def test_it():
    """A little extra work to keep text display from
    interfering with doctests.
    """
    saved_flag = config.TEXT_VIEW
    config.TEXT_VIEW = True 
    doctest.testmod(verbose=True)
    config.TEXT_VIEW = saved_flag


def get_board_letters() -> str:
    """Get a valid string to form a Boggle board
    from the user.  May produce diagnostic
    output and quit.
    """
    while True:
        board_string = input("Boggle board letters (or 'return' to exit)> ")
        if allowed(board_string) and len(board_string) == config.BOARD_SIZE:
            return board_string
        elif len(board_string) == 0:
            print(f"OK, sorry it didn't work out")
            sys.exit(0)
        else:
            print(f'"{board_string}" is not a valid Boggle board')
            print(f'Please enter exactly {config.BOARD_SIZE} letters (or empty to quit)')
    return normalize(board_string)
    
def unpack_board(letters: str, rows=config.N_ROWS) -> list[list[str]]:
    """Unpack a single string of characters into
    a square matrix of individual characters, N_ROWS x N_ROWS.

    >>> unpack_board("abcdefghi", rows=3)
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]

    >>> unpack_board("abcdefghijklmnop", rows=4)
    [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
    """
    board = []
    for i in range(rows):
        row = list(letters[i * rows: (i + 1) * rows])
        board.append(row)
    return board

def boggle_solve(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all the words that can be made by traversing
    the boggle board in all 8 directions.  Returns sorted list without
    duplicates.

    >>> board = unpack_board("PLXXMEXXXAXXSXXX", rows=4)
    >>> words = read_dict("data/dict.txt")
    >>> boggle_solve(board, words)
    ['AMP', 'AMPLE', 'AXE', 'AXLE', 'ELM', 'EXAM', 'LEA', 'MAX', 'PEA', 'PLEA', 'SAME', 'SAMPLE', 'SAX']
    """

    in_use = "@"
    solutions = []

    def solve(row: int, col: int, prefix: str):
        """One solution step"""
        if row < 0 or col < 0 or row >= config.N_ROWS or col >= config.N_COLS:
            return
        if board[row][col] == in_use:
            return 
        
        letter = board[row][col]
        prefix = prefix + letter
        if search(prefix,words) == "NOPE":
            return
        
        board[row][col] = in_use
        board_view.mark_occupied(row, col)

        status = search(prefix, words)
        if status == "MATCH": 
            solutions.append(prefix)
            board_view.celebrate(prefix)
        if status == MATCH or status == PREFIX:

            for d_row in [0,-1,1]:
                for d_col in [0,-1,1]:
                    solve(row + d_row, col + d_col, prefix)

        board[row][col] = letter
        board_view.mark_unoccupied(row, col)

    for row_i in range(config.N_ROWS):
        for col_i in range(config.N_COLS):
            solve(row_i, col_i, "")

    solutions = list(set(solutions))
    return sorted(solutions)

POINTS = [0, 0, 0, 1, 1, 2, 3, 5, 11,
          11, 11, 11, 11, 11, 11, 11, 11 ]



def word_score(word: str) -> int:
    """Standard point value in Boggle"""
    assert len(word) <= 16
    return POINTS[len(word)]


def score(solutions: list[str]) -> int:
    """Sum of scores for each solution

    >>> score(["ALPHA", "BETA", "ABSENTMINDED"])
    14
    """
    player_score = 0 
    for word in solutions: 
        POINT_VALUE = word_score(word)
        player_score += POINT_VALUE

    return player_score

def main():
    words = read_dict(config.DICT_PATH)
    board_string = get_board_letters()
    board_string = normalize(board_string)
    board = unpack_board(board_string)
    board_view.display(board)
    board_view.prompt_to_close()
    solutions = boggle_solve(board, words)
    print(solutions)
    print(f"{score(solutions)} points")


if __name__ == "__main__":
    test_it()
    main()
