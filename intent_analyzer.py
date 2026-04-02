# intent_analyzer.py

def detect_intent(text):
    text = text.lower()

    # Book appointment intent
    if any(word in text for word in ["book", "appointment", "schedule", "consult", "meet doctor", "fix appointment"]):
        return "book_appointment"

    # Doctor availability query
    elif any(word in text for word in ["doctor", "available", "who is there", "consulting", "seeing patients"]):
        return "doctor_availability"

    # Department location query
    elif any(word in text for word in ["department", "where", "location", "floor", "ward"]):
        return "department_location"

    # Bed/ICU/ward query
    elif any(word in text for word in ["bed", "icu", "ward", "availability", "vacant"]):
        return "bed_query"

    else:
        return "unknown"

