from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow



app = QApplication([])

window = QPushButton("Push Me")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")
        self.setMinimumSize(200, 300)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)
# window = QWidget()
window.show()
app.exec()