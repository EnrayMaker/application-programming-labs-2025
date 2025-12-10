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

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_iterator = None
        self.current_image_path = None
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Просмотрщик датасета изображений")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Панель управления (кнопки выбора)
        control_panel = QHBoxLayout()
        
        # Кнопка выбора папки
        self.btn_select_folder = QPushButton("Выбрать папку с изображениями")
        self.btn_select_folder.clicked.connect(self.select_folder)
        control_panel.addWidget(self.btn_select_folder)
        
        # Кнопка выбора файла аннотации
        self.btn_select_annotation = QPushButton("Выбрать файл аннотации")
        self.btn_select_annotation.clicked.connect(self.select_annotation)
        control_panel.addWidget(self.btn_select_annotation)
        
        main_layout.addLayout(control_panel)
        
        # Метка для отображения информации
        self.lbl_info = QLabel("Выберите папку с изображениями или файл аннотации")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_info)
        
        # Метка для отображения изображения
        self.lbl_image = QLabel()
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_image.setMinimumSize(400, 300)
        self.lbl_image.setStyleSheet("border: 2px solid #cccccc; background-color: #f0f0f0;")
        main_layout.addWidget(self.lbl_image)
        
        # Панель навигации
        nav_panel = QHBoxLayout()
        
        # Кнопка предыдущего изображения
        self.btn_prev = QPushButton("← Предыдущее")
        self.btn_prev.clicked.connect(self.show_previous_image)
        self.btn_prev.setEnabled(False)
        nav_panel.addWidget(self.btn_prev)
        
        # Кнопка следующего изображения
        self.btn_next = QPushButton("Следующее →")
        self.btn_next.clicked.connect(self.show_next_image)
        self.btn_next.setEnabled(False)
        nav_panel.addWidget(self.btn_next)
        
        main_layout.addLayout(nav_panel)
        
        # Статусная строка
        self.statusBar().showMessage("Готово")
        
    def select_folder(self):
        """Выбор папки с изображениями"""
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        if folder_path:
            try:
                self.image_iterator = ImagePathIterator(folder_path=folder_path)
                self.lbl_info.setText(f"Загружено изображений: {len(self.image_iterator)}")
                self.btn_next.setEnabled(True)
                self.btn_prev.setEnabled(True)
                self.statusBar().showMessage(f"Папка выбрана: {folder_path}")
                self.show_next_image()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображения: {e}")
                
    def select_annotation(self):
        """Выбор файла аннотации"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл аннотации", 
            "", 
            "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_path:
            try:
                self.image_iterator = ImagePathIterator(annotation_file=file_path)
                self.lbl_info.setText(f"Загружено изображений: {len(self.image_iterator)}")
                self.btn_next.setEnabled(True)
                self.btn_prev.setEnabled(True)
                self.statusBar().showMessage(f"Аннотация выбрана: {file_path}")
                self.show_next_image()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить аннотацию: {e}")
    
    def show_next_image(self):
        """Показать следующее изображение"""
        if self.image_iterator and len(self.image_iterator) > 0:
            try:
                # Если дошли до конца - начинаем сначала
                if self.image_iterator.current_index >= len(self.image_iterator.file_paths):
                    self.image_iterator.current_index = 0
                
                # Получаем путь к следующему изображению
                if self.image_iterator.current_index < len(self.image_iterator.file_paths):
                    self.current_image_path = self.image_iterator.file_paths[self.image_iterator.current_index]
                    self.image_iterator.current_index += 1
                    
                    # Загружаем и отображаем изображение
                    self.display_image(self.current_image_path)
                    
                    # Обновляем информацию
                    self.lbl_info.setText(
                        f"Изображение {self.image_iterator.current_index} из {len(self.image_iterator)}"
                    )
                    self.statusBar().showMessage(f"Файл: {os.path.basename(self.current_image_path)}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение: {e}")
    
    def show_previous_image(self):
        """Показать предыдущее изображение"""
        if self.image_iterator and len(self.image_iterator) > 0:
            try:
                # Переходим на предыдущее изображение
                if self.image_iterator.current_index > 1:
                    self.image_iterator.current_index -= 2
                else:
                    # Если мы на первом изображении - переходим к последнему
                    self.image_iterator.current_index = len(self.image_iterator.file_paths) - 1
                
                if self.image_iterator.current_index >= 0:
                    self.current_image_path = self.image_iterator.file_paths[self.image_iterator.current_index]
                    self.image_iterator.current_index += 1
                    
                    # Загружаем и отображаем изображение
                    self.display_image(self.current_image_path)
                    
                    # Обновляем информацию
                    self.lbl_info.setText(
                        f"Изображение {self.image_iterator.current_index} из {len(self.image_iterator)}"
                    )
                    self.statusBar().showMessage(f"Файл: {os.path.basename(self.current_image_path)}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение: {e}")
    
    def display_image(self, image_path: str) -> None:
        """
        Отображает изображение исходного размера или меньшего размера с сохранением пропорций
        
        Args:
            image_path (str): Путь к файлу изображения
        """
        try:
            # Загружаем изображение
            pixmap = QPixmap(image_path)
            
            if pixmap.isNull():
                self.lbl_image.setText("Не удалось загрузить изображение")
                self.lbl_image.setPixmap(QPixmap())
                return
            
            # Получаем размеры виджета для отображения
            label_width = self.lbl_image.width()
            label_height = self.lbl_image.height()
            
            # Масштабируем изображение с сохранением пропорций
            scaled_pixmap = pixmap.scaled(
                label_width, 
                label_height, 
                Qt.KeepAspectRatio,  # Сохраняем пропорции
                Qt.SmoothTransformation  # Плавное масштабирование
            )
            
            # Устанавливаем изображение
            self.lbl_image.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.lbl_image.setText(f"Ошибка загрузки: {str(e)}")
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        # При изменении размера окна перерисовываем текущее изображение
        if self.current_image_path:
            self.display_image(self.current_image_path)


def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()