import json
import os
import csv
# delete the results.csv if exists
try:
    os.remove('results.csv')
except OSError:
    pass


# load db.json
with open('db.json', 'r') as db:
    db_dict = json.load(db)

to_learn = list()
my_spell_count = 0
for w in db_dict['p_stat']:
    w_stat = dict()
    e_count = 0
    p_count = 0
    for p_hist in db_dict['p_stat'][w]['p_hist']:
        try:
            e_count += db_dict['p_stat'][w]['p_hist'][p_hist]['e_count']
            p_count += db_dict['p_stat'][w]['p_hist'][p_hist]['p_count']
        except TypeError:
            pass
    if e_count > 1:
        w_stat['word'] = w
        w_stat['e_count'] = e_count
        w_stat['p_count'] = p_count
        if my_spell_count < len(db_dict['p_stat'][w]['my_e_spell']):
            my_spell_count = len(db_dict['p_stat'][w]['my_e_spell'])
            most_diff_word_idx = len(to_learn)
        for idx, e_word in enumerate(db_dict['p_stat'][w]['my_e_spell']):
            w_stat[f'my_spell_{idx+1}'] = e_word
        to_learn.append(w_stat)
# Writre results to results.csv
with open('results.csv', 'w', newline='') as csvfile:
    fieldnames = to_learn[most_diff_word_idx].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(to_learn)