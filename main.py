import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, exts):
    result = []
    for file in files:
        for ext in exts:
            if file.endswith(ext):
                result.append(file)
    return result
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimg.loadImage(filename)
        img_path = os.path.join(workdir, workimg.filename)
        workimg.showImage(img_path)
def showfilenameList():
    try:
        extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg']
        chooseWorkdir()
        filenames = filter(os.listdir(workdir), extensions)
        lw_files.clear()
        lw_files.addItems(filenames)
    except:
        message('Картинка не выбрана')
        
def message(text):
    msg =QMessageBox()
    msg.setWindowTitle('Ошибка')
    msg.setText(text)
    msg.exec
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = '/Modified'

    def loadImage(self, filename):
        self.filename = filename
        img_path = os.path.join(workdir, self.filename)
        self.image = Image.open(img_path)
    def showImage(self, path):
        lb_img.hide()
        pixmapimg = QPixmap(path)
        w, h = lb_img.width(), lb_img.height()
        pixmapimg = pixmapimg.scaled(w, h, Qt.KeepAspectRatio)
        lb_img.setPixmap(pixmapimg)
        lb_img.show()
    def do_bw(self):
        try:
            self.image = self.image.convert('L')
            self.saveImage()
            img_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(img_path)
        except:
                message('Картинка не выбрана')
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        img_path = os.path.join(path, self.filename)
        self.image.save(img_path)
    def rotateImage_L(self):
        try:
            self.image=self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            img_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(img_path)
        except:
            message('Картинка не выбрана')
    def rotateImage_R(self):
        try:
            self.image=self.image.transpose(Image.ROTATE_270)
            self.saveImage()
            img_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(img_path)
        except:
            message('Картинка не выбрана')
    def blurImage(self):
        try:   
            self.image= self.image.filter(ImageFilter.BLUR)
            self.saveImage()
            img_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(img_path)
        except:
            message('Картинка не выбрана')
    def flipImage(self):
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            img_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(img_path)
        except:
            message('Картинка не выбрана')
app = QApplication([])
mw = QWidget()
mw.setWindowTitle('Easy Editor')
mw.resize(700, 500)
lb_img = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкозть')
btn_bw = QPushButton('Ч/Б')
row_line = QHBoxLayout() # основная линия
col1 = QVBoxLayout() # колонна 1
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2 = QVBoxLayout() # колонна 2
col2.addWidget(lb_img, 95)
row_tools = QHBoxLayout() # линия кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row_line.addLayout(col1, 20)
row_line.addLayout(col2, 80)
mw.setLayout(row_line)
workimg = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showfilenameList)
btn_bw.clicked.connect(workimg.do_bw)
btn_left.clicked.connect(workimg.rotateImage_L)
btn_right.clicked.connect(workimg.rotateImage_R)
btn_sharp.clicked.connect(workimg.blurImage)
btn_flip.clicked.connect(workimg.flipImage)
mw.show()
app.exec_()