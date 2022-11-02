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





if __name__ == "__main__":
    print(f"Loaded {len(IMAGE_FILES)} test images.")
    GUI.show()

sys.exit(APP.exec_())