import os
from PIL import Image

# Заданные параметры размера (ширина и высота в пикселях)
max_width = 160
max_height = 226

# Папка с изображениями
folder = './images/'

# Перебор файлов в папке
for file in os.listdir(folder):
    if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Поддерживаемые форматы изображений
        path_to_file = os.path.join(folder, file)
        img = Image.open(path_to_file)

        # Получение текущих размеров изображения
        width, height = img.size

        # Проверка, нужно ли уменьшать изображение
        if width > max_width or height > max_height:
            # Вычисление новых размеров с сохранением пропорций
            new_width = min(width, max_width)
            new_height = int(new_width * (height / width))

            # Уменьшение размера изображения
            resize_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Сохранение уменьшенного изображения (можно использовать другой формат файла)
            path_to_resize_img = os.path.join(folder, 'resized/', file)
            resize_img.save(path_to_resize_img)

            print(f"Изображение '{file}' было уменьшено.")