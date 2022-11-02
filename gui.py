from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QWidget, QRadioButton, QComboBox, QSlider, QLabel, QLineEdit, QCheckBox, QButtonGroup
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from utils import convert_cv_qt
from os import sep

import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

CAPTURE_DEVICE = cv2.VideoCapture(0)

class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def run(self):

        
        while True:
            ret, frame = CAPTURE_DEVICE.read()
            if ret and self.selected_input:
                self.changePixmap.emit(convert_cv_qt(frame, 600, 600))
            else:
                img_BGR = cv2.imread(str(self.images[self.selected_image]), cv2.IMREAD_COLOR)
                self.changePixmap.emit(convert_cv_qt(img_BGR, 600, 600))



class MyGUI(QWidget):

    def _init_layout(self):
        # LAYOUTS
        self.main_layout = QVBoxLayout()
        self.options_layout = QHBoxLayout()
        self.images_layout = QHBoxLayout()

        # SELECT IMAGE COMBO BOX
        self.selected_image_cb = QComboBox()
        self.selected_image_cb.addItems([str(x).split(sep)[-1] for x in self.IMAGE_FILES])
        #self.selected_image_cb.currentIndexChanged.connect(self.select_image)
        self.options_layout.addWidget(self.selected_image_cb)

        # SELECT METHOD RADIO BUTTONS
        self.method_selector_group = QButtonGroup()
        self.method_1 = QRadioButton("Method 1")
        self.method_1.setChecked(True)
        self.method_2 = QRadioButton('Method 2')
        self.method_selector_group.addButton(self.method_1)
        self.method_selector_group.addButton(self.method_2)

        # SELECT INPUT RADIO BUTTONS
        self.input_selector_group = QButtonGroup()
        self.input_1 = QRadioButton("Image files")
        self.input_1.setChecked(True)
        self.input_2 = QRadioButton('Camera')
        self.input_selector_group.addButton(self.method_1)
        self.input_selector_group.addButton(self.method_2)

        # ADDING SELECTORS TO OPTIONS LAYOUT
        self.options_layout.addWidget(self.method_1)
        self.options_layout.addWidget(self.method_2)
        self.options_layout.addWidget(self.input_1)
        self.options_layout.addWidget(self.input_2)

        # ADDING IMAGE LABEL TO IMAGES LAYOUT
        self.img_label = QLabel()
        self.images_layout.addWidget(self.img_label)

        # ADDING OPTIONS AND IMAGES LAYOUTS TO MAIN LAYOUT
        self.main_layout.addLayout(self.options_layout)
        self.main_layout.addLayout(self.images_layout)

        # SETTING THE MAIN LAYOUT AS THE WINDOWS LAYOUT
        self.setLayout(self.main_layout)

    def __init__(self, images = []):
        super().__init__()
        self.IMAGE_FILES = images
        self.setWindowTitle("Face detection")
        self._init_layout()

        self.selected_image_cb.currentIndexChanged.connect(self.select_image)
        self.input_1.toggled.connect(self.select_input)
        self.th = Thread(self)
        self.th.images = images
        self.th.selected_image = 0
        self.th.selected_input = 0
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def select_input(self):
        if self.input_1.isChecked():
            self.th.selected_input = 0
        else:
            self.th.selected_input = 1

    def select_image(self, index):
        self.th.selected_image = index

    @pyqtSlot(QPixmap)
    def setImage(self, image):
        self.img_label.setPixmap(image)
