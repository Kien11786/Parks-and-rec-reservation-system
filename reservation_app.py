import streamlit as st
import pandas as pd
import datetime

# Load and clean data
df = pd.read_csv("Park_schedule.csv")
df = df[df["date"] != "date"]  # Remove stray header rows if duplicated
df["date"] = pd.to_datetime(df["date"]).dt.date  # Convert to date objects

# Set page config
st.set_page_config(page_title="City Connect", layout="centered")
st.markdown("## 🌟 City Connect")

# --- Contact Information ---
st.subheader("👤🧳 Your Contact Information")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# --- Reservation Details ---
st.subheader("📍 Reservation Details")
parks = df["park_name"].unique()
selected_park = st.selectbox("Choose a park:", parks)

available_dates = df[(df["park_name"] == selected_park) & (df["status"] == "available")]["date"].unique()
selected_date = st.date_input("Choose a date:", min_value=datetime.date.today())

slots_df = df[(df["park_name"] == selected_park) & 
              (df["date"] == selected_date) & 
              (df["status"] == "available")]

available_slots = slots_df["time_slot"].tolist()
selected_slot = st.selectbox("Choose a time slot:", available_slots if available_slots else ["No options available"])

# Book button
if st.button("✅ Book Now") and selected_slot != "No options available":
    df.loc[
        (df["park_name"] == selected_park) & 
        (df["date"] == selected_date) & 
        (df["time_slot"] == selected_slot),
        "status"
    ] = "booked"
    df.to_csv("Park_schedule.csv", index=False)
    st.success(f"Reservation confirmed for {selected_park} on {selected_date} at {selected_slot}!")
    st.info("You will receive a confirmation email shortly (mock only).")

# View Bookings
with st.expander("📂 View All Bookings"):
    st.dataframe(df)

# --- Park Amenities Filter ---
st.header("📊 Park Data Insights & Filter")
st.subheader("🔍 Filter Parks by Amenities")
parks_df = pd.read_csv("Park_amenities.csv")

# Filter checkboxes
bbq = st.checkbox("Must have BBQ")
court = st.checkbox("Must have Basketball Court")
playground = st.checkbox("Must have Playground")
restroom = st.checkbox("Must have Restroom")
tennis = st.checkbox("Must have Tennis Courts")
volleyball = st.checkbox("Must have Volleyball")
skate = st.checkbox("Must have Skate Park")
soccer = st.checkbox("Must have Soccer Field")
pickleball = st.checkbox("Must have Pickleball")

# Apply filters dynamically
filtered = parks_df[
    (~bbq | parks_df["Has BBQ"]) &
    (~court | parks_df["Has Basketball Court"]) &
    (~playground | parks_df["Has Playground"]) &
    (~restroom | parks_df["Has Restroom"]) &
    (~tennis | parks_df["Has Tennis Courts"]) &
    (~volleyball | parks_df["Has Volleyball"]) &
    (~skate | parks_df["Has Skate Park"]) &
    (~soccer | parks_df["Has Soccer Field"]) &
    (~pickleball | parks_df["Has Pickleball"])
]

st.dataframe(filtered)

# --- Park Issue Reporting ---
st.subheader("🚨 Park Issue Reporting")
issue_description = st.text_area("Describe the issue you're experiencing:")
issue_type = st.selectbox("Issue type:", ["Litter", "Damaged Equipment", "Graffiti", "Other"])
issue_park = st.selectbox("Which park?", df["park_name"].unique())

if st.button("📋 Submit Report"):
    st.success("Your issue has been submitted. Thank you for helping improve our parks!")

# --- Optional: Chatbot (Footer Only) ---
user_input = st.chat_input("Ask a question about park rules, hours, or reservations...", key="chat_input_key")
if user_input:
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write("Chatbot response coming soon... (API not connected)")
