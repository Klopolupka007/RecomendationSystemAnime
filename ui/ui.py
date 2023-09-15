# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
import pandas as pd
from PyQt5.QtWidgets import QTableView, QHeaderView, QLineEdit, QWidget, QLabel, QVBoxLayout, QRadioButton, QMessageBox, \
    QSizePolicy
from tqdm import tqdm
import numpy as np
from collections import Counter
import json


class Ui_MainWindow(object):


    def Assets(self):
        self.font_header = QtGui.QFont()
        self.font_header.setFamily("Cascadia Mono")
        self.font_header.setPointSize(24)
        self.font_header.setBold(True)
        self.font_header.setWeight(75)
        self.font_header.setKerning(True)

        self.simple_font = QtGui.QFont()
        self.simple_font.setFamily("Arial")
        self.simple_font.setPointSize(11)

        self.bold_font = QtGui.QFont()
        self.bold_font.setFamily("Arial")
        self.bold_font.setPointSize(11)
        self.bold_font.setBold(True)

    def read_dataset(self):
        '''
        Чтение датасета
        :return:
        '''
        self.anime = pd.read_csv('../data/anime.csv')
        self.rating = pd.read_csv('../data/Rate.csv')
        #self.data_anime = pd.read_csv('../old/merged_file.csv')

    # Заголовок приложения
    def header_main(self):
        self.MainLabel = QtWidgets.QLabel(self.centralwidget)
        self.MainLabel.setFont(self.font_header)
        self.MainLabel.setStyleSheet("color: white;")
        self.MainLabel.setTextFormat(QtCore.Qt.AutoText)
        self.MainLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MainLabel.setObjectName("MainLabel")
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setOffset(-1.0, 1.0)
        shadow.setColor(QtGui.QColor("#333333"))
        self.MainLabel.setGraphicsEffect(shadow)
        self.verticalLayout_7.addWidget(self.MainLabel)

    def anime_list(self):
        # Скроллящаяся панель со списком аниме ------------- Уровень 0.1.2
        self.ScrollAreaAnime = QtWidgets.QScrollArea(self.centralwidget)
        self.ScrollAreaAnime.setStyleSheet("QScrollBar:vertical {\n"
                                           "    border: 4px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "    width: 15px;\n"
                                           "    margin: 15x 0 0 0;\n"
                                           "}\n"
                                           "QScrollBar::handle:vertical {\n"
                                           "    border-radius: 7px;\n"
                                           "    background-color: rgb(230, 230, 230, 255);\n"
                                           "    min-height: 20px;\n"
                                           "}\n"
                                           "QScrollBar::sub-line:vertical {\n"
                                           "    border: 4px;\n"
                                           "    border-top-left-radius: 7px;\n"
                                           "    border-top-right-radius: 7px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "}\n"
                                           "QScrollBar::add-line:vertical {\n"
                                           "    border: 4px;\n"
                                           "    border-bottom-left-radius: 7px;\n"
                                           "    border-bottom-right-radius: 7px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "}\n"
                                           "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow-vertical {\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                           "    background: none;\n"
                                           "}")
        self.ScrollAreaAnime.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.ScrollAreaAnime.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaAnime.setWidgetResizable(True)
        self.ScrollAreaAnime.setObjectName("ScrollAreaAnime")
        self.ScrollAreaAnime_layout = QtWidgets.QWidget()
        self.ScrollAreaAnime_layout.setGeometry(QtCore.QRect(0, 0, 308, 166))
        self.ScrollAreaAnime_layout.setObjectName("ScrollAreaAnime_layout")
        self.formLayout = QtWidgets.QFormLayout(self.ScrollAreaAnime_layout)
        self.formLayout.setObjectName("formLayout")

        self.anime_list = list(pd.unique(self.anime['name-ru']))
        self.anime_check_model = QStandardItemModel(len(self.anime_list), 1)
        for row, i in tqdm(enumerate(self.anime_list)):
            it = QStandardItem(str(i))
            it.setEditable(False)
            it.setSelectable(True)
            it.setCheckable(True)
            self.anime_check_model.setItem(row, 0, it)
            self.anime_check_model.setHorizontalHeaderLabels(['Список аниме'])

        self.filter_proxy_modelAnime = QSortFilterProxyModel()
        self.filter_proxy_modelAnime.setSourceModel(self.anime_check_model)
        self.filter_proxy_modelAnime.setFilterCaseSensitivity(Qt.CaseInsensitive)
        #self.filter_proxy_modelAnime.setFilterKeyColumn(0)
        self.tableAnime = QTableView()
        self.tableAnime.setStyleSheet('font-size: 12sp;'
                                  'font-family: Arial;'
                                  'border: none;'
                                  'background-color: rgb(255,255,255,0);')
        self.tableAnime.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableAnime.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableAnime.horizontalHeader().setStyleSheet('border: none;')
        self.tableAnime.verticalHeader().setStyleSheet('border: none;')
        self.tableAnime.setModel(self.filter_proxy_modelAnime)
        self.PlainTextAnime.textChanged.connect(self.filter_proxy_modelAnime.setFilterRegExp)
        self.formLayout.addWidget(self.tableAnime)

    def Jaccar_item(self, anime_1):
        '''
        Расстояние Жаккара
        :return:
        '''
        users_with_anime = self.rating[self.rating['anime_id'] == anime_1]['user_id'].unique()

        other_anime = self.rating[self.rating['user_id'].isin(users_with_anime)]['anime_id'].values
        unique_el, counts = np.unique(other_anime, return_counts=True)
        sorted_indexes = np.argsort(counts)[-100:]  # -counts для сортировки по убыванию
        self.jaccar_unique_elements = unique_el[sorted_indexes]
        self.jaccar_counts = counts[sorted_indexes]
        self.jaccar_counts = self.jaccar_counts/len(self.user_list)
        self.jaccar_counts /= self.jaccar_counts[-1]

        self.ListAnimeBlocks = []
        for i in range(len(self.jaccar_counts)):
            row = self.anime.loc[self.anime['anime_id'] == self.jaccar_unique_elements[i]]
            if row['name-ru'].isnull().values.any():
                str_name = list(row['name'])
            else:
                str_name = list(row['name-ru'])
            self.ListAnimeBlocks.append([list(row['src'])[0], str_name[0]])
        self.change_grid()

    def Jaccar_user(self, user_1):
        '''
        Расстояние Жаккара
        :return:
        '''

        def compute_jaccard_similarity_set(set1, set2):
            intersection = set(set1) & set(set2)
            union = set(set1) | set(set2)
            similarity = len(intersection) / len(union)
            return similarity

        similarities = {}
        for number, values in tqdm(self.userlist_anime.items()):
            if number != str(user_1):
                similarity = compute_jaccard_similarity_set(values, self.userlist_anime[str(user_1)])
                similarities[number] = similarity
        count = Counter([item for sublist in [self.userlist_anime[key] for key in sorted(similarities, key=similarities.get, reverse=True)[:100]] for item in sublist])
        self.ListAnimeBlocks = count.most_common()[:100]
        self.change_grid()

    def Manhattan(self, user_1):
        user_list_1 = self.userlist_anime[str(user_1)]
        result = []
        for number, values in tqdm(self.userlist_anime.items()):
            temp = 0
            if number != str(user_1):
                users = set(values) & set(user_list_1)
                if len(users) / len(user_list_1) > 0.76:
                    for i in users:
                        user_1_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(user_1))]['rating'])
                        if user_1_rate[0] == -1:
                            user_1_rate[0] = self.avg[str(i)]
                        user_2_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(number))]['rating'])
                        if user_2_rate[0] == -1:
                            user_2_rate[0] = self.avg[str(i)]
                        temp += user_1_rate[0] - user_2_rate[0]
                    if not len(users) == 0:
                        result.append((number, abs(temp/(len(users)))))
        if len(result) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Предупреждение')
            msg.setWindowTitle('Warning')
            msg.setInformativeText(
                'Внимание! Не было найдено ни одного пользователя, прошедших порог похожести с вашим профилем!')
            msg.exec()
            return
        min = 1e308
        min_tuple = None
        for i in result:
            if min > i[1]:
                min = i[1]
                min_tuple = i
        min = self.userlist_anime[min_tuple[0]]
        self.ListAnimeBlocks = []
        for i in min:
            self.ListAnimeBlocks.append([list(self.anime[self.anime['anime_id'] == int(i)]['src'])[0], list(self.anime[self.anime['anime_id'] == int(i)]['name-ru'])[0]])
        self.change_grid()

    def Euclid(self, user_1):
        user_list_1 = self.userlist_anime[str(user_1)]
        result = []
        for number, values in tqdm(self.userlist_anime.items()):
            temp = 0
            if number != str(user_1):
                users = set(values) & set(user_list_1)
                if len(users) / len(user_list_1) > 0.76:
                    for i in users:
                        user_1_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(user_1))]['rating'])
                        if user_1_rate[0] == -1:
                            user_1_rate[0] = self.avg[str(i)]
                        user_2_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(number))]['rating'])
                        if user_2_rate[0] == -1:
                            user_2_rate[0] = self.avg[str(i)]
                        temp += (user_1_rate[0] - user_2_rate[0])**2
                    if not len(users) == 0:
                        result.append((number, (temp/(len(users))**(1/2))))
        if len(result) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Предупреждение')
            msg.setWindowTitle('Warning')
            msg.setInformativeText(
                'Внимание! Не было найдено ни одного пользователя, прошедших порог похожести с вашим профилем!')
            msg.exec()
            return
        min = 1e308
        min_tuple = None
        for i in result:
            if min > i[1]:
                min = i[1]
                min_tuple = i
        min = self.userlist_anime[min_tuple[0]]
        self.ListAnimeBlocks = []
        for i in min:
            self.ListAnimeBlocks.append([list(self.anime[self.anime['anime_id'] == int(i)]['src'])[0], list(self.anime[self.anime['anime_id'] == int(i)]['name-ru'])[0]])
        self.change_grid()

    def Cosine(self, user_1):
        user_list_1 = self.userlist_anime[str(user_1)]
        result = []
        for number, values in tqdm(self.userlist_anime.items()):
            temp = 0
            temp_A = 0
            temp_B = 0
            if number != str(user_1):
                users = set(values) & set(user_list_1)
                if len(users) / len(user_list_1) > 0.76:
                    for i in users:
                        user_1_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(user_1))]['rating'])
                        if user_1_rate[0] == -1:
                            user_1_rate[0] = self.avg[str(i)]
                        user_2_rate = list(self.rating[(self.rating['anime_id'] == int(i)) & (self.rating['user_id'] == int(number))]['rating'])
                        if user_2_rate[0] == -1:
                            user_2_rate[0] = self.avg[str(i)]
                        temp += user_1_rate[0] * user_2_rate[0]
                        temp_A += user_1_rate[0]**2
                        temp_B += user_2_rate[0] ** 2
                    if not len(users) == 0:
                        result.append((number, (temp/((temp_A**1/2)*(temp_B**1/2)*len(users))) ))
        if len(result) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Предупреждение')
            msg.setWindowTitle('Warning')
            msg.setInformativeText(
                'Внимание! Не было найдено ни одного пользователя, прошедших порог похожести с вашим профилем!')
            msg.exec()
            return
        min = -10000
        min_tuple = None
        for i in result:
            if min < i[1]:
                min = i[1]
                min_tuple = i
        min = self.userlist_anime[min_tuple[0]]
        self.ListAnimeBlocks = []
        for i in min:
            self.ListAnimeBlocks.append([list(self.anime[self.anime['anime_id'] == int(i)]['src'])[0], list(self.anime[self.anime['anime_id'] == int(i)]['name-ru'])[0]])
        self.change_grid()

    def user_list(self):
        # Скролляцаяся панель со списком пользователей -------------- Уровень 0.1.4
        self.ScrollAreaUsers = QtWidgets.QScrollArea()
        self.ScrollAreaUsers.setStyleSheet("QScrollBar:vertical {\n"
                                           "    border: 4px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "    width: 15px;\n"
                                           "    margin: 15x 0 0 0;\n"
                                           "}\n"
                                           "QScrollBar::handle:vertical {\n"
                                           "    border-radius: 7px;\n"
                                           "    background-color: rgb(230, 230, 230, 255);\n"
                                           "    min-height: 20px;\n"
                                           "}\n"
                                           "QScrollBar::sub-line:vertical {\n"
                                           "    border: 4px;\n"
                                           "    border-top-left-radius: 7px;\n"
                                           "    border-top-right-radius: 7px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "}\n"
                                           "QScrollBar::add-line:vertical {\n"
                                           "    border: 4px;\n"
                                           "    border-bottom-left-radius: 7px;\n"
                                           "    border-bottom-right-radius: 7px;\n"
                                           "    background-color: rgb(255, 255, 255, 50);\n"
                                           "}\n"
                                           "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow-vertical {\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                           "    background: none;\n"
                                           "}\n"
                                           "")
        self.ScrollAreaUsers.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ScrollAreaUsers.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaUsers.setWidgetResizable(True)
        self.ScrollAreaUsers.setObjectName("ScrollAreaUsers")
        self.ScrollAreaUsers_layout = QtWidgets.QWidget()
        self.ScrollAreaUsers_layout.setGeometry(QtCore.QRect(0, -16, 293, 183))
        self.ScrollAreaUsers_layout.setObjectName("ScrollAreaUsers_layout")
        self.formLayout_2 = QtWidgets.QVBoxLayout(self.ScrollAreaUsers_layout)
        self.formLayout_2.setObjectName("formLayout_2")

        self.user_list = list(pd.unique(self.rating['user_id']))
        # user_list = list(pd.unique(self.rating.user_id))
        self.user_check_model = QStandardItemModel(len(self.user_list), 1)

        for row, i in tqdm(enumerate(self.user_list)):
            it = QStandardItem(str(i))
            it.setEditable(False)
            it.setCheckable(True)
            self.user_check_model.setItem(row, 0, it)
            self.user_check_model.setHorizontalHeaderLabels(['Список пользователей'])
        self.filter_proxy_modelUsers = QSortFilterProxyModel()
        self.filter_proxy_modelUsers.setSourceModel(self.user_check_model)
        self.filter_proxy_modelUsers.setFilterCaseSensitivity(Qt.CaseInsensitive)
        #self.filter_proxy_modelUsers.setFilterKeyColumn(0)
        self.table_users = QTableView()
        self.table_users.setStyleSheet('font-size: 12sp;'
                                  'font-family: Arial;'
                                  'border: none;'
                                  'background-color: rgb(255,255,255,0);')
        self.table_users.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_users.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_users.horizontalHeader().setStyleSheet('border: none;')
        self.table_users.verticalHeader().setStyleSheet('border: none;')
        self.table_users.setModel(self.filter_proxy_modelUsers)
        self.PlainTextUsers.textChanged.connect(self.filter_proxy_modelUsers.setFilterRegExp)
        self.formLayout_2.addWidget(self.table_users)

    def anime_by_user(self, user_id):
        animeByUser = self.rating[self.rating['user_id'] == user_id]['anime_id']
        self.ListAnimeBlocks = []
        for i in animeByUser:
            self.ListAnimeBlocks.append([self.anime[self.anime['anime_id'] == i]['src'].values[0], self.anime[self.anime['anime_id'] == i]['name-ru'].values[0]])
        self.change_grid()

    def change_grid(self):
        '''
        Обновление области списка аниме
        :return:
        '''
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        if self.ListAnimeBlocks == []:
            pass
        else:
            if type(self.ListAnimeBlocks[0]) == tuple:
                temp = []
                for i in self.ListAnimeBlocks:
                    temp.append([self.anime[self.anime['anime_id'] == int(i[0])]['src'].values[0], self.anime[self.anime['anime_id'] == int(i[0])]['name-ru'].values[0]])
                self.ListAnimeBlocks = temp.copy()
            k = 0
            for i, image_label in enumerate(self.ListAnimeBlocks):
                image_path, label_text = image_label
                if type(image_path) == str:
                    widget = QWidget()
                    widget_layout = QVBoxLayout()
                    widget_layout.setAlignment(Qt.AlignHCenter)
                    widget.setLayout(widget_layout)

                    self.image_label = QLabel()
                    if not isinstance(image_path, str):
                        image = "assets/Not_found_image.jpg"
                    else:
                        image = '../parse/images/'+image_path.split('/')[-1]
                    img = QPixmap(image)
                    self.image_label.setPixmap(img)
                    self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    self.image_label.setStyleSheet('background-color:gray;')
                    self.image_label.setMaximumWidth(160)
                    self.image_label.setMaximumHeight(226)
                    widget_layout.addWidget(self.image_label)

                    label = QLabel(label_text.replace('~', ','))
                    label.setMaximumWidth(160)
                    label.setWordWrap(True)
                    widget_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    #label.setStyleSheet('background-color:gray;')
                    widget_layout.addWidget(label)

                    # Добавляем виджет в GridLayout
                    self.gridLayout.addWidget(widget, (i-k) // 6, (i-k) % 6)
                else:
                    k += 1

    def TrashClick(self):
        for row in range(len(self.anime_list)):
            it = self.anime_check_model.item(row, 0)
            if Qt.Checked == it.checkState():
                it.setCheckState(QtCore.Qt.Unchecked)
        for row in range(len(self.user_list)):
            it = self.user_check_model.item(row, 0)
            if Qt.Checked == it.checkState():
                it.setCheckState(QtCore.Qt.Unchecked)

    def SearchClick(self):
        self.userSelected = ''
        self.animeSelected = ''
        if self.type.currentText() == 'Item-based':
            for row in range(len(self.anime_list)):
                it = self.anime_check_model.item(row, 0)
                if Qt.Checked == it.checkState() and self.animeSelected == '':
                    self.animeSelected = self.anime[self.anime['name-ru'] == it.text()]['anime_id'].unique()[0]
                    self.Jaccar_item(self.animeSelected)
                elif Qt.Checked == it.checkState() and self.animeSelected != '':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText('Предупреждение')
                    msg.setWindowTitle('Warning')
                    msg.setInformativeText(
                    'Внимание! Выделенно 2 и более объектов в списке, в качестве активного будет использован элемент выше '
                    'по списку. Для отмены выделения уберите галочку из соответствующих объектов или воспользуйтесь '
                    'кнопкой сброса выделения.')
                    msg.exec()
                    break
        elif self.type.currentText() == 'User-based':
            for row in range(len(self.user_list)):
                it = self.user_check_model.item(row, 0)
                if Qt.Checked == it.checkState() and self.userSelected == '':
                    self.userSelected = it.text()
                    #'Метод Жаккара', 'Расстояние Манхеттена', "Евклидово расстояние", "Коэфициент Отиаи", "Коэфициент корелляции Пирсона"
                    if self.method.currentText() == 'Метод Жаккара':
                        self.Jaccar_user(int(self.userSelected))
                    elif self.method.currentText() == 'Расстояние Манхеттена':
                        self.Manhattan(int(self.userSelected))
                    elif self.method.currentText() == 'Евклидово расстояние':
                        self.Euclid(int(self.userSelected))
                    elif self.method.currentText() == 'Коэфициент Отиаи':
                        self.Cosine(int(self.userSelected))
                elif Qt.Checked == it.checkState() and self.userSelected != '':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText('Предупреждение')
                    msg.setWindowTitle('Warning')
                    msg.setInformativeText(
                    'Внимание! Выделенно 2 и более объектов в списке, в качестве активного будет использован элемент выше '
                    'по списку. Для отмены выделения уберите галочку из соответствующих объектов или воспользуйтесь '
                    'кнопкой сброса выделения.')
                    msg.exec()
                    break
        else:
            for row in range(len(self.user_list)):
                it = self.user_check_model.item(row, 0)
                if Qt.Checked == it.checkState() and self.userSelected == '':
                    self.userSelected = it.text()
                    self.anime_by_user(int(self.userSelected))
                elif Qt.Checked == it.checkState() and self.userSelected != '':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText('Предупреждение')
                    msg.setWindowTitle('Warning')
                    msg.setInformativeText(
                    'Внимание! Выделенно 2 и более объектов в списке, в качестве активного будет использован элемент выше '
                    'по списку. Для отмены выделения уберите галочку из соответствующих объектов или воспользуйтесь '
                    'кнопкой сброса выделения.')
                    msg.exec()
                    break


    def setupUi(self, MainWindow):

        with open('../data/grouping_anime_by_users.json', 'r') as jsonFile:
            self.userlist_anime = json.load(jsonFile)

        with open('../data/средние_оценки.json', 'r') as avgFile:
            self.avg = json.load(avgFile)

        # Читаем датасет
        self.read_dataset()
        self.Assets()
        MainWindow.setObjectName("MainWindow")
        #MainWindow.setFixedSize(930, 560)
        MainWindow.setEnabled(True)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(
            "QWidget#centralwidget {border-image: url(\"assets/doge.jpg\");}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setContentsMargins(10, 20, 10, 15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.header_main()


        # ----------------- Верхний уровень 0 ------------------
        # Главный Layout (горизонтальный)
        self.MainHorizontalLayout = QtWidgets.QHBoxLayout()
        self.MainHorizontalLayout.setObjectName("MainHorizontalLayout")

        # Левая панель (поисковая) ------- Уровень 0.1
        self.LeftPanel = QtWidgets.QVBoxLayout()
        self.LeftPanel.setContentsMargins(12, -1, 6, -1)
        self.LeftPanel.setObjectName("LeftPanel")

        # Поисковая строка аниме --------- Уровень 0.1.1
        self.PlainTextAnime = QtWidgets.QLineEdit(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.PlainTextAnime.setPalette(palette)
        self.PlainTextAnime.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.PlainTextAnime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.PlainTextAnime.setStyleSheet("font: 11pt \"Arial\";\n"
                                          "border-radius:5px;\n"
                                          "background-color: rgb(255, 255, 255, 200);")
        self.PlainTextAnime.setText("")
        self.PlainTextAnime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PlainTextAnime.setObjectName("PlainTextAnime")
        self.LeftPanel.addWidget(self.PlainTextAnime)

        # Добавляем список аниме
        self.animeSelected = ''
        self.anime_list()
        self.ScrollAreaAnime.setWidget(self.ScrollAreaAnime_layout)
        self.LeftPanel.addWidget(self.ScrollAreaAnime)

        # Поисковая строка с пользователями ------------ Уровень 0.1.3
        self.PlainTextUsers = QLineEdit(self.centralwidget)
        self.PlainTextUsers.setStyleSheet("font: 11pt \"Arial\";\n"
                                          "border-radius:5px;\n"
                                          "background-color: rgb(255, 255, 255, 200);")
        self.PlainTextUsers.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PlainTextUsers.setObjectName("PlainTextUsers")
        self.LeftPanel.addWidget(self.PlainTextUsers)

        # Добавляем список элементов пользователей
        self.userSelected = ''
        self.user_list()
        self.ScrollAreaUsers.setWidget(self.ScrollAreaUsers_layout)
        self.LeftPanel.addWidget(self.ScrollAreaUsers)

        # Кнопки левой панели (Поиск, мусорка) --------- Уровни 0.1.5.x
        self.Search_Trash_layout = QtWidgets.QHBoxLayout()
        self.Search_Trash_layout.setObjectName("Search_Trash_layout")
        self.SearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.SearchButton.setFont(self.simple_font)
        self.SearchButton.setObjectName("SearchButton")
        self.SearchButton.clicked.connect(self.SearchClick)
        self.Search_Trash_layout.addWidget(self.SearchButton)
        self.TrashButton = QtWidgets.QPushButton(self.centralwidget)
        self.TrashButton.setFont(self.simple_font)
        self.TrashButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                       "")
        self.TrashButton.setIcon(QtGui.QIcon('assets/trash.png'))
        self.TrashButton.setIconSize(QtCore.QSize(20, 20))
        self.TrashButton.setObjectName("TrashButton")
        self.TrashButton.clicked.connect(self.TrashClick)
        self.Search_Trash_layout.addWidget(self.TrashButton)
        self.Search_Trash_layout.setStretch(0, 4)
        self.Search_Trash_layout.setStretch(1, 1)
        self.LeftPanel.addLayout(self.Search_Trash_layout)
        self.LeftPanel.setStretch(0, 1)
        self.LeftPanel.setStretch(1, 5)
        self.LeftPanel.setStretch(2, 1)
        self.LeftPanel.setStretch(3, 5)
        self.LeftPanel.setStretch(4, 1)
        self.MainHorizontalLayout.addLayout(self.LeftPanel)

        # Правая панель -------- Уровень 0.2
        self.RightPanel = QtWidgets.QVBoxLayout()
        self.RightPanel.setObjectName("RightPanel")

        # Настройки визуализации -------- Уровень 0.2.1
        self.UpperFrame = QtWidgets.QFrame(self.centralwidget)
        self.UpperFrame.setStyleSheet(" border-radius:10px;\n"
                                      "background-color: rgb(255, 255, 255, 150);")
        self.UpperFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UpperFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UpperFrame.setObjectName("UpperFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.UpperFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Тестовые кнопки -------- Уровни 0.2.1.3-0.2.1.4
        self.method = QtWidgets.QComboBox(self.UpperFrame)
        self.method.setObjectName("method")
        self.horizontalLayout_2.addWidget(self.method)
        self.type = QtWidgets.QComboBox(self.UpperFrame)
        self.type.setObjectName("type")
        self.horizontalLayout_2.addWidget(self.type)

        self.RightPanel.addWidget(self.UpperFrame)

        # Скроллящаяся панель рекомендуемого аниме -------- Уровень 0.2.2
        self.ScrollAreaAnimeList = QtWidgets.QScrollArea(self.centralwidget)
        self.ScrollAreaAnimeList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaAnimeList.setObjectName('animeScroll')
        self.ScrollAreaAnimeList.setStyleSheet("QScrollArea#animeScroll { background-color:transparent; background-image: transparent; border: none;}")
        self.ScrollAreaAnimeList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaAnimeList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.ScrollAreaAnimeList.setWidgetResizable(True)
        self.ScrollAreaAnimeList.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ScrollAreaAnimeList_layout = QtWidgets.QWidget()
        self.ScrollAreaAnimeList_layout.setObjectName("ScrollAreaAnimeList_layout")
        self.ScrollAreaAnimeList_layout.setStyleSheet("QWidget#message_container {background-color:transparent;}")
        self.ScrollAreaAnimeList_layout.setGeometry(QtCore.QRect(0, 0, 541, 389))
        self.gridLayout = QtWidgets.QGridLayout(self.ScrollAreaAnimeList_layout)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(0)

        # Созадем список блоков аниме
        self.ListAnimeBlocks = []
        self.change_grid()


        self.ScrollAreaAnimeList.setWidget(self.ScrollAreaAnimeList_layout)
        self.RightPanel.addWidget(self.ScrollAreaAnimeList)
        self.RightPanel.setStretch(0, 1)
        self.RightPanel.setStretch(1, 12)

        self.MainHorizontalLayout.addLayout(self.RightPanel)
        self.MainHorizontalLayout.setStretch(0, 3)
        self.MainHorizontalLayout.setStretch(1, 5)
        self.verticalLayout_7.addLayout(self.MainHorizontalLayout)
        self.verticalLayout_7.setStretch(0, 2)
        self.verticalLayout_7.setStretch(1, 12)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Рекомендательная система по подбору Аниме"))
        MainWindow.setWindowIcon(QtGui.QIcon('assets/iconWindow.png'))
        self.MainLabel.setText(_translate("MainWindow", "Рекомендательная система для подбора аниме"))
        self.PlainTextAnime.setPlaceholderText(_translate("MainWindow", "Введите название аниме"))
        self.PlainTextUsers.setPlaceholderText(_translate("MainWindow", "Введите имя пользователя"))
        self.SearchButton.setText(_translate("MainWindow", "Поиск"))
        self.method.addItems(['Метод Жаккара', 'Расстояние Манхеттена', "Евклидово расстояние", "Коэфициент Отиаи", "Коэфициент корелляции Пирсона"])
        self.type.addItems(["User-based", "Item-based", 'Список аниме пользователя'])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Добавляем шансон
    playlist = QMediaPlaylist()
    url = QUrl.fromLocalFile("assets/audio_1.mp3")
    playlist.addMedia(QMediaContent(url))
    playlist.setPlaybackMode(QMediaPlaylist.Loop)
    player = QMediaPlayer()
    player.setPlaylist(playlist)
    player.play()

    MainWindow.showMaximized()
    sys.exit(app.exec_())