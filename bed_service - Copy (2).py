from connection import get_connection


def get_bed_status():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, ward_type, total_beds, occupied_beds
        FROM beds
    """

    cursor.execute(query)
    beds = cursor.fetchall()

    cursor.close()
    conn.close()

    return beds

