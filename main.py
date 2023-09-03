import pandas as pd
anime = pd.read_csv('animeList.csv')
rating = pd.read_csv('Rate.csv')
#print(anime.shape, rating.shape)
#print(anime.head(), '\n\n', rating.head())

n_users = len(rating.user_id.unique())
n_anime = len(rating.anime_id.unique())
# print('Количество уникальных пользователей:', n_users)
# print('Количество уникальных аниме:', n_anime, '\nОбщее количество записей:', len(rating), '\nРазряженность матрицы:', len(rating) / (n_users*n_anime) * 100, '%')

print(pd.unique(rating.user_id).shape)
