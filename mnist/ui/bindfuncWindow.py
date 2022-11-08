import io
import sys

import numpy as np
import torch
import cv2

from PIL import Image
from ui.mainWindow import Ui_MainWindow
from network.myCNN import CNN
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QPoint, Qt, QBuffer


class funcWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.predictButton.clicked.connect(self.predictFunction)
        self.clearButton.clicked.connect(self.clearFunction)
        self.saveButton.clicked.connect(self.saveFunction)

        self.paintWidget = QPixmap(330, 440)
        self.paintWidget.fill(Qt.white)
        self.lastPoint = QPoint()
        self.endPoint = QPoint()

        self.lastImg = Image.Image
        self.lastPredict = []
        self.cnt = 0

    def paintEvent(self, event):
        painPainter = QPainter(self.paintWidget)
        painPainter.drawLine(self.lastPoint, self.endPoint)
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.paintWidget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.button and Qt.LeftButton:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            self.update()

    def predictFunction(self):
        cnn = CNN()
        cnn.load_state_dict(torch.load('./network/model.pkl'))
        cnn.eval()

        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        q_img = self.paintWidget.toImage()
        q_img.save(buffer, "PNG")
        tmp_input = Image.open(io.BytesIO(buffer.data()))

        self.lastImg = tmp_input

        tmp_input = tmp_input.convert("L")
        tmp_input = tmp_input.resize((28, 28))

        res = []
        for x in range(28):
            for y in range(28):
                pixel = 1.0 - float(tmp_input.getpixel((y, x))) / 255.0
                res.append(pixel)
        res2 = torch.tensor(np.array(res).reshape((1, 1, 28, 28)))
        res2 = res2.to(torch.float32)
        out = cnn(res2)
        y = torch.max(out, 1)[1].data.numpy()
        self.numberLabel.setText(str(y))
        self.lastPredict = y

    def clearFunction(self):
        self.paintWidget.fill(Qt.white)
        self.numberLabel.clear()
        self.update()

    def saveFunction(self):
        self.cnt += 1
        path = 'The ' + str(self.cnt) + 'th predict is' + str(self.lastPredict) + '.png'
        self.lastImg.save(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = funcWindow()
    window.show()
    sys.exit(app.exec_())