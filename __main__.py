from pathlib import Path
from PyQt5.QtWidgets import QApplication


IMAGES_PATH = Path(__file__).parent / 'imgs'
IMAGE_FILES =  tuple(Path(f) for f in IMAGES_PATH.glob('*.jpg'))




