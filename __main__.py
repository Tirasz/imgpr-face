from pathlib import Path
from PyQt5.QtWidgets import QApplication
from gui import MyGUI
import cv2
import sys
from itertools import chain

IMAGES_PATH = Path(Path(__file__).parent / 'imgs')
IMAGE_FILES = [f for f in chain(IMAGES_PATH.glob('*.jpg'), IMAGES_PATH.glob('*.jpeg'), IMAGES_PATH.glob('*.png'))]
APP = QApplication([])
GUI = MyGUI(IMAGE_FILES)
SELECTED_METHOD = "Method 1"
LAST_INDEX = 0
# CAPTURE_DEVICE = cv2.VideoCapture(0)


def update_image():
    global LAST_INDEX, GUI, SELECTED_METHOD
    img_BGR = cv2.imread(str(IMAGE_FILES[LAST_INDEX]), cv2.IMREAD_COLOR)
    GUI.update_img(img_BGR)

def img_select(i):
    # called when select image cb changes
    global LAST_INDEX
    LAST_INDEX = i
    update_image()

def select_method(b):
    global SELECTED_METHOD
    if b.isChecked():
        SELECTED_METHOD = b.text()
        print(f"SELECTED METHOD: {SELECTED_METHOD}")
        update_image()

def select_input(b):
    if b.isChecked():
        print(f"{b.text()}")


    

if __name__ == "__main__":
    print(f"Loaded {len(IMAGE_FILES)} test images.")
    update_image()
    GUI.get_main().show()
    GUI.add_img_cb_handler(img_select)
    GUI.add_method_selected_handler(select_method)
    GUI.add_input_selected_handler(select_input)

sys.exit(APP.exec_())