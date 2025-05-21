import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
bioavailability = 0.98  # 98%

# Title
st.title("Caffeine Plasma Concentration Calculator")

# Inputs
name = st.text_input("Name")
body_mass = st.number_input("Body mass (kg)", min_value=1.0, max_value=200.0, value=70.0)
gender = st.selectbox("Gender", options=["m", "f", "d"])
smoker = st.selectbox("Smoker", options=["y", "n"])
pregnant = st.selectbox("Pregnant", options=["y", "n"])
oral_contraceptives = st.selectbox("Oral contraceptives", options=["y", "n"])
baby = st.selectbox("Baby", options=["y", "n"])

# Set Vd based on gender
Vd = 0.7 if gender == "m" else 0.6

doses = []
for i in range(1, 24):
    dose_time = st.number_input(f"Caffeine consume {i} time (h)", min_value=0.0, max_value=24.0, step=0.25, key=f"time_{i}")
    dose_mg = st.number_input(f"Caffeine consume {i} mg", min_value=0.0, max_value=1000.0, key=f"mg_{i}")
    doses.append((dose_time, dose_mg))

# Adjust half-life based on individual parameters
half_life = 5.0
if baby == "y":
    half_life = 80.0
if oral_contraceptives == "y":
    half_life = 8.0
if pregnant == "y":
    half_life += 15.0
if smoker == "y":
    half_life -= 2.0

# Function to calculate plasma concentration
def caffeine_concentration(doses, body_mass, half_life, Vd):
    k_elim = np.log(2) / half_life
    time = np.linspace(0, 24, 240)
    conc = np.zeros_like(time)

    for dose_time, dose_mg in doses:
        if dose_time is not None and dose_mg is not None:
            dose_time = float(dose_time)
            dose_mg = float(dose_mg)
            dose_conc = (dose_mg * bioavailability) / (Vd * body_mass)
            conc += dose_conc * np.exp(-k_elim * np.maximum(time - dose_time, 0))

    return time, conc

# Calculate and plot if button is pressed
if st.button("Calculate Caffeine Concentration"):
    time, conc = caffeine_concentration(doses, body_mass, half_life, Vd)

    fig, ax = plt.subplots()
    ax.plot(time, conc, label=f"{name}'s Cpl")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Plasma Concentration (mg/L")
    ax.set_title("Caffeine Plasma Concentration Over Time")
    ax.legend()
    st.pyplot(fig)
