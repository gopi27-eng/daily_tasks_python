import streamlit as st
from engine import get_rag_chain

# --- 1. CONFIGURE STREAMLIT PAGE ---
st.set_page_config(page_title="Data Scientist Guide AI", page_icon="🧠", layout="centered")
st.title("🧠 Data Scientist Role - PDF Chatbot")
st.write("Powered by Llama 3, LangChain, and ChromaDB")

# --- 2. LOAD AI ENGINE (WITH CACHING) ---
@st.cache_resource
def load_engine():
    return get_rag_chain()

with st.spinner("Booting up AI Engine..."):
    rag_chain = load_engine()

# --- 3. INITIALIZE CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming greeting
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I have read your PDF about the Data Scientist role. What would you like to know?"
    })

# --- 4. DRAW PREVIOUS MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. HANDLE NEW CHAT INPUT ---
if user_input := st.chat_input("Ask a question about the PDF..."):
    
    # Display user message on screen
    with st.chat_message("user"):
        st.markdown(user_input)
    # Save user message to memory
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching PDF and thinking..."):
            try:
                # Pass the question into your engine.py logic
                response = rag_chain.invoke(user_input)
                st.markdown(response)
            except Exception as e:
                st.error("Error connecting to Ollama. Make sure you have run `ollama run llama3` in a separate terminal tab.")
                response = "Error connecting to backend."
                
    # Save AI response to memory
    st.session_state.messages.append({"role": "assistant", "content": response})