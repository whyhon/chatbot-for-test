import os
import fitz  # PyMuPDF library for reading PDFs
import streamlit as st
from openai import OpenAI

# Load and extract product data from all PDF files in a folder
def load_pdf_folder(folder_path):
    product_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            with fitz.open(os.path.join(folder_path, filename)) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf[page_num]
                    text = page.get_text()
                    # Basic parsing; adjust based on PDF structure
                    lines = text.splitlines()
                    product_name, product_description = "", ""
                    for line in lines:
                        if line.startswith("Product Name:"):
                            product_name = line.split(":")[1].strip()
                        elif line.startswith("Description:"):
                            product_description = line.split(":")[1].strip()
                    if product_name and product_description:
                        product_data[product_name] = product_description
    return product_data

# Path to the folder containing PDF files
pdf_folder_path = "/workspaces/chatbot-for-test/products"
product_knowledge = load_pdf_folder(pdf_folder_path)

# Streamlit app setup
st.title("FA Controls - Sales Inquiry GPT")

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for model and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to check if a prompt is about a specific product
def get_product_response(prompt):
    for product, description in product_knowledge.items():
        if product.lower() in prompt.lower():
            return description
    return None

# Handle user input
if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if prompt relates to a specific product
    product_response = get_product_response(prompt)
    if product_response:
        response = product_response
    else:
        # Use OpenAI API if no specific product match found
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

    # Display and save the response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
