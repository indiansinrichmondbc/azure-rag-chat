import os

def process_documents(uploaded_files):
    # Initialize local storage vector store
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = []

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        # Read the content of the file
        content = uploaded_file.read().decode("utf-8")
        
        # Add the content to the vector store
        st.session_state.vector_store.append(content)

    return "Local Storage Vector Store"
