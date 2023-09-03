import csv

with open('anime.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    banned = []
    animeList = csv.writer(open('animeList.csv', newline='', encoding='utf-8', mode='a+'))
    for row in reader:
        if not 'hentai' in row[2].lower() and not 'yuri' in row[2].lower() and not 'yaoi' in row[2].lower():
            animeList.writerow(row)
        else:
            if not row[0] in banned:
                banned.append(row[0])

with open('rating.csv', newline='', encoding='utf-8') as File:
    reader = csv.reader(File)
    rating = csv.writer(open('Rate.csv', newline='', encoding='utf-8', mode='a+'))
    for row in reader:
        if not row[1] in banned:
            rating.writerow(row)
