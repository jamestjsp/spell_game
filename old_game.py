import random
from  w_list import nw_list
import time

def chek_spelling(w, your_spelling):
    if w.lower() == your_spelling.lower():
        return True
    else:
        return False
result = True
accuracy = 0
ws_tried = 0
attempts = 0
try_count = 0
w = ''
while True:
    if result == True:
        try_count = 0
        w = random.choice(nw_list)
        print('Try', w.upper())
        your_spelling = input('input your word: ')
        if your_spelling.lower() != 'exit':
            ws_tried += 1
            attempts += 1
            result = chek_spelling(w, your_spelling)
        else:
            break

    elif result == True:
        continue
    else:
        your_spelling = input('Try again: ')
        if your_spelling.lower() != 'exit':
            try_count += 1
            attempts += 1
            result = chek_spelling(w, your_spelling)
        else:
            break

        if try_count > 4:
            result = True
            print('Try', w.upper(), 'later.')


if attempts == 0:
    accuracy = 0
else:
    accuracy = ws_tried/attempts*100

print('Thank you, your accuracy was', accuracy,'percentage.')