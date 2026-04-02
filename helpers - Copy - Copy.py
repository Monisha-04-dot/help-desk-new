from datetime import datetime


# -----------------------------
# 1️⃣ Format Date
# -----------------------------
def format_date(date_obj):
    """
    Converts date object to YYYY-MM-DD format
    """
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%Y-%m-%d")


# -----------------------------
# 2️⃣ Format Time
# -----------------------------
def format_time(time_obj):
    """
    Converts time object to HH:MM:SS format
    """
    if isinstance(time_obj, str):
        return time_obj
    return time_obj.strftime("%H:%M:%S")


# -----------------------------
# 3️⃣ Calculate Available Beds
# -----------------------------
def calculate_available_beds(total, occupied):
    if occupied > total:
        return 0
    return total - occupied


# -----------------------------
# 4️⃣ Clean User Text
# -----------------------------
def clean_text(text):
    if not text:
        return ""
    return text.strip().lower()


# -----------------------------
# 5️⃣ Validate Appointment Time
# -----------------------------
def is_valid_time_range(selected_time, start_time, end_time):
    """
    Checks if selected time is within doctor's available time
    """
    return start_time <= selected_time <= end_time


# -----------------------------
# 6️⃣ Generate Simple Greeting
# -----------------------------
def generate_greeting():
    hour = datetime.now().hour

    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"
