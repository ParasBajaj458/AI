import streamlit as st
from openai import OpenAI

# Groq API key
API_KEY = "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"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL ="openai/gpt-oss-20b"


def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=512
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


st.set_page_config(
    page_title="AI Teaching Assistant",
    layout="centered"
)

st.title("🤖 AI Teaching Assistant")
st.write("Ask me anything about various subjects.")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Generating response..."):
            answer = generate_response(question)

        st.session_state.history.insert(
            0,
            {"question": question, "answer": answer}
        )
        st.rerun()
    else:
        st.warning("Please enter a question.")

if st.session_state.history:
    st.markdown("### Conversation History")

    for i, chat in enumerate(st.session_state.history, 1):
        st.markdown(f"**Q{i}: {chat['question']}**")
        st.write(chat["answer"])
        st.divider()

if st.button("🧹 Clear Conversation"):
    st.session_state.history = []
    st.rerun()