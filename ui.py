import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from db_actions import load_equipment_data, add_equipment, delete_equipment, update_equipment
from config import COLOR_SCHEME, LOGGING_CONFIG

# Налаштування логування
logging.basicConfig(filename=LOGGING_CONFIG['filename'], level=LOGGING_CONFIG['level'], format=LOGGING_CONFIG['format'])


class MedicalEquipmentApp(QWidget):
    def __init__(self):
        super().__init__()

        # Налаштування назви вікна та його розміру
        self.setWindowTitle('Облік медичного устаткування')
        self.setGeometry(100, 100, 800, 700)  # Ширина 800, висота 700

        # Налаштування кольорової схеми
        self.set_medical_style()

        # Створення макета
        self.layout = QVBoxLayout()

        # Кнопка для завантаження даних
        self.load_button = QPushButton('Завантажити дані')
        self.load_button.clicked.connect(self.load_data)

        # Кнопка для додавання нового запису
        self.add_button = QPushButton('Додати обладнання')
        self.add_button.clicked.connect(self.add_new_equipment)

        # Кнопка для видалення запису
        self.delete_button = QPushButton('Видалити вибране обладнання')
        self.delete_button.clicked.connect(self.delete_selected_equipment)

        # Кнопка для редагування запису
        self.edit_button = QPushButton('Редагувати вибране обладнання')
        self.edit_button.clicked.connect(self.edit_selected_equipment)

        # Таблиця для відображення даних
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Назва обладнання', 'Тип', 'Місце зберігання', 'Статус'])

        # Додавання елементів до макета
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def set_medical_style(self):
        """
        Налаштовує медичну кольорову схему для вікна та елементів з конфігурації.
        """
        palette = QPalette()

        # Фоновий колір для вікна
        palette.setColor(QPalette.Window, QColor(COLOR_SCHEME['window_bg']))  # Фон вікна

        # Колір тексту
        palette.setColor(QPalette.WindowText, QColor(COLOR_SCHEME['window_text']))  # Текст

        # Кольори для кнопок
        palette.setColor(QPalette.Button, QColor(COLOR_SCHEME['button_bg']))  # Фон кнопок
        palette.setColor(QPalette.ButtonText, QColor(COLOR_SCHEME['button_text']))  # Текст кнопок

        # Фон таблиці
        palette.setColor(QPalette.Base, QColor(COLOR_SCHEME['table_bg']))  # Білий фон таблиці
        palette.setColor(QPalette.AlternateBase,
                         QColor(COLOR_SCHEME['table_alt_bg']))  # Альтернативний фон рядків таблиці

        # Акцентний колір для вибраного елементу
        palette.setColor(QPalette.Highlight, QColor(COLOR_SCHEME['highlight_bg']))  # Акцентний колір

        # Встановлення палітри для вікна
        self.setPalette(palette)

    def load_data(self):
        try:
            # Виклик функції для завантаження даних із бази
            results = load_equipment_data()

            # Очищення таблиці
            self.table.setRowCount(0)

            # Додавання даних до таблиці
            for row_number, row_data in enumerate(results):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            # Автовирівнювання ширини стовпців по вмісту
            self.table.resizeColumnsToContents()

            logging.info("Дані успішно завантажені в інтерфейс")
        except Exception as e:
            logging.error(f"Помилка завантаження даних в інтерфейс: {e}")
            QMessageBox.critical(self, 'Помилка', 'Не вдалося завантажити дані')

    def add_new_equipment(self):
        try:
            add_equipment('Новий апарат', 1, 1, 'Використовується')
            self.load_data()
            logging.info("Додано нове обладнання через інтерфейс")
        except Exception as e:
            logging.error(f"Помилка додавання обладнання через інтерфейс: {e}")
            QMessageBox.critical(self, 'Помилка', 'Не вдалося додати нове обладнання')

    def delete_selected_equipment(self):
        try:
            # Отримання вибраного рядка
            selected_row = self.table.currentRow()
            if selected_row == -1:
                logging.warning("Не обрано рядок для видалення")
                QMessageBox.warning(self, 'Помилка', 'Оберіть запис для видалення.')
                return

            # Підтвердження видалення
            reply = QMessageBox.question(self, 'Підтвердження', 'Ви впевнені, що хочете видалити цей запис?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # Видалення запису з бази
                equipment_id = selected_row + 1  # Припущення: equipment_id збігається з індексом рядка
                delete_equipment(equipment_id)
                self.load_data()
                logging.info(f"Обладнання з ID {equipment_id} успішно видалено")
        except Exception as e:
            logging.error(f"Помилка видалення обладнання через інтерфейс: {e}")
            QMessageBox.critical(self, 'Помилка', 'Не вдалося видалити обладнання')

    def edit_selected_equipment(self):
        try:
            # Отримання вибраного рядка
            selected_row = self.table.currentRow()
            if selected_row == -1:
                logging.warning("Не обрано рядок для редагування")
                QMessageBox.warning(self, 'Помилка', 'Оберіть запис для редагування.')
                return

            # Отримання поточних значень
            equipment_id = selected_row + 1  # Припущення: equipment_id збігається з індексом рядка
            current_name = self.table.item(selected_row, 0).text()
            current_type = self.table.item(selected_row, 1).text()
            current_location = self.table.item(selected_row, 2).text()
            current_status = self.table.item(selected_row, 3).text()

            # Використання діалогів для отримання нових значень
            new_name, ok = QInputDialog.getText(self, 'Редагувати обладнання', 'Назва обладнання:', text=current_name)
            if not ok or not new_name:
                return

            new_type, ok = QInputDialog.getInt(self, 'Редагувати обладнання', 'Тип обладнання:',
                                               value=int(current_type))
            if not ok:
                return

            new_location, ok = QInputDialog.getInt(self, 'Редагувати обладнання', 'Місце зберігання:',
                                                   value=int(current_location))
            if not ok:
                return

            new_status, ok = QInputDialog.getText(self, 'Редагувати обладнання', 'Статус:', text=current_status)
            if not ok or not new_status:
                return

            # Оновлення запису в базі
            update_equipment(equipment_id, new_name, new_type, new_location, new_status)
            self.load_data()

            logging.info(f"Обладнання з ID {equipment_id} успішно відредаговано")
        except Exception as e:
            logging.error(f"Помилка редагування обладнання через інтерфейс: {e}")
            QMessageBox.critical(self, 'Помилка', 'Не вдалося редагувати обладнання')
