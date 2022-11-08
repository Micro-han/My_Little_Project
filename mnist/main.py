import sys
from ui.bindfuncWindow import funcWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = funcWindow()
    ui.show()
    sys.exit(app.exec_())
