import csv

import unicodedata

file_write = csv.writer(open('../data/anime.csv', newline='', encoding='utf-8', mode='w'))
with open('../old/anime_parse.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    for string_old in reader:
        string_old[3] = string_old[3].replace('&#039;', "'").encode('ascii', 'ignore').decode()
        file_write.writerow(string_old)
