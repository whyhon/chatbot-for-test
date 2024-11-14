import streamlit as st
from openai import OpenAI

# Streamlit app setup
st.title("FA Controls - Sales Inquiry GPT")

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state for model and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful sales representative for FA Controls. You provide detailed information about FA Controls' products and answer customer inquiries professionally."}
    ]

# Display chat history, excluding system messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to check if a prompt is about a specific product
def get_product_response(prompt):
    # Placeholder for product knowledge dictionary, now empty
    product_knowledge = {}
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
