import streamlit as st
from dotenv import dotenv_values
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from datetime import datetime
import chromadb
from chromadb.utils import embedding_functions

config = dotenv_values(".env")

azure_openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_base=config["AZURE_EMBEDDING_BASE"],
    deployment_id=config["AZURE_EMBEDDING_MODEL"],
    api_type="azure",
    api_version="2023-05-15",
    api_key=config["AZURE_EMBEDDING_API_KEY"],
)

if not config.get("GROQ_API_KEY"):
    st.error("GROQ_API_KEY is not set in the environment variables.")

groq_api_key = config.get("GROQ_API_KEY")

st.title("LangChain RAG with Groq AI")


client = chromadb.HttpClient(host="localhost", port=8088)

if not (ret := client.heartbeat()):
    st.error("ChromaDB server is not running. Please start the server and try again.")
    st.stop()
else:
    st.success(
        f"The system is up and running. {datetime.fromtimestamp(int(ret / 1e9))}"
    )


system_message = SystemMessage(
    content="""You are a helpful assistant that is not too verbose. 
Only answer the question based on the context provided. If you don't know the answer, say 'I don't know'.
If the question is not related to the context, say 'I don't know'.""",
)


collection = client.get_or_create_collection(
    name="demo_rag_collection", embedding_function=azure_openai_ef
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


def get_relevant_docs(msg: str) -> list[str]:
    resp = collection.query(
        query_texts=[msg],
        n_results=5,
    )

    docs = [i[0] for i in resp["documents"]]
    start_info = f""" {system_message}
Use the following context to answer the question:
{"".join(docs)}"""

    return [SystemMessage(content=start_info)] + st.session_state.messages


def generate_response(msg: str):

    messages = get_relevant_docs(msg)
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
    response = generate_response(msg)

    st.rerun()


st.divider()
