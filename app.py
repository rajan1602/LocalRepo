# import streamlit as st
# import requests

# st.title("🌿 Oxygen Impact Tracker")

# city = st.text_input("Enter your city:")

# if city:
#     url = f"http://api.openweathermap.org/data/2.5/air_pollution?appid=YOUR_API_KEY&lat=28.67&lon=77.22"  # You’ll need lat/lon
#     # Use separate API to convert city → lat/lon (or hardcode it for now)
    
#     st.write("Fetching AQI data...")
#     # Dummy AQI value for now
#     aqi = 120

#     st.metric("Air Quality Index (AQI)", aqi)

#     if aqi < 50:
#         st.success("Oxygen Level Normal 🌳")
#     elif aqi < 100:
#         st.warning("Slight Oxygen Drop ⚠️")
#     else:
#         st.error("Significant Oxygen Drop ❌\nTry using air purifiers or indoor plants!")



# import streamlit as st
# import pandas as pd
# import datetime
# import requests
# import time

# # Replace with your Pushbullet access token
# PUSHBULLET_TOKEN = "o.60OUjBRtJgU3GnGDxrApmbqRZPIF75yU"

# # Send Push Notification
# def send_notification(title, body):
#     data = {"type": "note", "title": title, "body": body}
#     res = requests.post(
#         'https://api.pushbullet.com/v2/pushes',
#         json=data,
#         headers={'Access-Token': PUSHBULLET_TOKEN}
#     )
#     return res.status_code == 200

# st.title("📅 Time Table + Notification App")

# # Input form
# with st.form("timetable_form"):
#     task = st.text_input("Enter Task/Subject")
#     task_time = st.time_input("Time to notify")
#     submit = st.form_submit_button("Add to Timetable")

# if submit:
#     df = pd.read_csv("timetable.csv") if "timetable.csv" in st.session_state else pd.DataFrame(columns=["Task", "Time"])
#     # Create a new DataFrame with the new row
#     new_row = pd.DataFrame([{"Task": task, "Time": task_time.strftime("%H:%M")}])

#     # Concatenate the new row to the original DataFrame
#     df = pd.concat([df, new_row], ignore_index=True)

#     df.to_csv("timetable.csv", index=False)
#     st.success("Task added!")

# # Show timetable
# st.subheader("📋 Your Time Table")
# try:
#     df = pd.read_csv("timetable.csv")
#     st.dataframe(df)
# except:
#     st.write("No tasks yet!")

# # Notification loop (run every 30s)
# current_time = datetime.datetime.now().strftime("%H:%M")
# try:
#     df = pd.read_csv("timetable.csv")
#     for i, row in df.iterrows():
#         if row["Time"] == current_time:
#             send_notification("📚 Time for your task!", f"Task: {row['Task']} at {row['Time']}")
#             st.success(f"Notification sent for: {row['Task']}")
# except:
#     pass




# import streamlit as st
# import pandas as pd
# import requests
# import schedule
# import time
# import threading
# import datetime

# # Replace with your Pushbullet access token
# PUSHBULLET_TOKEN = "o.60OUjBRtJgU3GnGDxrApmbqRZPIF75yU"

# # Function to send Push Notification
# def send_notification(title, body):
#     data = {"type": "note", "title": title, "body": body}
#     res = requests.post(
#         'https://api.pushbullet.com/v2/pushes',
#         json=data,
#         headers={'Access-Token': PUSHBULLET_TOKEN}
#     )
#     return res.status_code == 200

# # Function to check timetable and send notification
# def check_timetable():
#     current_time = datetime.datetime.now().strftime("%H:%M")
#     try:
#         df = pd.read_csv("timetable.csv")
#         for i, row in df.iterrows():
#             if row["Time"] == current_time:
#                 send_notification("📚 Time for your task!", f"Task: {row['Task']} at {row['Time']}")
#                 print(f"Notification sent for: {row['Task']}")
#     except:
#         pass

# # Function to run schedule in background
# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# # Set up scheduler to check for notifications every minute
# schedule.every(1).minute.do(check_timetable)

# # Start the scheduling thread
# thread = threading.Thread(target=run_schedule)
# thread.daemon = True
# thread.start()

# st.title("📅 Time Table + Notification App")

# # Input form for adding tasks
# with st.form("timetable_form"):
#     task = st.text_input("Enter Task/Subject")
#     task_time = st.time_input("Time to notify")
#     repeat_option = st.selectbox("Repeat?", ["None", "Daily", "Weekly"])
#     submit = st.form_submit_button("Add to Timetable")

# if submit:
#     # Read or create timetable CSV
#     df = pd.read_csv("timetable.csv") if "timetable.csv" in st.session_state else pd.DataFrame(columns=["Task", "Time", "Repeat"])
    
#     # Add new task to dataframe
#     # Create a new DataFrame with the new row
#     new_row = pd.DataFrame([{"Task": task, "Time": task_time.strftime("%H:%M")}])

#     # Concatenate the new row to the original DataFrame
#     df = pd.concat([df, new_row], ignore_index=True)

#     df.to_csv("timetable.csv", index=False)
#     st.success(f"Task '{task}' added at {task_time}.")

# # Display timetable
# st.subheader("📋 Your Time Table")
# try:
#     df = pd.read_csv("timetable.csv")
#     st.dataframe(df)
# except:
#     st.write("No tasks yet!")

import streamlit as st
import pandas as pd
import requests
import schedule
import time
import threading
import datetime

# Telegram Bot credentials
BOT_TOKEN = '7978328252:AAHviGrFM1MWMDmfLWhqsk9D64XtbyJMsWk'
CHAT_ID = '5738184404'

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
    time_input = st.time_input("Time (24hr format)")
    submitted = st.form_submit_button("Add Task")

if submitted:
    new_entry = {"Task": task, "Time": time_input.strftime("%H:%M")}
    try:
        df = pd.read_csv("timetable.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Task", "Time"])

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("timetable.csv", index=False)
    st.success(f"Task '{task}' scheduled at {time_input.strftime('%H:%M')}")

st.subheader("📋 Your Timetable")
try:
    df = pd.read_csv("timetable.csv")
    st.dataframe(df)
except:
    st.write("No tasks added yet.")
