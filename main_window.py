import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QSizePolicy)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Импортируем итератор из второй лабораторной работы
try:
    from lab2 import ImagePathIterator  # Если сохранен как lab2_code.py
except ImportError as e:
    raise Exception(f"Ошибка при импортировании лабораторной 2 {e}")

def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()