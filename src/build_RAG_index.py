
#check latest https://docs.llamaindex.ai/en/stable/examples/vector_stores/FaissIndexDemo/

from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import faiss

INDEX_PATH = "../index_directory"

# 1. Load your documents
documents = SimpleDirectoryReader(input_dir="../data/docs/").load_data()


# 2. Initialize embeddings, used for encoding documents into embedding
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


# 3. Create FAISS index
dimension = 384  # Dimension for MiniLM embeddings
faiss_index = faiss.IndexFlatL2(dimension)

# 4. Construct the FaissVectorStore
faiss_vector_store = FaissVectorStore(faiss_index=faiss_index)


# 5. Create a StorageContext to use with LlamaIndex
storage_context = StorageContext.from_defaults(vector_store=faiss_vector_store)

# 6. Build index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)
retriever = index.as_retriever()


# 7. Save index to disk
index.storage_context.persist(INDEX_PATH)
