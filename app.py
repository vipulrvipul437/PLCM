import streamlit as st

st.title("AgriMotion Tractor Fleet Tracker")

# Sample data
tractors_db = {
    "TRAC-001": {
        "model": "AgriMotion 50HP",
        "owner": "Ramesh Kumar",
        "status": "active",
        "location": "Mysuru (12.2958, 76.6394)",
        "engine_hours": 420.5,
    },
    "TRAC-002": {
        "model": "AgriMotion 75HP Turbo",
        "owner": "Suresh Patel",
        "status": "idle",
        "location": "Mysuru (12.3050, 76.6500)",
        "engine_hours": 185.0,
    }
}

# Display fleet UI
st.subheader("Fleet Overview")
for tid, info in tractors_db.items():
    with st.expander(f"{tid} - {info['model']}"):
        st.write(f"**Owner:** {info['owner']}")
        st.write(f"**Status:** {info['status']}")
        st.write(f"**Location:** {info['location']}")
        st.write(f"**Engine Hours:** {info['engine_hours']}")
