import streamlit as st
import pandas as pd
import requests
import schedule
import time
import threading
import datetime

# Telegram Bot credentials
BOT_TOKEN = st.secrets["telegram"]["BOT_TOKEN"]
CHAT_ID = st.secrets["telegram"]["CHAT_ID"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    return response.status_code == 200


def check_timetable():
    current_time = datetime.datetime.now().strftime("%H:%M")
    try:
        df = pd.read_csv("timetable.csv")
        for _, row in df.iterrows():
            if row["Time"] == current_time:
                send_telegram_message(f"⏰ Reminder: {row['Task']} at {row['Time']}")
    except:
        pass

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)


# Schedule the checker every minute
schedule.every(1).minute.do(check_timetable)
thread = threading.Thread(target=run_schedule)
thread.daemon = True
thread.start()

# Streamlit App UI
st.title("📅 Timetable App with Telegram Alerts")

with st.form("task_form"):
    task = st.text_input("Enter Task")
    time_input = st.text_input("Enter time in 24hr format (HH:MM)")
    submitted = st.form_submit_button("Add Task")

if submitted:
    new_entry = {"Task": task, "Time": time_input.strip()}
    try:
        df = pd.read_csv("timetable.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Task", "Time"])

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("timetable.csv", index=False)
    st.success(f"Task '{task}' scheduled at {time_input.strip()}")

st.subheader("📋 Your Timetable")
try:
    df = pd.read_csv("timetable.csv")
    st.dataframe(df)
except:
    st.write("No tasks added yet.")
