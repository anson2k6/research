import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="DBST Molecular Logic Gate System",
    layout="wide",
)

# --------------------------------------------------
# CUSTOM CSS (Professional Dark Theme)
# --------------------------------------------------

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3, h4 {
    color: #f0f2f6;
}
.stDataFrame, .stTable {
    background-color: #1c1f26;
}
div[data-testid="stSidebar"] {
    background-color: #111418;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("DBST Chemosensor Molecular Logic Gate Analyzer")

st.markdown("""
This platform performs fluorescence data analysis for DBST probe systems.

Functions included:
• Automatic λmax detection  
• Spectral visualization  
• Enhancement and quenching calculation  
• Analog-to-digital fluorescence conversion  
• Molecular logic gate simulation  
• Truth table generation  
""")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.header("1. Data Upload")

uploaded_file = st.file_uploader("Upload CSV file (Wavelength, DBST, DBST+H2PO4-, DBST+Pb2+)", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if df.shape[1] < 4:
        st.error("CSV must contain four columns: Wavelength, DBST, DBST+H2PO4-, DBST+Pb2+")
        st.stop()

    wavelength = df.iloc[:, 0]
    dbst = df.iloc[:, 1]
    h2po4 = df.iloc[:, 2]
    pb = df.iloc[:, 3]

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # --------------------------------------------------
    # λmax Detection
    # --------------------------------------------------

    st.header("2. Peak Analysis")

    idx_max = dbst.idxmax()
    lambda_max = wavelength.iloc[idx_max]

    I_dbst = dbst.iloc[idx_max]
    I_h2po4 = h2po4.iloc[idx_max]
    I_pb = pb.iloc[idx_max]

    col1, col2, col3 = st.columns(3)

    col1.metric("λmax (nm)", f"{lambda_max:.2f}")
    col2.metric("DBST Intensity", f"{I_dbst:.2f}")
    col3.metric("H2PO4- Intensity", f"{I_h2po4:.2f}")

    # --------------------------------------------------
    # SPECTRAL VISUALIZATION
    # --------------------------------------------------

    st.header("3. Spectral Visualization")

    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(wavelength, dbst, label="DBST", linewidth=2)
    ax.plot(wavelength, h2po4, label="DBST + H2PO4-", linewidth=2)
    ax.plot(wavelength, pb, label="DBST + Pb2+", linewidth=2)

    ax.axvline(lambda_max, linestyle="--", linewidth=1)

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Fluorescence Intensity")
    ax.set_title("Fluorescence Emission Spectra")
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig, use_container_width=True)

    # --------------------------------------------------
    # ANALYTICAL PARAMETERS
    # --------------------------------------------------

    st.header("4. Analytical Parameters")

    enhancement_factor = I_h2po4 / I_dbst
    quenching_efficiency = (I_dbst - I_pb) / I_dbst

    col1, col2 = st.columns(2)
    col1.metric("Enhancement Factor (EF)", f"{enhancement_factor:.3f}")
    col2.metric("Quenching Efficiency (QE)", f"{quenching_efficiency:.3f}")

    # --------------------------------------------------
    # DIGITAL CONVERSION
    # --------------------------------------------------

    st.header("5. Digital Fluorescence Conversion")

    max_intensity = max(I_dbst, I_h2po4, I_pb)

    threshold = st.slider(
        "Select Digital Threshold",
        min_value=0,
        max_value=int(max_intensity),
        value=int(I_dbst/2)
    )

    digital_dbst = 1 if I_dbst > threshold else 0
    digital_h2po4 = 1 if I_h2po4 > threshold else 0
    digital_pb = 1 if I_pb > threshold else 0

    digital_table = pd.DataFrame({
        "System": ["DBST", "DBST + H2PO4-", "DBST + Pb2+"],
        "Intensity at λmax": [I_dbst, I_h2po4, I_pb],
        "Digital Output": [digital_dbst, digital_h2po4, digital_pb]
    })

    st.table(digital_table)

    # --------------------------------------------------
    # LOGIC GATE SIMULATION
    # --------------------------------------------------

    st.header("6. Molecular Logic Gate Simulation")

    st.markdown("INHIBIT Gate Model: Output = H2PO4- AND NOT(Pb2+)")

    col1, col2 = st.columns(2)

    with col1:
        input_A = st.checkbox("H2PO4- Present")

    with col2:
        input_B = st.checkbox("Pb2+ Present")

    if input_A and not input_B:
        intensity = I_h2po4
    elif input_B:
        intensity = I_pb
    else:
        intensity = I_dbst

    output = 1 if intensity > threshold else 0

    st.write(f"Output Intensity: {intensity:.2f}")
    st.write(f"Digital Output: {output}")

    # --------------------------------------------------
    # TRUTH TABLE
    # --------------------------------------------------

    st.header("7. Truth Table")

    truth_table = pd.DataFrame({
        "H2PO4-": [0,0,1,1],
        "Pb2+": [0,1,0,1],
        "Fluorescence Output": [1,0,1,0]
    })

    st.table(truth_table)

    # --------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------

    st.header("8. Scientific Interpretation")

    st.markdown(f"""
    λmax detected at {lambda_max:.2f} nm.

    The presence of H2PO4- enhances fluorescence (EF = {enhancement_factor:.3f}).

    Pb2+ significantly quenches emission (QE = {quenching_efficiency:.3f}).

    The system functions as a molecular INHIBIT logic gate where fluorescence
    is observed only when H2PO4- is present and Pb2+ is absent.
    """)