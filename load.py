# Load, split and store the text data into the vector store
from dotenv import dotenv_values
from chunking_evaluation.chunking import ClusterSemanticChunker
from chromadb.utils import embedding_functions
import chromadb
import streamlit as st

config = dotenv_values(".env")
st.title("LangChain RAG with Groq AI")

st.subheader("Upload your text file to create a RAG pipeline")

if not config.get("AZURE_EMBEDDING_MODEL"):
    st.error(
        "AZURE_EMBEDDING_MODEL environment variable is not set. Please set it to your Azure OpenAI embedding model."
    )
    st.stop()

if not config.get("AZURE_EMBEDDING_BASE"):
    st.error(
        "AZURE_EMBEDDING_BASE environment variable is not set. Please set it to your Azure OpenAI embedding base url."
    )
    st.stop()

if not config.get("AZURE_EMBEDDING_API_KEY"):
    st.error(
        "AZURE_EMBEDDING_API_KEY environment variable is not set. Please set it to your Azure OpenAI embedding API key."
    )
    st.stop()


azure_openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_base=config.get("AZURE_EMBEDDING_BASE"),
    deployment_id=config.get("AZURE_EMBEDDING_MODEL"),
    api_type="azure",
    api_version="2023-05-15",
    api_key=config.get("AZURE_EMBEDDING_API_KEY"),
)

uploaded_file = st.file_uploader(
    "Upload a text file to create a RAG pipeline",
    type=["txt"],
)

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    st.write("filename:", uploaded_file.name)

    with st.spinner("Loading data...", show_time=True):
        client = chromadb.HttpClient(
            host=config["CHROMADB_HOST"], port=config["CHROMADB_PORT"]
        )
        chunker = ClusterSemanticChunker(
            embedding_function=azure_openai_ef, max_chunk_size=200
        )
        semantic_chunks = chunker.split_text(data)

        collection = client.get_or_create_collection(
            name="demo_rag_collection", embedding_function=azure_openai_ef
        )
        collection.add(
            documents=semantic_chunks, ids=[str(i) for i in range(len(semantic_chunks))]
        )

    st.success("Number of chunks created: {}".format(len(semantic_chunks)))
    st.success("File uploaded and processed successfully!")
