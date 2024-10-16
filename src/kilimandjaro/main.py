"""This module holds the code for the web UI"""

import streamlit as st
import kilimandjaro.db as db
from kilimandjaro.models import CollectionInfo

# --- Components

@st.dialog("Peek")
def peekaboo(info: CollectionInfo):
    st.markdown("First n terms of " + info["name"])
    st.write(info["peek"])

# --- Main

st.header("Kilimandjaro :mountain:")
st.subheader("Querying concepts")

colls = db.list_collections()

selected = st.selectbox("Choose a terminology", colls.keys(), index=None)

if selected:
    st.markdown(
        f"You selected {colls[selected]["name"]} which holds {colls[selected]["count"]} terms."
    )
    peeked = st.button("Peek")
    if peeked:
        peekaboo(colls[selected])


text = st.text_input("Your text")
run = st.button("Run")

if text or run:
    if selected:
        st.markdown(f"Matching terms for: {text}")
        results = db.query(selected, text)
        for result in zip(results["ids"][0], results["documents"][0]):
            st.markdown(f"_{result[0]}_ - {result[1]}")
