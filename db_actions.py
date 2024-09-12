import mysql.connector
import logging
from config import DATABASE_CONFIG, LOGGING_CONFIG

# Налаштування логування
logging.basicConfig(filename=LOGGING_CONFIG['filename'], level=LOGGING_CONFIG['level'], format=LOGGING_CONFIG['format'])


def get_connection():
    """Функція для підключення до бази даних з використанням налаштувань з конфігурації."""
    try:
        connection = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        logging.info("Підключення до бази даних успішне")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Помилка підключення до бази даних: {err}")
        raise


def load_equipment_data():
    """Функція для завантаження даних з бази даних."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT e.name, t.type_name, l.location_name, e.status 
        FROM Equipment e
        JOIN EquipmentTypes t ON e.type_id = t.type_id
        JOIN StorageLocations l ON e.location_id = l.location_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        logging.info("Дані успішно завантажені з бази")
        return results
    except Exception as e:
        logging.error(f"Помилка завантаження даних: {e}")
        return []


def add_equipment(name, type_id, location_id, status):
    """Функція для додавання нового обладнання."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "INSERT INTO Equipment (name, type_id, location_id, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, type_id, location_id, status))

        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f"Додано нове обладнання: {name}")
    except Exception as e:
        logging.error(f"Помилка додавання обладнання: {e}")


def delete_equipment(equipment_id):
    """Функція для видалення обладнання за його ID."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "DELETE FROM Equipment WHERE equipment_id = %s"
        cursor.execute(query, (equipment_id,))

        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f"Обладнання з ID {equipment_id} успішно видалено")
    except Exception as e:
        logging.error(f"Помилка видалення обладнання: {e}")


def update_equipment(equipment_id, name, type_id, location_id, status):
    """Функція для редагування обладнання."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "UPDATE Equipment SET name = %s, type_id = %s, location_id = %s, status = %s WHERE equipment_id = %s"
        cursor.execute(query, (name, type_id, location_id, status, equipment_id))

        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f"Обладнання з ID {equipment_id} успішно оновлено")
    except Exception as e:
        logging.error(f"Помилка оновлення обладнання: {e}")
