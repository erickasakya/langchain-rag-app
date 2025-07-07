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