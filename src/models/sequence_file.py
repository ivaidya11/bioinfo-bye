import random

class SequenceFile():
    def __init__(self, filename):
        self.filename=filename #When you create the object, you pass a filename.

    def get_sequence_dictionary(self): #This function reads the file and returns a dictionary of groups
        seqs: dict[int: set[str]] = dict()
        GROUP = 0

        with open(self.filename) as f:
            for line in f:
                if line[0] == 'GROUP':
                    GROUP = int(line[1])
                    seqs[GROUP] = {}
                elif line[0] == 'GRADE:':
                    pass
                else:
                    seqs[GROUP].add(line[0])

        return seqs

    def get_shuffled_list(self): #This method returns a random list of all sequences, ignoring groups
        list_seqs = []

        with open(self.filename) as f:
            for one_line in f:
                line = one_line.split()
                if line[0] == 'GROUP' or line[0] == 'GRADE:':
                    pass
                else:
                    list_seqs.append(line[0])
        random.shuffle(list_seqs)
        return list_seqs
