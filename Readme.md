## Steps to Run this Application

1. Run `docker compose up -d `
2. Run all the cells in `rag_pipeline.ipynb`
3. Run strealit app `streamlit run main.py`
4. Start chatting


## Steps to develop RAG

1. read the data/text from the db or from a file
2. from chunking_evaluation.chunking import ClusterSemanticChunker/ the chuking method
3. intialize the embeddings using the azureOpenAIEmbeddings
4. Intialize the ClusterSemanticChunker
5. Split text received on step one
6. Create an embeddings function for chromadb



## Install a custom chunking library
```
pip install git+https://github.com/brandonstarxel/chunking_evaluation.git
```