if intent == "doctor_availability":
    doctors = fetch_doctors()

    # Filter doctors based on department keywords in user query
    user_input_lower = translated.lower()
    department_keywords = ["cardio", "neuro", "ortho", "pedia", "derma"]  # add more as needed

    filtered_doctors = []
    for doc in doctors:
        for kw in department_keywords:
            if kw in user_input_lower and kw in doc['department'].lower():
                filtered_doctors.append(doc)

    # If no keywords matched, show all doctors
    if filtered_doctors:
        doctors_to_show = filtered_doctors
    else:
        doctors_to_show = doctors

    response = "Available Doctors:\n"
    for doc in doctors_to_show:
        response += f"{doc['name']} ({doc['department']}) - {doc['available_days']} {doc['available_time']}\n"



