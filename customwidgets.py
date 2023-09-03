from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout)


class OnOffWidget(QWidget):

    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.name = name  # Name of widget used for searching.
        self.is_on = False  # Current state (true=ON, false=OFF)