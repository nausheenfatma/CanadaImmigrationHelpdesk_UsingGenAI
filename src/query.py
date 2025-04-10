
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore

from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama2", request_timeout=100.0)

# Restore settings
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

INDEX_PATH = "../index_directory"

# load index from disk
vector_store = FaissVectorStore.from_persist_dir(INDEX_PATH)
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir=INDEX_PATH)
index = load_index_from_storage(storage_context=storage_context)
retriever = index.as_retriever()

# Query function
def query_rag_system(question):
    retrieved_docs = retriever.retrieve(question)
    context = "\n".join([doc.text for doc in retrieved_docs])    
    prompt = f"Context:\n{context}\n\n Question: {question}\n\n\n\nAnswer:"
    response = llm.complete(prompt)
    return response

def main():
    ### Example
    question = "Can I apply for the Rural and Northern Immigration Pilot now?"
    answer = query_rag_system(question=question)
    print (answer)
    
    
main()