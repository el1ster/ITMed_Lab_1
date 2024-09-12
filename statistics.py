from db_actions import get_connection


def count_equipment_by_status(status):
    """Функція для підрахунку обладнання за статусом."""
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM Equipment WHERE status = %s"
    cursor.execute(query, (status,))
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count


def count_equipment_by_type(type_id):
    """Функція для підрахунку обладнання за типом."""
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM Equipment WHERE type_id = %s"
    cursor.execute(query, (type_id,))
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count
