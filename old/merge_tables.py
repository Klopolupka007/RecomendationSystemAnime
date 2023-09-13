import pandas as pd

# Загрузите данные из двух CSV файлов
file1 = pd.read_csv('animeList.csv')
file2 = pd.read_csv('anime_parse.csv')
file1['name'] = file1['name'].str.lower()
file2['name'] = file2['name'].str.lower()
file1['name'] = file1['name'].str.replace(' ', '')
file2['name'] = file2['name'].str.replace(' ', '')


# Сопоставьте значения из одного столбца файлов
merged_file = pd.merge(file1, file2, on='name', how='left')

# Создайте новый столбец в первом файле
merged_file['name-ru'] = merged_file['name-ru']
merged_file['src'] = merged_file['src']

# Сохраните результат в новом файле CSV
merged_file.to_csv('merged.csv', index=False)