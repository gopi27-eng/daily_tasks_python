from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from cleaned_pdf import extract_cleaned_pdf
from logging_utils.log import setup_logger

logger = setup_logger("rag_ingestion.log")

def build_vector_database(pdf_path: str):
    logger.info("--- Booting Vector Ingestion Pipeline ---")
    
    # 1. Run your custom extraction script (Returns a list of strings)
    raw_pages = extract_cleaned_pdf(pdf_path)
    
    if not raw_pages:
        logger.error("No text extracted. Aborting database build.")
        return
        
    # 2. Bridge to LangChain: Convert strings to Document objects
    documents = []
    for page_num, text in enumerate(raw_pages):
        # We attach the page number as metadata so the LLM can cite its sources later!
        doc = Document(page_content=text, metadata={"page": page_num + 1})
        documents.append(doc)
        
    # 3. Clean and Chunk the Text
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    logger.info(f"PDF split into {len(chunks)} overlapping chunks.")
    
    # 4. Initialize Embeddings
    logger.info("Initializing HuggingFace Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 5. Save to a Local Database Folder
    logger.info("Saving vectors to disk at ./chroma_db...")
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    logger.success("✅ Database built successfully!")

if __name__ == "__main__":
    # Path to your specific PDF
    pdf_path = "/mnt/c/Users/Gopi/Desktop/python_devops/Data_Scientist_Role.pdf"
    build_vector_database(pdf_path)