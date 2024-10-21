"""A bag of letters for finding anagrams.
Associates a cardinality (count) with each character
in the bag.
Author: Hayden Oelke
Date: 01/20/2024
Credits: 
"""


def normalize(phrase: str) -> list[str]:
    """Normalize word or phrase to the
    sequence of letters we will try to match, discarding
    anything else, such as blanks and apostrophes.
    Return as a list of individual letters.
    """
    return [char.lower() for char in phrase if char.isalpha()]


class LetterBag:
    """A bag (also known as a multiset) is
    a map from keys to non-negative integers.
    A LetterBag is a bag of single character
    strings.
    """
    def __init__(self, word=""):
        """Create a LetterBag"""
        self.word = word.strip()
        normal = normalize(self.word)
        self.length = len(normal)  # Counts letters only!

        #loop that counts and adds letters to letters dict 
        #empty dict 
        self.letters = {} 
        #iterate for letter in the normalize word 
        for letter in normal : 
            self.letters[letter] = self.letters.get(letter,0) + 1 

    def __len__(self):
        return self.length

    def __str__(self):
        return self.word

    def __repr__(self):
        counts = [f"{ch}:{n}" for ch, n in self.letters.items() if n > 0]
        return f'LetterBag({self.word}/[{", ".join(counts)}])'
        
    def contains(self, other: "LetterBag") -> bool:
        """Determine whether enough of each letter in
        other LetterBag are contained in this LetterBag.
        """
        for letter, count in other.letters.items():
            if letter not in self.letters or self.letters[letter] < count: 
                return False
        return True 

    def copy(self) -> "LetterBag":
        """Make a copy before mutating."""
        copy_ = LetterBag()
        copy_.word = self.word
        copy_.letters = self.letters.copy()  # Copied to avoid aliasing
        copy_.length = self.length
        return copy_
    
    def take(self, other: "LetterBag") -> "LetterBag":
        """Return a LetterBag after removing
        the letters in other.  Raises exception
        if any letters are not present.
        """
        bag = self.copy()

        for letter, count in other.letters.items():
            bag.letters[letter] -= count
            assert bag.letters[letter] >= 0
        bag.length -= other.length
                                
        return bag
