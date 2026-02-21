import streamlit as st

def init_page():
    st.set_page_config(page_title="real-estate-listings", layout="wide")
    
    with st.sidebar:        
        with st.expander("Metadata", expanded=False):        
            placeholders = {
                "load_ts": st.empty(),
                "coverage": st.empty()
            }
                    
    return placeholders