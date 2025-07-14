import streamlit as st
import pandas as pd

# Load CSV files
@st.cache_data
def load_data():
    operator_df = pd.read_csv("NonIlluminatedPushbuttonOperator.csv", header=None)
    color_df = pd.read_csv("NonIlluminatedPushbuttonButtonColor.csv", header=None)
    circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None)

    # Convert to dictionaries
    operator_dict = {str(v).strip(): str(k).strip() for k, v in zip(operator_df.iloc[:, 1], operator_df.iloc[:, 0])}
    color_dict = {str(v).strip(): str(k).strip() for k, v in zip(color_df.iloc[:, 1], color_df.iloc[:, 0])}
    circuit_dict = {str(v).strip(): str(k).strip() for k, v in zip(circuit_df.iloc[:, 1], circuit_df.iloc[:, 0])}

    # Reverse lookup
    operator_code_to_label = {v: k for k, v in operator_dict.items()}
    color_code_to_label = {v: k for k, v in color_dict.items()}
    circuit_code_to_label = {v: k for k, v in circuit_dict.items()}

    return operator_code_to_label, color_code_to_label, circuit_code_to_label

operator_lookup, color_lookup, circuit_lookup = load_data()

# UI
st.title("10250T Catalog Number Decoder")
catalog_input = st.text_input("Enter a 10250T catalog number (e.g., 10250T112-1 or 10250T1121):")

if catalog_input:
    normalized = catalog_input.replace("-", "").strip().upper()

    if normalized.startswith("10250T") and len(normalized) > 7:
        code_part = normalized[6:]
        if len(code_part) >= 4:
            operator_code = code_part[:2]
            color_code = code_part[2]
            circuit_code = code_part[3:]

            operator_label = operator_lookup.get(operator_code, "Unknown Operator Code")
            color_label = color_lookup.get(color_code, "Unknown Color Code")
            circuit_label = circuit_lookup.get(circuit_code, "Unknown Circuit Code")

            st.markdown("### 🔍 Decoded Result")
            st.write(f"**Operator Type**: {operator_label}")
            st.write(f"**Button Color**: {color_label}")
            st.write(f"**Circuit Type**: {circuit_label}")
        else:
            st.error("Catalog number is too short to decode.")
    else:
        st.error("Catalog number must start with '10250T'.")
