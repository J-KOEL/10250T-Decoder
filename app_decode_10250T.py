import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    operator_df = pd.read_csv("NonIlluminatedPushbuttonOperator.csv", header=None)
    color_df = pd.read_csv("NonIlluminatedPushbuttonButtonColor.csv", header=None)
    circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None)
    alt_df = pd.read_csv("AlternateCatalogNumbers.csv")

    # Convert to dictionaries
    operator_dict = {str(v).strip(): str(k).strip() for k, v in zip(operator_df.iloc[:, 1], operator_df.iloc[:, 0])}
    color_dict = {str(v).strip(): str(k).strip() for k, v in zip(color_df.iloc[:, 1], color_df.iloc[:, 0])}
    circuit_dict = {str(v).strip(): str(k).strip() for k, v in zip(circuit_df.iloc[:, 1], circuit_df.iloc[:, 0])}

    operator_code_to_label = {v: k for k, v in operator_dict.items()}
    color_code_to_label = {v: k for k, v in color_dict.items()}
    circuit_code_to_label = {v: k for k, v in circuit_dict.items()}

    # Alternate catalog number mapping
    alt_map = {str(row['Alternate']).strip().upper(): str(row['Standard']).strip().upper()
               for _, row in alt_df.iterrows()}

    return operator_code_to_label, color_code_to_label, circuit_code_to_label, alt_map

operator_lookup, color_lookup, circuit_lookup, alt_map = load_data()

st.title("🔍 10250T Catalog Number Decoder")

catalog_input = st.text_input("Enter a 10250T catalog number (e.g., 10250T112-1 or 10250T30B):")

if catalog_input:
    original_input = catalog_input.replace("-", "").strip().upper()

    
    # Try to convert alternate number
    mapped = alt_map.get(original_input, original_input)
    if mapped != original_input:
        st.info(f"Alternate catalog number detected. Decoding as: `{mapped}`")

    # Normalize the mapped result (remove dash, uppercase)
    normalized = mapped.replace("-", "").strip().upper()


    if normalized.startswith("10250T") and len(normalized) > 7:
        code_part = normalized[6:]
        if len(code_part) >= 4:
            operator_code = code_part[:2]
            color_code = code_part[2]
            circuit_code = code_part[3:]

            operator_label = operator_lookup.get(operator_code, "Unknown Operator Code")
            color_label = color_lookup.get(color_code, "Unknown Color Code")
            circuit_label = circuit_lookup.get(circuit_code, "Unknown Circuit Code")

            operator_pn = f"10250T{operator_code}{color_code}"
            contact_block_pn = f"10250T{circuit_code}"

            st.markdown("### ✅ Decoded Result")
            st.write(f"**Operator Type**: {operator_label}")
            st.write(f"**Button Color**: {color_label}")
            st.write(f"**Circuit Type**: {circuit_label}")

            st.markdown("### 🧩 Component Part Numbers")
            st.write(f"**Operator P/N**: `{operator_pn}`")
            st.write(f"**Contact Block P/N**: `{contact_block_pn}`")
        else:
            st.error("Catalog number is too short to decode.")
    else:
        st.error("Catalog number must start with '10250T'.")
