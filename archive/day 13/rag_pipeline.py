from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from logging_utils.log import setup_logger

logger = setup_logger("rag_pipeline.log")


def build_rag_pipeline():
    
    logger.info("---Booting Rag Vector Engine---")
    
    raw_data = (
        "Section 1: General Cargo. All standard freight must be processed at Terminal A. "
        "Section 2: Fragile Goods. Fragile cargo has a maximum weight limit of 4500 KG per pallet. "
        "It must be routed through Terminal B and inspected. "
        "Section 3: Perishables. Temperature-controlled goods require a -10C environment. "
        "Section 4: Hazardous Materials. Hazmat requires station manager approval."
    )
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 10)
    chunks = splitter.create_documents([raw_data])
    logger.info(f"successfully converted document into chunks {len(chunks)}!")
    
    # Inetializing Embeding Model
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    
    logger.info("Building local Vector Database...")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    
    # 5. Execute Similarity Search
    query = "What is the weight limit for fragile goods?"
    results = vector_db.similarity_search(query, k=2)
    
    logger.success("Search Results:")
    for i, doc in enumerate(results):
        print(f"Result {i+1}: {doc.page_content}")

if __name__ == "__main__":
    build_rag_pipeline()