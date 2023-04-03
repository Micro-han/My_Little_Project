import sys

from ui.mainWindow import Ui_mainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class funcWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = funcWindow()
    window.show()
    sys.exit(app.exec_())