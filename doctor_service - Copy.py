from connection import get_connection


def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM doctors
        WHERE on_leave = FALSE
    """

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_doctors_by_department(department_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM doctors
        WHERE department = %s
        AND on_leave = FALSE
    """

    cursor.execute(query, (department_name,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

