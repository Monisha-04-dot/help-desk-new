import streamlit as st
from gpt_helper import ask_gpt
from text_to_speech import speak
from translator import detect_language, translate_to_english, translate_from_english
from doctor_service import get_all_doctors
from connection import get_connection


# -----------------------------
# Fetch Departments from DB
# -----------------------------
def fetch_departments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM departments")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# -----------------------------
# Streamlit UI Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Hospital Helpdesk",
    layout="centered"
)

st.title("🏥 AI Powered Government Hospital Helpdesk")
st.write("Ask about doctors, departments, availability, or services.")


# -----------------------------
# User Input
# -----------------------------
user_input = st.text_input("Enter your question:")


if st.button("Submit") and user_input:

    try:
        # 1️⃣ Detect User Language
        user_lang = detect_language(user_input)

        # 2️⃣ Translate to English (for AI reasoning)
        english_input = translate_to_english(user_input)

        # 3️⃣ Fetch Hospital Data
        doctors = get_all_doctors()
        departments = fetch_departments()

        # 4️⃣ Build Database Context for Grok
        db_context = "Doctors:\n"
        for d in doctors:
            db_context += (
                f"{d['name']} ({d['department']}) - "
                f"{d['available_days']} {d['available_time']}\n"
            )

        db_context += "\nDepartments:\n"
        for dep in departments:
            db_context += (
                f"{dep['name']} - Location: "
                f"{dep.get('location', 'N/A')}\n"
            )

        # 5️⃣ Prepare Prompt for Grok
        prompt = (
            f"User asked: '{english_input}'.\n"
            f"Hospital Information:\n{db_context}\n"
            "Answer ONLY what is relevant. Be short and clear."
        )

        # 6️⃣ Get AI Response (English)
        ai_response_en = ask_gpt(prompt)

        # 7️⃣ Translate Back to Original Language
        final_response = translate_from_english(ai_response_en, user_lang)

        # 8️⃣ Display Result in UI
        st.success(final_response)

        # 9️⃣ Speak Response
        speak(final_response, lang=user_lang)

    except Exception:
        st.warning("⚠️ System temporarily unavailable. Please try again later.")