from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QWidget, QRadioButton, QComboBox, QSlider, QLabel, QLineEdit, QCheckBox, QButtonGroup
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from utils import convert_cv_qt
from os import sep

class MyGUI:

    def __init__(self, images = []):
        self.IMAGE_FILES = images
        self.window = QWidget()
        self.window.setWindowTitle("Face detection")


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
        self.window.setLayout(self.main_layout)


    def get_main(self):
        return self.window

    def add_method_selected_handler(self, handler):
        self.method_1.toggled.connect(lambda:handler(self.method_1))
        self.method_2.toggled.connect(lambda:handler(self.method_2))

    def add_input_selected_handler(self, handler):
        self.input_1.toggled.connect(lambda:handler(self.input_1))
        self.input_2.toggled.connect(lambda:handler(self.input_2))

    def add_img_cb_handler(self, handler):
        "handler(i)"
        self.selected_image_cb.currentIndexChanged.connect(handler)

    def update_img(self, cv_img):
        """Updates the image with a new opencv image"""
        qt_img = convert_cv_qt(cv_img, 600, 600)
        self.img_label.setPixmap(qt_img)
