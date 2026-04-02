import streamlit as st
from connection import get_connection

st.title("🏥 Hospital Admin Panel")

menu = st.sidebar.selectbox("Admin Options", [
    "Add Department",
    "Add Doctor",
    "Update Doctor Status",
    "Update Bed Availability",
    "View Appointments"
])

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# ----------------------------
# 1️⃣ ADD DEPARTMENT
# ----------------------------
if menu == "Add Department":
    st.subheader("Add New Department")

    name = st.text_input("Department Name")
    location = st.text_input("Location")

    if st.button("Add Department"):
        query = "INSERT INTO departments (name, location) VALUES (%s, %s)"
        cursor.execute(query, (name, location))
        conn.commit()
        st.success("Department Added Successfully")


# ----------------------------
# 2️⃣ ADD DOCTOR
# ----------------------------
elif menu == "Add Doctor":
    st.subheader("Add New Doctor")

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    dept_dict = {dept['name']: dept['id'] for dept in departments}

    name = st.text_input("Doctor Name")
    dept_name = st.selectbox("Department", list(dept_dict.keys()))
    specialization = st.text_input("Specialization")
    experience = st.number_input("Experience (Years)", min_value=0)
    fee = st.number_input("Consultation Fee", min_value=0.0)
    available_from = st.time_input("Available From")
    available_to = st.time_input("Available To")
    working_days = st.text_input("Working Days (e.g., Mon-Fri)")

    if st.button("Add Doctor"):
        query = """
        INSERT INTO doctors 
        (name, department_id, specialization, experience_years, consultation_fee,
         available_from, available_to, working_days, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'active')
        """

        cursor.execute(query, (
            name,
            dept_dict[dept_name],
            specialization,
            experience,
            fee,
            available_from,
            available_to,
            working_days
        ))

        conn.commit()
        st.success("Doctor Added Successfully")


# ----------------------------
# 3️⃣ UPDATE DOCTOR STATUS
# ----------------------------
elif menu == "Update Doctor Status":
    st.subheader("Update Doctor Status")

    cursor.execute("SELECT id, name FROM doctors")
    doctors = cursor.fetchall()

    doctor_dict = {doc['name']: doc['id'] for doc in doctors}

    doctor_name = st.selectbox("Select Doctor", list(doctor_dict.keys()))
    new_status = st.selectbox("Status", ["active", "on_leave"])

    if st.button("Update Status"):
        query = "UPDATE doctors SET status=%s WHERE id=%s"
        cursor.execute(query, (new_status, doctor_dict[doctor_name]))
        conn.commit()
        st.success("Doctor Status Updated")


# ----------------------------
# 4️⃣ UPDATE BED AVAILABILITY
# ----------------------------
elif menu == "Update Bed Availability":
    st.subheader("Update Bed Information")

    cursor.execute("""
        SELECT b.id, d.name AS department, b.total_beds, b.occupied_beds 
        FROM beds b
        JOIN departments d ON b.department_id = d.id
    """)
    beds = cursor.fetchall()

    bed_dict = {f"{b['department']}": b['id'] for b in beds}

    dept_name = st.selectbox("Select Department", list(bed_dict.keys()))
    total = st.number_input("Total Beds", min_value=0)
    occupied = st.number_input("Occupied Beds", min_value=0)

    if st.button("Update Beds"):
        available = total - occupied

        query = """
        UPDATE beds 
        SET total_beds=%s, occupied_beds=%s, available_beds=%s 
        WHERE id=%s
        """

        cursor.execute(query, (total, occupied, available, bed_dict[dept_name]))
        conn.commit()
        st.success("Bed Data Updated")


# ----------------------------
# 5️⃣ VIEW APPOINTMENTS
# ----------------------------
elif menu == "View Appointments":
    st.subheader("All Appointments")

    cursor.execute("""
        SELECT a.id, a.patient_name, d.name AS doctor,
               a.appointment_date, a.appointment_time, a.status
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
    """)

    appointments = cursor.fetchall()
    st.table(appointments)


conn.close()
