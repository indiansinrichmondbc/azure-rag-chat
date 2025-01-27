import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from document_processor import process_documents
from chat_chain import create_chat_chain
from chat_history import get_session_history

from langchain_community.vectorstores.chroma import Chroma
from azure_config import embeddings
import os

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    # Try to load existing vector store
    if os.path.exists("/app/chroma_db"):
        st.session_state.vector_store = Chroma(
            persist_directory="/app/chroma_db",
            embedding_function=embeddings
        )
    else:
        st.session_state.vector_store = None
if "memory_store" not in st.session_state:
    st.session_state.memory_store = {}
if "use_existing_docs" not in st.session_state:
    st.session_state.use_existing_docs = False

# Streamlit UI
st.title("📚 Modern RAG Chat with Azure OpenAI")

# Toggle for using existing documents
st.session_state.use_existing_docs = st.checkbox("Use existing documents", st.session_state.use_existing_docs)

if not st.session_state.use_existing_docs:
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload text documents",
        type=["txt"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            st.session_state.vector_store = process_documents(uploaded_files)
            st.success("Documents processed successfully!")
else:
    # Check if we have existing documents
    if os.path.exists("/app/chroma_db"):
        if st.session_state.vector_store is None:
            st.session_state.vector_store = Chroma(
                persist_directory="/app/chroma_db",
                embedding_function=embeddings
            )
        st.success("Using existing documents from the database")
    else:
        st.warning("No existing documents found in the database. Please upload new documents.")
        st.session_state.use_existing_docs = False
        st.rerun()

# Chat interface
if st.session_state.vector_store:
    # Initialize the chat chain
    conversational_rag_chain = create_chat_chain(st.session_state.vector_store)
    
    # Display chat history first
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Process user input
    if prompt := st.chat_input("Ask about your documents"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        get_session_history("default").add_message(HumanMessage(content=prompt))
        
        # Generate and process response
        try:
            with st.spinner("Thinking..."):
                response = conversational_rag_chain.invoke(
                    {"input": prompt},
                    config={"configurable": {"session_id": "default"}},
                )
                
                # Format answer in the required JSON structure
                if "answer" in response:
                    raw_answer = response["answer"]
                    if isinstance(raw_answer, str):
                        # If it's already a string, use it directly
                        formatted_answer = raw_answer
                    else:
                        # Convert any other type to string
                        formatted_answer = str(raw_answer)
                
                # Add assistant response to history
                st.session_state.chat_history.append({"role": "assistant", "content": formatted_answer})
                get_session_history("default").add_message(AIMessage(content=formatted_answer))
                
                # Rerun to immediately show new messages
                st.rerun()
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            get_session_history("default").add_message(AIMessage(content=error_msg))
            st.rerun()
    
    # Display memory store
    with st.sidebar:
        if st.session_state.memory_store:
            st.subheader("📝 Memory Store")
            for key, value in st.session_state.memory_store.items():
                st.text(f"{key}: {value}")
