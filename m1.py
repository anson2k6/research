# spectral_simulator.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Fluorescence Spectral Simulator")

ion = st.selectbox("Select Ion", ["Pb2+", "H2PO4-"])
conc = st.slider("Ion concentration (µM)", 0, 50, 10)

wavelength = np.linspace(400, 600, 200)

#This is just a formula simplified into python code: I0​(λ)=100*e^(−0.01(λ−480)^2)
base_intensity = np.exp(-0.01*(wavelength-480)**2)*100

if ion == "Pb2+":
    intensity = base_intensity * np.exp(-0.05*conc)  # quenching
else:
    intensity = base_intensity * (1 + 0.05*conc)      # enhancement

fig,ax = plt.subplots()

ax.plot(wavelength, intensity)
ax.set_xlabel("Wavelength (nm)")
ax.set_ylabel("Fluorescence Intensity")
ax.set_ylim(0,400)
st.pyplot(fig)
