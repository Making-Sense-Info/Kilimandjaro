import streamlit as st
import kilimandjaro.db as db
from kilimandjaro.models import CollectionInfo

@st.dialog("Peek")
def peekaboo(info: CollectionInfo):
    st.markdown("First n terms of " + info["name"])
    st.write(info["peek"])

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
    st.markdown(f"Matching terms for: {text}")
    results = db.query("ccam", text)
    for result in zip(results["ids"][0], results["documents"][0]):
        st.markdown(f"_{result[0]}_ - {result[1]}")
