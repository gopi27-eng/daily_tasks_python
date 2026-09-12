from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from logging_utils.log import setup_logger 

logger = setup_logger("llm_rag.log")


def build_genaration_chain(vectior_db):
    
    