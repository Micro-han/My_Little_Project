import os
import sys
import time

import matplotlib.pyplot as plt
from PIL import Image
from PIL.ImageQt import ImageQt
from ui.mainWindow import Ui_mainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from policy import LSB
from policy import mSteganoGAN
from steganogan import SteganoGAN
import imageio
import torch
from imageio import imread, imwrite
from torch.nn.functional import binary_cross_entropy_with_logits, mse_loss
from torch.optim import Adam
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class funcWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chooseButton.clicked.connect(self.chooseImg)
        self.chooseButton_2.clicked.connect(self.chooseImg_2)
        self.encodeButton.clicked.connect(self.encodeImg)
        self.decodeButton.clicked.connect(self.decodeImg)
        self.downButton.clicked.connect(self.downImg)

        self.img_path = ""
        self.img_path_decode = ""
        self.output_img = None
        self.steganogan = SteganoGAN.load(architecture='dense')
        self.method = None

    def chooseImg(self):
        img_name = QFileDialog.getOpenFileNames(self, '选择图像', os.getcwd())
        self.img_path = img_name[0][0]

        figure = plt.figure()
        canvas = FigureCanvas(figure)
        img = Image.open(self.img_path).resize((512, 512))
        plt.imshow(img)
        plt.axis('off')
        canvas.draw()

        scene1 = QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        scene1.addWidget(canvas)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.preView.setScene(scene1)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.preView.show()  # 最后，调用show方法呈现图形！

    def chooseImg_2(self):
        img_name = QFileDialog.getOpenFileNames(self, '选择图像', os.getcwd())
        self.img_path_decode = img_name[0][0]

        figure = plt.figure()
        canvas = FigureCanvas(figure)
        img = Image.open(self.img_path_decode)
        plt.imshow(img)
        plt.axis('off')
        canvas.draw()

        scene1 = QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        scene1.addWidget(canvas)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicsView_2.setScene(scene1)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicsView_2.show()  # 最后，调用show方法呈现图形！

    def encodeImg(self):
        img = Image.open(self.img_path).resize((512, 512))
        txt = self.messageLine.text()
        print(txt)

        self.method = self.methodBox.currentText()
        encode_img = None
        if self.method == "LSB":
            encode_img = LSB.encode_img(img, txt)
            self.output_img = encode_img
        elif self.method == "SteganoGAN":
            self.output_img = mSteganoGAN.my_steganogan_encode(self.steganogan, self.img_path, txt)
            encode_img = self.output_img

        figure = plt.figure()
        canvas = FigureCanvas(figure)
        plt.imshow(encode_img)
        plt.axis('off')
        canvas.draw()

        scene2 = QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        scene2.addWidget(canvas)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicsView.setScene(scene2)  # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicsView.show()  # 最后，调用show方法呈现图形！

    def decodeImg(self):
        img = Image.open(self.img_path_decode)
        method = self.methodBox_2.currentText()
        if method == "LSB":
            lsb_img = LSB.decode_img(img)
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            plt.imshow(lsb_img)
            plt.axis('off')
            canvas.draw()

            scene2 = QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
            scene2.addWidget(canvas)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
            self.outputView_2.setScene(scene2)  # 第五步，把QGraphicsScene放入QGraphicsView
            self.outputView_2.show()
        elif method == "SteganoGAN":
            lsb_img = self.steganogan.decode_image(img)
            self.outputText.setText(lsb_img)

    def downImg(self):
        file_directory = QFileDialog.getExistingDirectory(None, "请选择文件夹路径", "D:/")
        if self.method == "LSB":
            self.output_img.save(file_directory + "/output.png")
        elif self.method == "SteganoGAN":
            imwrite(self.output_img, file_directory + "/output.png")
        print(file_directory)
        # return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = funcWindow()
    window.show()
    sys.exit(app.exec_())