#Is this kind of like pseudocode? 
import random

def check_guess(box_guess:str, correct_guess:int, box_to_group:dict[str:int], seqs_in_box:dict[str:list[str]], seq:str):
    if box_guess in box_to_group:
        if correct_guess == box_to_group[box_guess]:
            seqs_in_box[box_guess].append(seq)
            return True
        else:
            return False
    elif not box_to_group:
        box_to_group[box_guess] = correct_guess
        seqs_in_box[box_guess].append(seq)
        return True
    elif correct_guess in box_to_group.values():
        return False
    else:
        box_to_group[box_guess] = correct_answer
        seqs_in_box[box_guess].append(seq)
        return True

file = "src/data/seqs_3.txt"
box_to_group: dict[str:int] = dict()
seqs_in_group: dict[int:list[str]] = {1:[], 2:[], 3:[], 4:[]}
seqs_in_box: dict[str:list[str]] = {'A':[], 'B':[], 'C':[], 'D':[]}
all_seqs = []

current_group = 0


with open(file, 'r') as f:
    for line in f:
        words = line.split()
        print(words[0])
        if words[0] == 'GROUP':
            current_group = int(words[1])
        elif current_group != 0:
            seqs_in_group[current_group].append(words[0])
            all_seqs.append(words[0])

points = 0
n_seqs = len(all_seqs)
reverse_lookup = {s: k for k, lst in seqs_in_group.items() for s in lst}

seq = random.choice(all_seqs)
all_seqs.remove(seq)

for i in range(n_seqs):
    correct_answer = reverse_lookup[seq]
    print(f'You have {points} points. This is what your boxes are looking like:')
    print(seqs_in_box)
    print(seq)
    box_guess = input('Which box does the sequence belong to?')
    if check_guess(box_guess, correct_answer, box_to_group, seqs_in_box, seq):
        print('Congrats! That is correct')
        points += 10
        if len(all_seqs) != 0:
            seq = random.choice(all_seqs)
            all_seqs.remove(seq)
    else:
        print('Sorry! That is not correct. Try again :)')