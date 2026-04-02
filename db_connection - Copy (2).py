# db_connection.py - dummy for testing without MySQL
def fetch_doctors():
    return [
        {"name": "Dr. Ravi", "department": "Cardiology", "available_days": "Mon-Fri", "available_time": "10AM-2PM"},
        {"name": "Dr. Meena", "department": "Neurology", "available_days": "Tue-Thu", "available_time": "1PM-5PM"}
    ]

def fetch_departments():
    return [
        {"name": "Cardiology", "location": "Floor 1"},
        {"name": "Neurology", "location": "Floor 2"}
    ]

def book_appointment(patient, doctor, date, time):
    # just print instead of writing to DB
    print(f"Booked appointment: {patient} with {doctor} on {date} at {time}")
    return "Appointment booked successfully"
