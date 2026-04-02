from connection import get_connection


def get_available_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, name FROM doctors WHERE on_leave = FALSE"
    cursor.execute(query)

    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    return doctors


def book_appointment(patient_name, doctor_id, date, time):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Check if doctor exists and not on leave
        cursor.execute(
            "SELECT on_leave FROM doctors WHERE id = %s",
            (doctor_id,)
        )
        doctor = cursor.fetchone()

        if not doctor:
            return "Doctor not found ❌"

        if doctor[0]:  # on_leave = TRUE
            return "Doctor is currently on leave ❌"

        # 2️⃣ Check if slot already booked
        cursor.execute(
            """
            SELECT * FROM appointments 
            WHERE doctor_id = %s 
            AND appointment_date = %s 
            AND appointment_time = %s
            """,
            (doctor_id, date, time)
        )

        existing = cursor.fetchone()

        if existing:
            return "Slot already booked ❌ Please choose another time."

        # 3️⃣ Insert appointment
        insert_query = """
            INSERT INTO appointments 
            (patient_name, doctor_id, appointment_date, appointment_time)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (patient_name, doctor_id, date, time))
        conn.commit()

        return "Appointment booked successfully ✅"

    except Exception as e:
        return f"Error occurred: {str(e)}"

    finally:
        cursor.close()
        conn.close()
