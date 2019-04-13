"""This file is a copy from the file in which the class was defined (practice 1)"""

class Seq:
    """Class for working with sequences"""
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def complement(self):
        complement_str = ""
        for element in self.strbases:
            if element == "A":
                complement_str = complement_str + "T"
            elif element == "T":
                complement_str = complement_str + "A"
            elif element == "C":
                complement_str = complement_str + "G"
            elif element == "G":
                complement_str = complement_str + "C"
        complement = Seq(complement_str)
        return complement

    def reverse(self):
        reverse_str = self.strbases[::-1]
        reverse = Seq(reverse_str)
        return reverse

    def count(self, base):
        counter = (self.strbases).count(base)
        return counter

    def perc(self, base):
        tl = len(self.strbases)
        counter = self.strbases.count(base)
        perc = round((counter/tl) * 100,1)
        return perc