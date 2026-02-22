import streamlit as st

def init_page():
    st.set_page_config(page_title="real-estate-listings", layout="wide")

    st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                }
                footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True
    )
    
    with st.sidebar:        
        with st.expander("Metadata", expanded=False):        
            placeholders = {
                "load_ts": st.empty(),
                "coverage": st.empty()
            }
                    
    return placeholders