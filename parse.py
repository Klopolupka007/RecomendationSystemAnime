import csv

from bs4 import BeautifulSoup
import requests

url = 'https://shikimori.me/animes/season/2022,2015_2019,2020_2021,2010_2014,2000_2010,199x,198x,ancient/genre/!34-Yuri,!33-Yaoi,!12-Hentai'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.971 Yowser/2.5 Safari/537.36'
}

'''
content = result.text
soup = BeautifulSoup(content, 'lxml')
box = soup.find_all('img')
L = [link['href'] for link in box]
print(L)
'''
from tqdm import tqdm
'''
file = open('data.txt', 'a', encoding='utf-8')
file_n = open('data_name.txt', 'a', encoding='utf-8')
for i in tqdm(range(840, 968)):
    link = url + '/page/' + str(i)
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    box = soup.find_all('img')
    box_name = soup.find_all('span', class_='name-en')
    file.write(str(box)+'\n')
    file_n.write(str(box_name) + '\n')
'''
file = open('data.txt', 'r', encoding='utf-8')
file_n = open('data_name.txt', 'r', encoding='utf-8')

anime = csv.writer(open('anime_parse.csv', newline='', encoding='utf-8', mode='w'))
anime.writerow(['name-ru', 'src', 'srcset', 'name'])
for str in tqdm(file.readlines()):
    if str == '':
        continue
    str_name = file_n.readline().strip('[]').replace('<span class="name-en">', '').replace('</span>', '').replace(';', ' ').replace(']\n', '').split(',')
    if str_name == []:
        continue
    #str = '[<img alt="Стальной алхимик: Братство" src="https://desu.shikimori.me/uploads/poster/animes/5114/preview_alt-ba65e789c26d848f95418b3f8718b525.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/5114/preview_alt_2x-e8855f1e9deab68bcb8deca302975122.jpeg 2x"/>, <img alt="Врата Штейна" src="https://desu.shikimori.me/uploads/poster/animes/9253/preview_alt-2e34cb98f6d7199d871e9520f24a4b0a.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/9253/preview_alt_2x-4a8bcb5517e572246ba6ef459c18894d.jpeg 2x"/>, <img alt="Блич: Тысячелетняя кровавая война" src="https://desu.shikimori.me/uploads/poster/animes/41467/preview_alt-8cc8979ef0c9228db6a1127fa511fbfc.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/41467/preview_alt_2x-21d9bd1f5418aa35404bcd434951d79a.jpeg 2x"/>, <img alt="Гинтама 4" src="https://desu.shikimori.me/uploads/poster/animes/28977/preview_alt-2fff98c1ee26af4f31c76ae3d5b7a9d6.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/28977/preview_alt_2x-40e249a5561ac2ac220387454e561a9d.jpeg 2x"/>, <img alt="Атака титанов 3. Часть 2" src="https://desu.shikimori.me/uploads/poster/animes/38524/preview_alt-6b7fb02920c5109293e37b07258b229e.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/38524/preview_alt_2x-b0df93920c3039124646f14fa552809f.jpeg 2x"/>, <img alt="Гинтама 2" src="https://desu.shikimori.me/uploads/poster/animes/9969/preview_alt-51616db864aa8711969de0ee916e1260.png" srcset="https://desu.shikimori.me/uploads/poster/animes/9969/preview_alt_2x-c0517c90cd00f6cb5f419d6f815c53f9.png 2x"/>, <img alt="Гинтама: Финал" src="https://desu.shikimori.me/uploads/poster/animes/39486/preview_alt-ac788cf428673269cc49639b8d7d8b61.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/39486/preview_alt_2x-0904735b94f0f18fa52035aa397f3223.jpeg 2x"/>, <img alt="Охотник х Охотник (2011)" src="https://desu.shikimori.me/uploads/poster/animes/11061/preview_alt-6e20d146e854ef52a28f8366d021ad23.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/11061/preview_alt_2x-d5d82f3514e49005d860b19233b58aec.jpeg 2x"/>, <img alt="Госпожа Кагуя: в любви как на войне 3" src="https://desu.shikimori.me/uploads/poster/animes/43608/preview_alt-532c5378713eec5879442201ed20a0e3.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/43608/preview_alt_2x-73581ca061bcca3a2ee2220d5e5fd328.jpeg 2x"/>, <img alt="Гинтама 3" src="https://desu.shikimori.me/uploads/poster/animes/15417/preview_alt-067cace0e71b383d4da65fdeaa6c6f12.png" srcset="https://desu.shikimori.me/uploads/poster/animes/15417/preview_alt_2x-3080c896e699b25c73ffc23b6b677f06.png 2x"/>, <img alt="Легенда о героях Галактики" src="https://desu.shikimori.me/uploads/poster/animes/820/preview_alt-dce26e98e501c6e63d9452fdee5b3651.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/820/preview_alt_2x-d5af51a334ab9b7ce61719f3d9eccdfe.jpeg 2x"/>, <img alt="Корзинка фруктов: Финал" src="https://desu.shikimori.me/uploads/poster/animes/42938/preview_alt-3d02d1535bc3d137f7fd28f945ddbdfe.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/42938/preview_alt_2x-0d85117b96d87f5ff7cf563e9482d651.jpeg 2x"/>, <img alt="Гинтама 5" src="https://desu.shikimori.me/uploads/poster/animes/34096/preview_alt-82fe9d396a84e955ecc0b01224386854.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/34096/preview_alt_2x-739f1045a1a12f6c807af7f7fa5d705a.jpeg 2x"/>, <img alt="Гинтама" src="https://desu.shikimori.me/uploads/poster/animes/918/preview_alt-b036d9f2e2c6967ccdf36044a1929f0b.png" srcset="https://desu.shikimori.me/uploads/poster/animes/918/preview_alt_2x-8a269d63962f08b4d3af8ec2c567b709.png 2x"/>, <img alt="Форма голоса" src="https://desu.shikimori.me/uploads/poster/animes/28851/preview_alt-d83a0a0ff4508a844e7a145d3f3866de.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/28851/preview_alt_2x-aa57b4c3a30c9f6c530dfacfd8c00bbb.jpeg 2x"/>, <img alt="Мартовский лев 2" src="https://desu.shikimori.me/uploads/poster/animes/35180/preview_alt-46dac8aa9f013ed92a2dd63011420e03.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/35180/preview_alt_2x-fcd792cc474d635ec81a3504214ee000.jpeg 2x"/>, <img alt="Кланнад: Продолжение истории" src="https://desu.shikimori.me/uploads/poster/animes/4181/preview_alt-0cfac6b30ce41947ab4f455c5f027cd1.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/4181/preview_alt_2x-4996847842298d51746494e9a094970e.jpeg 2x"/>, <img alt="Код Гиас: Восставший Лелуш 2" src="https://desu.shikimori.me/uploads/poster/animes/2904/preview_alt-df83ebd3c988ac49d7f90714368dd5c0.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/2904/preview_alt_2x-37f126f2ed6c73dec8c63c1d34023269.jpeg 2x"/>, <img alt="Гинтама: Финальная арка — Ёродзуя навсегда!" src="https://desu.shikimori.me/uploads/poster/animes/15335/preview_alt-a9d2340a9b0850e0c7640a7e326b0767.png" srcset="https://desu.shikimori.me/uploads/poster/animes/15335/preview_alt_2x-3745eea66bb3c75ead9029f1c053239c.png 2x"/>, <img alt="Вайолет Эвергарден. Фильм" src="https://desu.shikimori.me/uploads/poster/animes/37987/preview_alt-59a45a44f4054c5ec2a33a7b2acc3e26.jpeg" srcset="https://desu.shikimori.me/uploads/poster/animes/37987/preview_alt_2x-ed61fa6c50ef606e58629f478a778969.jpeg 2x"/>]'
    str = str.strip('[]').replace(' <img alt="', '').replace(" <img alt='", '').replace('<img alt="', '').replace('" src=', '').replace('" srcset=', '').split(' 2x"/>,')
    str_anime = []
    for i in range(len(str)):
        str_anime.append(str[i].replace(' 2x"/>]\n', '').replace('/assets/globals/missing/preview.png', 'None').replace('/assets/globals/missing/preview@2x.png', 'None').replace(",", '~').split('"'))

    for i in range(len(str_anime)):
        if i != len(str_name) and len(str_anime[i]) > 2:

            anime.writerow([str_anime[i][0], str_anime[i][1], str_anime[i][2], str_name[i]])
            print(str_anime[i][0], str_name[i])
        else:
            break

