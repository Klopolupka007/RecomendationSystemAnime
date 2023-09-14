import csv
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.971 Yowser/2.5 Safari/537.36'
}

File =  csv.reader(open('../data/anime.csv', newline='', encoding='utf-8'))
k = 0
for i in File:
    if not i[8] == 'src' and not i[8] == '':
        k += 1
        if k > 8309:
            resource = requests.get(i[8], headers=headers)
            res = open(i[8].split('/')[-1], 'wb')
            res.write(resource.content)
            res.close()
