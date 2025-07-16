import streamlit as st
import requests

st.set_page_config(page_title="LexiBot - Malaysian Law Chatbot")

st.title("⚖️ LexiBot")
st.subheader("Ask legal questions based on Malaysian law")

query = st.text_area("📝 Your legal question", height=150)

top_k = st.slider("📚 Number of context chunks to retrieve", min_value=1, max_value=10, value=3)

if st.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",  # Update if FastAPI is hosted elsewhere
                    json={"query": query, "top_k": top_k}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("🧠 Answer")
                    st.markdown(data["answer"])

                    with st.expander("📚 Retrieved Context Chunks"):
                        for i, chunk in enumerate(data["context"], 1):
                            st.markdown(f"**Chunk {i}**\n\n{chunk}")
                else:
                    st.error(f"❌ Error from backend: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Failed to connect to backend: {e}")
