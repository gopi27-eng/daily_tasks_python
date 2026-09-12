from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from logging_utils.log import setup_logger

logger = setup_logger("rag_engine.log")

def get_rag_chain():
    logger.info("--- Booting RAG Engine ---")
    
    # 1. Initialize the EXACT same embeddings used in ingest.py
    logger.info("Loading Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Connect to the saved Chroma database
    logger.info("Connecting to local Chroma DB...")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 3. Create Retriever (Fetch top 3 most relevant chunks)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    
    # 4. Initialize Local Llama 3 via Ollama
    logger.info("Loading Ollama Llama 3...")
    llm = Ollama(model="llama3")
    
    # 5. Define the Prompt Template (Tailored for your PDF)
    template = """You are a Data Science Career Expert. Answer the question based ONLY on the provided context from the PDF.
    If the answer is not in the context, say "I don't have information on that in the PDF."
    
    Context from PDF:
    {context}
    
    User Question: {question}
    Answer:"""
    prompt = PromptTemplate.from_template(template)
    
    # 6. Helper function to format retrieved chunks into plain text
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    # 7. Build the LCEL Chain
    logger.info("Fusing the LCEL Chain...")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    # Quick test to ensure the engine runs independently before plugging into Streamlit
    chain = get_rag_chain()
    print("Engine built successfully. Testing connection...")
    # Uncomment the line below to test it directly in the terminal:
    # print(chain.invoke("What does a Data Scientist do?"))