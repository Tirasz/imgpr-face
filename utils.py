import cv2

def convert_cv_qt(cv_img, display_width, display_height):
    """Convert and scale from an opencv (BGR) image to QPixmap"""
    from PyQt5.QtGui import QPixmap, QImage
    from PyQt5.QtCore import Qt

    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)