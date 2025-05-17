# query_retrieval.py
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
load_dotenv()

def retrieve_context(query, index_path, k=3):
    """Retrieve top-k relevant documents for a query."""

    # Updated embedding configuration for Azure OpenAI
    embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_type=os.getenv("AZURE_API_TYPE"),
    openai_api_version=os.getenv("AZURE_API_VERSION")
)

    # Load FAISS vector store
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # Retrieve top-k documents
    results = vectorstore.similarity_search(query, k=k)

    # Return only the text content
    return [result.page_content for result in results]


if __name__ == "__main__":
    query = input("Enter your query: ").strip()
    index_path = "embeddings/dora_index1"
    context = retrieve_context(query, index_path)
    print("\nRetrieved Context:\n")
    print("\n".join(context))
