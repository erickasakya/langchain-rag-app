import streamlit as st
from dotenv import dotenv_values
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.documents import Document
from datetime import datetime
import chromadb

config = dotenv_values(".env")
if not config.get("GROQ_API_KEY"):
    st.error("GROQ_API_KEY is not set in the environment variables.")

groq_api_key = config.get("GROQ_API_KEY")


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(name="demo_rag_collection")

st.title("LangChain RAG with Groq AI")

system_message = SystemMessage(
    content="You are a helpful assistant that is not too verbose. "
)

if "latest_msgs_sent" not in st.session_state:
    st.session_state.latest_msgs_sent = []

if "file_path" not in st.session_state:
    st.session_state.file_path = None

if "llm_chain" not in st.session_state:
    llm_chain = ChatGroq(
        model=config["GROQ_MODEL"],
        api_key=groq_api_key,
        temperature=0.7,
        # max_tokens=40,
    )
    st.session_state.llm_chain = llm_chain
else:
    llm_chain = st.session_state.llm_chain


if "messages" not in st.session_state:
    st.session_state.messages = []


def get_relevant_docs(message: HumanMessage) -> list[str]:
    # Query database for relevant documents based on the message content.
    pass
    # return a list of relevant documents
    return ["This is a relevant document."]


def generate_response():
    start_time = datetime.now()
    start_info = f""" Current time: {start_time} 
{system_message}"""
    messages = [SystemMessage(content=start_info)] + st.session_state.messages
    response = llm_chain.invoke(messages)

    st.session_state.messages.append(response)
    st.session_state.latest_msgs_sent = messages

    return response


for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("ai"):
            st.write(message.content)
    else:
        with st.chat_message("system"):
            st.write(message.content)

if msg := st.chat_input("Ask a question"):
    st.session_state.messages.append(HumanMessage(content=msg))
    response = generate_response()

    st.rerun()


st.divider()
st.write(st.session_state.file_path)
st.write(st.session_state.latest_msgs_sent)
