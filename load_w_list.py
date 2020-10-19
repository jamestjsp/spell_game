from spell_game import add_nw2db, lod_db, write_db
db = lod_db()
with open('n_words.txt', 'r') as f:
    lines = f.readlines()
nw_list = [line.strip() for line in lines]
add_nw2db(db, nw_list)
write_db(db)