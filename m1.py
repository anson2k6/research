# spectral_simulator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Fluorescence Spectral Simulator")

ion = st.selectbox("Select Ion", ["Pb2+", "H2PO4-"])
conc = st.slider("Ion concentration (µM)", 0, 50, 10)

# Wavelength range
wavelength = np.linspace(400, 600, 400)

# Base Gaussian parameters
peak_center = 480
peak_width = 20

if ion == "Pb2+":
    # Peak shifts to shorter wavelength (blue shift)
    shifted_center = peak_center - 0.3 * conc
    
    # Peak broadening
    width = peak_width + 0.2 * conc
    
    # Quenching effect
    intensity = np.exp(-((wavelength - shifted_center)**2) / (2 * width**2))
    intensity *= np.exp(-0.03 * conc) * 100

else:  # H2PO4-
    # Slight red shift
    shifted_center = peak_center + 0.2 * conc
    
    # Slight narrowing
    width = peak_width - 0.1 * conc if peak_width - 0.1 * conc > 5 else 5
    
    main_peak = np.exp(-((wavelength - shifted_center)**2) / (2 * width**2))
    
    # Add secondary shoulder peak
    shoulder = 0.3 * np.exp(-((wavelength - 520)**2) / (2 * 15**2))
    
    intensity = (main_peak + shoulder) * (1 + 0.03 * conc) * 100

# Plot
fig, ax = plt.subplots()
ax.plot(wavelength, intensity, color="blue")
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Fluorescence Intensity")
ax.set_title(f"Spectrum for {ion} at {conc} µM")

st.pyplot(fig)
