# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
import pandas as pd
from PyQt5.QtWidgets import QTableView, QHeaderView, QLineEdit, QWidget, QLabel, QVBoxLayout, QRadioButton, QMessageBox
import requests
from tqdm import tqdm

from customwidgets import OnOffWidget

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
        self.anime = pd.read_csv('../animeList.csv')
        self.rating = pd.read_csv('../Rate.csv')

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
        self.ScrollAreaAnime.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaAnime.setWidgetResizable(True)
        self.ScrollAreaAnime.setObjectName("ScrollAreaAnime")
        self.ScrollAreaAnime_layout = QtWidgets.QWidget()
        self.ScrollAreaAnime_layout.setGeometry(QtCore.QRect(0, 0, 308, 166))
        self.ScrollAreaAnime_layout.setObjectName("ScrollAreaAnime_layout")
        self.formLayout = QtWidgets.QFormLayout(self.ScrollAreaAnime_layout)
        self.formLayout.setObjectName("formLayout")

        anime_list = list(pd.unique(self.anime['name']))
        anime_check_model = QStandardItemModel(len(anime_list), 1)
        for row, i in tqdm(enumerate(anime_list)):
            it = QStandardItem(str(i))
            it.setEditable(False)
            it.setSelectable(True)
            it.setCheckable(True)
            anime_check_model.setItem(row, 0, it)
            anime_check_model.setHorizontalHeaderLabels(['Список аниме'])

        self.filter_proxy_modelAnime = QSortFilterProxyModel()
        self.filter_proxy_modelAnime.setSourceModel(anime_check_model)
        # filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_modelAnime.setFilterKeyColumn(0)
        self.tableAnime = QTableView()
        self.tableAnime.setStyleSheet('font-size: 12px;'
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
        # filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_modelUsers.setFilterKeyColumn(0)
        self.table_users = QTableView()
        self.table_users.setStyleSheet('font-size: 12px;'
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
            for i, image_label in enumerate(self.ListAnimeBlocks):
                image_path, label_text = image_label

                widget = QWidget()
                widget_layout = QVBoxLayout()
                widget.setLayout(widget_layout)

                image_label = QLabel()
                if image_path == '':
                    image = "F:\PycharmProjects\RecomendationSystem\\ui\\assets\\Not_found_image.jpg"
                else:

                    image = QImage()
                    image.loadFromData(requests.get(image_path).content)
                image_label.setPixmap(QPixmap(image))
                widget_layout.addWidget(image_label)

                label = QLabel(label_text)
                widget_layout.addWidget(label)

                # Добавляем виджет в GridLayout
                self.gridLayout.addWidget(widget, i // 3, i % 3)

    def SearchClick(self):
        self.userSelected = ''
        for row in range(len(self.user_list)):
            it = self.user_check_model.item(row, 0)
            if Qt.Checked == it.checkState() and self.userSelected == '':
                self.userSelected = it.text()
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
        # Читаем датасет
        self.read_dataset()
        self.Assets()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(897, 547)
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
        self.PlainTextAnime.setStyleSheet("font: 12pt \"Arial\";\n"
                                          " border-radius:5px;\n"
                                          "background-color: rgb(255, 255, 255, 200);")
        self.PlainTextAnime.setText("")
        self.PlainTextAnime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PlainTextAnime.setObjectName("PlainTextAnime")
        self.LeftPanel.addWidget(self.PlainTextAnime)

        # Добавляем список аниме
        self.anime_list()
        self.ScrollAreaAnime.setWidget(self.ScrollAreaAnime_layout)
        self.LeftPanel.addWidget(self.ScrollAreaAnime)

        # Поисковая строка с пользователями ------------ Уровень 0.1.3
        self.PlainTextUsers = QLineEdit(self.centralwidget)
        self.PlainTextUsers.setStyleSheet("font: 12pt \"Arial\";\n"
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

        # Сортировка -------- Уровни 0.2.1.1-0.2.1.2
        self.SortingLabel = QtWidgets.QLabel(self.UpperFrame)
        self.SortingLabel.setFont(self.simple_font)
        self.SortingLabel.setStyleSheet("background-color: rgb(255,255,255,0);")
        self.SortingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SortingLabel.setObjectName("SortingLabel")
        self.horizontalLayout_2.addWidget(self.SortingLabel)
        self.ComboBoxSorting = QtWidgets.QComboBox(self.UpperFrame)
        self.ComboBoxSorting.setObjectName("ComboBoxSorting")
        self.ComboBoxSorting.addItem("")
        self.ComboBoxSorting.addItem("")
        self.horizontalLayout_2.addWidget(self.ComboBoxSorting)

        # Тестовые кнопки -------- Уровни 0.2.1.3-0.2.1.4
        self.test1 = QtWidgets.QPushButton(self.UpperFrame)
        self.test1.setObjectName("test1")
        self.horizontalLayout_2.addWidget(self.test1)
        self.test2 = QtWidgets.QPushButton(self.UpperFrame)
        self.test2.setObjectName("test2")
        self.horizontalLayout_2.addWidget(self.test2)

        self.RightPanel.addWidget(self.UpperFrame)

        # Скроллящаяся панель рекомендуемого аниме -------- Уровень 0.2.2
        self.ScrollAreaAnimeList = QtWidgets.QScrollArea(self.centralwidget)
        self.ScrollAreaAnimeList.setAutoFillBackground(False)
        self.ScrollAreaAnimeList.setStyleSheet("QScrollBar:vertical {\n"
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
        self.ScrollAreaAnimeList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ScrollAreaAnimeList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ScrollAreaAnimeList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.ScrollAreaAnimeList.setWidgetResizable(True)
        self.ScrollAreaAnimeList.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ScrollAreaAnimeList.setObjectName("ScrollAreaAnimeList")
        self.ScrollAreaAnimeList_layout = QtWidgets.QWidget()
        self.ScrollAreaAnimeList_layout.setGeometry(QtCore.QRect(0, 0, 541, 389))
        self.ScrollAreaAnimeList_layout.setObjectName("ScrollAreaAnimeList_layout")
        self.gridLayout = QtWidgets.QGridLayout(self.ScrollAreaAnimeList_layout)
        self.gridLayout.setObjectName("gridLayout")

        # Созадем список блоков аниме
        self.ListAnimeBlocks = [('https://desu.shikimori.me/uploads/poster/animes/5114/preview_alt-ba65e789c26d848f95418b3f8718b525.jpeg', 'Стальной алхимик'),
                                ('', 'алхимик'),
                                ('', 'алхимик'),
                                ('', 'алхимик')]
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
        '''
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
        self.label_12.setText(_translate("MainWindow", "TextLabel"))
        self.label_13.setText(_translate("MainWindow", "TextLabel"))
        self.label_14.setText(_translate("MainWindow", "TextLabel"))
        self.label_15.setText(_translate("MainWindow", "TextLabel"))
        self.label_16.setText(_translate("MainWindow", "TextLabel"))
        self.label_17.setText(_translate("MainWindow", "TextLabel"))
        '''
        self.SearchButton.setText(_translate("MainWindow", "Поиск"))
        self.SortingLabel.setText(_translate("MainWindow", "Сортировать по:"))
        self.ComboBoxSorting.setItemText(0, _translate("MainWindow", "Возрастанию"))
        self.ComboBoxSorting.setItemText(1, _translate("MainWindow", "Убыванию"))
        self.test1.setText(_translate("MainWindow", "PushButton"))
        self.test2.setText(_translate("MainWindow", "PushButton"))
        # self.pushButton_5.setText(_translate("MainWindow", "PushButton"))


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

    MainWindow.show()
    sys.exit(app.exec_())
