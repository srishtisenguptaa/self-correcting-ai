import os

# 🔐 Replace with your NEW HuggingFace token (revoke old one!)
token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# -------------------------------
# Imports
# -------------------------------
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# -------------------------------
# 1️⃣ Load Document
# -------------------------------
loader = TextLoader("docs.txt")   # Make sure docs.txt exists
documents = loader.load()

# -------------------------------
# 2️⃣ Split into chunks
# -------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

# -------------------------------
# 3️⃣ Create Embeddings + FAISS
# -------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# -------------------------------
# 4️⃣ Initialize HuggingFace LLM
# -------------------------------
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="conversational",   # ✅ FIXED
    temperature=0.2,
    max_new_tokens=512
)

# -------------------------------
# 5️⃣ Prompt Template
# -------------------------------
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.

Context:
{context}

Question: {input}
""")

# -------------------------------
# 6️⃣ LCEL RAG Chain
# -------------------------------
rag_chain = (
    {
        "context": retriever,
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# -------------------------------
# 7️⃣ Ask Question
# -------------------------------
query = "What are the key takeaways from the document?"

response = rag_chain.invoke(query)

print("\nAnswer:\n")
print(response)
