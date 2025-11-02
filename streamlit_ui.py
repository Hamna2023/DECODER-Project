import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import json

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
API_BASE = "http://127.0.0.1:8000"

st.title("🏢 Mini-DECODER Dashboard")
st.markdown("This dashboard interacts with your FastAPI backend for data ingestion and forecasting.")

# --------------------------------------------------
# 1️⃣ Ingest Sensor Data
# --------------------------------------------------
st.subheader("📤 Ingest Sensor Data")

building_id = st.text_input("Building ID", "B001")
meter_type = st.text_input("Sensor ID", "S001")
value = st.number_input("Sensor Value", value=100.0)
timestamp = st.text_input("Timestamp", "2017-07-03 20:00:00")
sensor_for_forecast = st.text_input("📟 Meter ID", "S001")

if st.button("Send Data"):
 

    payload = {
        "building_id": building_id,
        "meter_type": meter_type,
        "timestamp": timestamp,
        "value": value,
    }

    st.write("📦 Sending payload:", json.dumps(payload, indent=2))  # optional debug

    try:
        res = requests.post(f"{API_BASE}/ingest", json=payload)
        st.write("🧭 Response text:", res.text)  # optional debug

        if res.status_code == 200:
            st.success("✅ Data ingested successfully!")
        else:
            st.error(f"⚠️ Failed: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"🚨 Error connecting to API: {e}")


# --------------------------------------------------
# 2️⃣ Get Forecast
# --------------------------------------------------
st.subheader("🔮 Forecast Sensor Data")

building_for_forecast = st.text_input("Building ID for Forecast", "B001")
meter_type_for_forecast = st.selectbox(
    "⚙️ Meter Type",
    ["solar", "electricity", "water", "gas"],
    index=0
)

if st.button("Get Forecast"):
    try:
        res = requests.get(
            f"{API_BASE}/forecast/",
            params={
                "building_id": building_for_forecast,
                "meter_type": meter_type_for_forecast
            }
        )
        if res.status_code == 200:
            forecast_data = res.json()
            st.json(forecast_data)

            # Visualization (if numeric)
            if "forecast" in forecast_data:
                plt.figure(figsize=(6, 3))
                plt.plot(forecast_data["forecast"], marker="o")
                plt.title("Forecasted Values")
                st.pyplot(plt)
        else:
            st.error(f"⚠️ Failed: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"🚨 Error connecting to API: {e}")


