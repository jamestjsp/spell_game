import json
import time
import random
from gtts import gTTS
from playsound import playsound



def lod_db():
    '''
    A function to parse db.json file and returns a dict object.
    '''
    with open('db.json', 'r') as db:
        return json.load(db)


def add_nw2db(db, nw_list):
    w_list = list(db.get('p_stat').keys())
    w_template = db['p_stat']['word']
    for nw in nw_list:
        if nw.lower() not in w_list:
            tts = gTTS(nw)
            tts.save('audio/' + nw.lower() + '.mp3')
            db['p_stat'][nw.lower()] = w_template.copy()
            print('added', nw)
    print('Done!')


def write_db(db):
    timestr = time.strftime('%Y%m%d%H%M%S')
    with open('db_bkp\db_' + timestr + '.json', 'w') as f:
        json.dump(db, f)
    with open('db.json', 'w') as f:
        json.dump(db, f)   
def get_w_accracy(p_hist):
    p_count = 0
    e_count = 0
    w_accuracy = 0
    for attempt in p_hist:
        try:
            p_count += p_hist[attempt]['p_count']
            e_count += p_hist[attempt]['e_count']
        except TypeError:
            pass
        try:
            w_accuracy += p_count / (p_count + e_count) * 100
        except ZeroDivisionError:
            w_accuracy += 100
    try:
        avg_accuracy = w_accuracy / len(p_hist)
    except ZeroDivisionError:
        avg_accuracy = 100
    return avg_accuracy


def get_error_w(db, p):
    p_stat = db['p_stat']
    error_w_list = list()
    for w in p_stat:
        p_hist = p_stat[w]['p_hist']
        if w != 'word' and get_w_accracy(p_hist) < p:
            error_w_list.append(w)
    return error_w_list

def get_w_practice_count(p_hist):
    p_count = 0
    for attempt in p_hist:
        try:
            p_count += p_hist[attempt]['p_count']
        except TypeError:
            pass
    return p_count


def get_low_pw(db, p):
    p_stat = db['p_stat']
    low_pw_list = list()
    for w in p_stat:
        p_hist = p_stat[w]['p_hist']
        if w != 'word' and get_w_practice_count(p_hist) < p:
            low_pw_list.append(w)
    return low_pw_list

def chek_spelling(w, your_spelling):
    if w.lower() == your_spelling.lower():
        return True
    else:
        return False
def game(db):
    result = True
    try_count = 0
    p_count = 0
    e_count = 0
    new_pidx = len(db['g_stat']) + 1
    w_list = list(db.get('p_stat').keys())
    w_list.remove('word')
    w_count = 0
    if not w_list:
        enter_game = False
        print('word list is empty use load_w_list.py to add words to db')
    else:
        enter_game = True
    
    while enter_game:
        if result == True:
            w = random.choice(w_list)
            w_p_hist = db['p_stat'][w]['p_hist']
            w_count += 1
            print('-'*15, w_count, '-'*15, sep='')
            playsound('audio/' + w + '.mp3')
            your_spelling = input('input your word: ')
            if your_spelling.lower() != 'exit':
                while your_spelling.lower() == 'sm' or your_spelling.lower() == 'la':
                    if your_spelling.lower() == 'sm':
                        f_w ="_".join(w).upper()
                        print(f_w)
                        your_spelling = input('Try again: ')
                    if  your_spelling.lower() == 'la':
                        playsound('audio/' + w + '.mp3')
                        your_spelling = input('Try again: ')
                p_count += 1
                try_count = 1
                if len(w_p_hist) == 0:
                    idx = str(1)
                    w_p_hist[idx] = {'p_count':1}
                    w_p_hist[idx]['e_count'] = 0
                    w_p_hist[idx]['p_idx'] = new_pidx
                else:
                    last_p = w_p_hist[str(len(w_p_hist))]
                    w_p_idx = last_p['p_idx']
                    if w_p_idx != new_pidx:
                        idx = str(len(w_p_hist)+1)
                        w_p_hist[idx] = {'p_count':1}
                        w_p_hist[idx]['e_count'] = 0
                        w_p_hist[idx]['p_idx'] = new_pidx

                    else:
                        idx = str(len(w_p_hist))
                        w_p_hist[idx]['p_count'] += 1
                result = chek_spelling(w, your_spelling)
            else:
                break

        elif result == True:
            continue
        else:
            w_p_hist[idx]['e_count'] += 1
            e_count += 1
            my_e_spell = db['p_stat'][w]['my_e_spell']
            if your_spelling not in my_e_spell:
                my_e_spell.append(your_spelling)
            your_spelling = input('Try again: ')
            if your_spelling.lower() != 'exit':
                while your_spelling.lower() == 'sm' or your_spelling.lower() == 'la':
                    if your_spelling.lower() == 'sm':
                        f_w ="_".join(w).upper()
                        print(f_w)
                        your_spelling = input('Try again: ')
                    if your_spelling.lower() == 'la':
                        playsound('audio/' + w + '.mp3')
                        your_spelling = input('Try again: ')
                try_count += 1
                result = chek_spelling(w, your_spelling)                   
            else:
                break

            if try_count >= 3 and not result:
                e_count += 1
                result = True
                print('Try', w.upper(), 'later.')
    
    if w_list:
        if len(db['g_stat']) == 0:
            idx = str(1)
            db['g_stat'][idx] = {'p_count':p_count}
            db['g_stat'][idx]['e_count'] = e_count
        else:
            db['g_stat'][new_pidx] = {'p_count':p_count}
            db['g_stat'][new_pidx]['e_count'] = e_count
        write_db(db)
        accuracy = 100 * (1 - p_count/(p_count + e_count))
        print('Thank you, your accuracy was', accuracy,'percentage.')
    else:
        print('Bye!')
if __name__ == "__main__":
    db = lod_db()
    game(db)