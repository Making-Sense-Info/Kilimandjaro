import streamlit as st
import kilimandjaro.db as db

st.header("Kilimandjaro :mountain:")
st.subheader("Querying concepts")

colls = db.list_collections()

selected = st.selectbox(
    "Choose a terminology",
    colls.keys(),
    index=None
)

if selected:
    st.text(f"You selected {colls[selected]["name"]} which holds {colls[selected]["count"]} terms.")

text = st.text_input("Your text")
run = st.button("Run")

if run:
    st.text(f"Matching terms for: {text}")
    results = db.query("ccam", text)
    for result in zip(results["ids"][0], results["documents"][0]):
        st.markdown(f"_{result[0]}_ - {result[1]}")
