
import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

st.title("Spectral Line Identifier (Web Version)")

uploaded_file = st.file_uploader("Upload your spectrum (.xls format)", type="xls")
rms_threshold = st.number_input("RMS Threshold (K)", value=0.005)

if uploaded_file:
    try:
        sheet = pd.read_excel(uploaded_file, sheet_name="Sheet1", header=None)
        freq = sheet.iloc[:, 0]
        vel = sheet.iloc[:, 1]
        temp = sheet.iloc[:, 2]

        # Clean bad data
        clean_data = sheet[temp > -1000]
        freq = clean_data.iloc[:, 0].values
        temp = clean_data.iloc[:, 2].values

        # Plot
        fig, ax = plt.subplots()
        ax.step(freq, temp, where='mid')
        ax.set_xlabel("Frequency (MHz)")
        ax.set_ylabel("Temperature (K)")
        st.pyplot(fig)

        # Find peaks
        peaks, _ = find_peaks(temp, height=rms_threshold)
        st.markdown("### Identified Peaks")
        st.write(pd.DataFrame({
            "Frequency (MHz)": freq[peaks],
            "Temperature (K)": temp[peaks]
        }))

    except Exception as e:
        st.error(f"Error reading file: {e}")
