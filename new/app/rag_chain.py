from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

# Your Hugging Face API key should be set as an environment variable
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# 1. In-memory knowledge base
defect_docs = [
    Document(page_content="Weld cracks are caused by residual stress or improper cooling."),
    Document(page_content="Paint scratches occur due to rough handling or poor surface preparation."),
    Document(page_content="Surface pitting is caused by corrosion or poor material quality.")
]

# 2. Embeddings + Vector Store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(defect_docs, embeddings)
retriever = vectorstore.as_retriever()

# 3. RAG Chain
rag_chain = RetrievalQA.from_chain_type(
    llm=HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.2}),
    retriever=retriever
)

# 4. Function to call in route
def query_rag(defect_query):
    return rag_chain.run(f"What causes {defect_query} and how to repair it?")
