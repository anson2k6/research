# spectral_simulator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Fluorescence Spectral Simulator")

# ---------------------------
# Store number of samples
# ---------------------------
if "num_samples" not in st.session_state:
    st.session_state.num_samples = 1

# ---------------------------
# Button to add new slider
# ---------------------------
if st.button("Add Sample"):
    st.session_state.num_samples += 1

# ---------------------------
# Ion Selection
# ---------------------------
ion = st.selectbox("Select Ion", ["Pb2+", "H2PO4-"])

# ---------------------------
# Wavelength Range
# ---------------------------
wavelength = np.linspace(400, 600, 200)

# ---------------------------
# Spectrum Generator Function
# ---------------------------
def generate_spectrum(ion, conc, wavelength):

    base_intensity = np.exp(-0.01*(wavelength-480)**2)*30000

    if ion == "Pb2+":   # Quenching
        k_lambda = 0.05 * np.exp(-0.01*(wavelength-480)**2)
        intensity = base_intensity * np.exp(-k_lambda * conc)

    else:               # Enhancement
        enhance_lambda = 0.05 * np.exp(-0.01*(wavelength-480)**2)
        intensity = base_intensity * (1 + enhance_lambda * conc)

    return intensity

# ---------------------------
# Create Plot
# ---------------------------
fig, ax = plt.subplots()

# ---------------------------
# Dynamic Sliders + Graphs
# ---------------------------
for i in range(st.session_state.num_samples):

    conc = st.slider(
        f"Concentration for Sample {i+1} (µM)",
        0, 10, 1,
        key=f"conc_{i}"
    )

    intensity = generate_spectrum(ion, conc, wavelength)

    ax.plot(wavelength, intensity, label=f"Sample {i+1}")

# ---------------------------
# Graph Settings
# ---------------------------
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Fluorescence Intensity")
ax.set_ylim(0, 40000)     # Fix autoscaling issue
ax.legend()

# ---------------------------
# Display Plot
# ---------------------------
st.pyplot(fig)
