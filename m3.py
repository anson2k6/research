import streamlit as st

st.title("Limit of Detection Calculator")

sigma = st.number_input("Standard deviation (σ)", 0.0)
slope = st.number_input("Slope (k)", 0.0)

if slope > 0:
    lod = (3 * sigma) / slope
    st.success(f"LOD = {lod:.3e} M")
