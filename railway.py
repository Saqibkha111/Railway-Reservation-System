import streamlit as st
import pandas as pd
import random
from datetime import date

# --- Page Config ---
st.set_page_config(
    page_title="Railway Reservation System",  
    page_icon="🚆",                          
    layout="centered"
)


users = {
    "saqib": "khan"
}

# --- Helper Functions ---
def generate_pnr():
    return str(random.randint(1000000000, 9999999999))

def fare_calc(distance, seats):
    return distance * 0.5 * seats

# --- Train Data ---
trains = [
    {"train_no": "12952", "name": "Mumbai Rajdhani", "src": "NDLS", "dst": "BCT", "distance": 1384},
    {"train_no": "12301", "name": "Howrah Rajdhani", "src": "HWH", "dst": "NDLS", "distance": 1531},
    {"train_no": "12658", "name": "Chennai Mail", "src": "MAS", "dst": "SBC", "distance": 358},
    {"train_no": "12046", "name": "Chandigarh Shatabdi", "src": "NDLS", "dst": "CDG", "distance": 266},
    {"train_no": "11013", "name": "Coimbatore Express", "src": "LTT", "dst": "CBE", "distance": 1498},
    {"train_no": "22120", "name": "Nagpur Duronto", "src": "NGP", "dst": "CSTM", "distance": 837},
    {"train_no": "12802", "name": "Purushottam Express", "src": "NDLS", "dst": "BBS", "distance": 1796},
    {"train_no": "12424", "name": "Rajdhani Express", "src": "NDLS", "dst": "DBRG", "distance": 2279},
    {"train_no": "12627", "name": "Karnataka Express", "src": "SBC", "dst": "NDLS", "distance": 2391},
    {"train_no": "12277", "name": "Satabdi Express", "src": "HWH", "dst": "PNBE", "distance": 532},
]

# --- Session State ---
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "page" not in st.session_state:
    st.session_state.page = "Login" 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# --- App Title ---
st.title("🚆 Railway Reservation System")

# --- Login Page ---
if st.session_state.page == "Login":
    st.subheader("🔑 Login to Continue")
    uname = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if uname in users and users[uname] == pwd:
            st.session_state.logged_in = True
            st.session_state.username = uname
            st.success(f"✅ Welcome {uname}!")
            st.session_state.page = "View Trains"
        else:
            st.error("❌ Invalid Username or Password!")

# --- If Logged In Show Navbar ---
if st.session_state.logged_in:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("📋 View Trains"):
            st.session_state.page = "View Trains"
    with col2:
        if st.button("📝 Book Ticket"):
            st.session_state.page = "Book Ticket"
    with col3:
        if st.button("🎟 My Bookings"):
            st.session_state.page = "My Bookings"
    with col4:
        if st.button("❌ Cancel Ticket"):
            st.session_state.page = "Cancel Ticket"
    with col5:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Login"
            st.info("You have been logged out.")


# --- Content Switch ---
if st.session_state.logged_in:

    if st.session_state.page == "View Trains":
        st.subheader("📋 Available Trains")
        st.dataframe(pd.DataFrame(trains))

    elif st.session_state.page == "Book Ticket":
        st.subheader("📝 Book Your Ticket")

        train_choice = st.selectbox("Select Train", [f"{t['train_no']} - {t['name']} ({t['src']} ➝ {t['dst']})" for t in trains])
        train_map = {f"{t['train_no']} - {t['name']} ({t['src']} ➝ {t['dst']})": t for t in trains}
        sel = train_map[train_choice]

        pname = st.text_input("Passenger Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        seats = st.number_input("Seats", min_value=1, max_value=6, value=1)
        jdate = st.date_input("Journey Date", min_value=date.today())

        if st.button("Confirm Booking"):
            if pname.strip() == "":
                st.error("⚠️ Please enter passenger name!")
            else:
                pnr = generate_pnr()
                fare = fare_calc(sel["distance"], seats)
                booking = {
                    "PNR": pnr,
                    "Train": sel["name"],
                    "From": sel["src"],
                    "To": sel["dst"],
                    "Date": jdate.strftime("%Y-%m-%d"),
                    "Passenger": pname,
                    "Age": age,
                    "Seats": seats,
                    "Fare": fare
                }
                st.session_state.bookings.append(booking)
                st.success(f"✅ Ticket Booked Successfully! PNR: {pnr}")
                st.json(booking)

    elif st.session_state.page == "My Bookings":
        st.subheader("🎟 My Bookings")
        if st.session_state.bookings:
            st.dataframe(pd.DataFrame(st.session_state.bookings))
        else:
            st.info("No bookings found!")

    elif st.session_state.page == "Cancel Ticket":
        st.subheader("❌ Cancel Ticket")
        if st.session_state.bookings:
            pnrs = [b["PNR"] for b in st.session_state.bookings]
            pnr_choice = st.selectbox("Select PNR to cancel", pnrs)
            if st.button("Cancel Booking"):
                st.session_state.bookings = [b for b in st.session_state.bookings if b["PNR"] != pnr_choice]
                st.success(f"❌ Ticket with PNR {pnr_choice} cancelled.")
        else:
            st.info("No bookings available to cancel.")
