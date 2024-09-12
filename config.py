# config.py

import logging

# Налаштування для підключення до бази даних
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 8772,
    'user': 'root',
    'password': 'Qwant_8772_5033',
    'database': 'MedicalEquipmentDB'
}

# Кольорова схема для інтерфейсу
COLOR_SCHEME = {
    'window_bg': '#E0F7FA',
    'window_text': '#000000',
    'button_bg': '#80CBC4',
    'button_text': '#000000',
    'table_bg': '#FFFFFF',
    'table_alt_bg': '#F1F8E9',
    'highlight_bg': '#4DB6AC',
}

# Налаштування логування
LOGGING_CONFIG = {
    'filename': 'medical_equipment.log',
    'level': logging.DEBUG,  # Записувати всі події (DEBUG і вище)
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}
