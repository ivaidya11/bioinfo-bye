from enum import Enum

class Group(Enum):
    """
    Enumerator class of all available groups (4)
    """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

class SequenceBlock():
    """
    This class defines the sequence blocks.

    :attr sequence: DNA sequence that defines the block
    :type sequence: str
    :attr length: Length of the DNA sequence
    :type length: int
    :attr group: Group that the sequence belongs to (relative to each other)
    :type group: Group
    """

    sequence: str
    length: int
    group: Group

    def __init__(self, sequence: str, group: Group):
        """
        Initializes a Sequence block

        :param sequence: DNA sequence that defines the block
        :type sequence: str
        :param group: Group that the sequence belongs to (1-4)
        :type length: int
        """

        self.sequence = sequence
        self.length = len(sequence)
        self.group = group

    def getSequence(self) -> str:
        return self.sequence

    def getLength(self) -> int:
        return self.length

    def getGroup(self) -> int:
        return self.group

    def __eq__(self, other: SequenceBlock) -> bool:
        return self.group == other.group #This overrides the == operator., it checks the group rather than the sequence 