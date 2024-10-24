import streamlit as st

@st.cache_resource
def get_shared_counter():
    # Shared counter initialized to 0
    return {"value": 0}

# Function to increment the shared counter
def increment_shared_counter(shared_counter):
    shared_counter["value"] += 1

# Retrieve the shared counter
shared_counter = get_shared_counter()

text = st.empty()

# Button to increment the counter
if st.button("Increase by 1"):
    increment_shared_counter(shared_counter)
    st.rerun()

# Display the counter
@st.fragment(run_every=1)
def writeOutput():
    text.write(f"Current number: {shared_counter['value']}")
writeOutput()