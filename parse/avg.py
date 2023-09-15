import pandas as pd
import json

df = pd.read_csv('../data/Rate.csv')

df = df[df['rating'] != -1]
average_ratings = df.groupby(['anime_id', 'user_id'])['rating'].mean().reset_index()
anime_ratings_dict = {}
for anime_id, group in average_ratings.groupby('anime_id'):
    anime_ratings_dict[str(anime_id)] = group['rating'].mean()


with open('../data/средние_оценки.json', 'w') as json_file:
    json.dump(anime_ratings_dict, json_file)