import streamlit as st
import kilimandjaro.db as db

st.header("Kilimandjaro :mountain:")
st.subheader("Querying concepts")

st.text("Available collections")
colls = db.list_collections()
for k, v in colls.items():
    st.markdown(f" - {k}")

text = st.text_input("A text")
run = st.button("Run")

if run:
    st.text(f"Thing is: {text}")
