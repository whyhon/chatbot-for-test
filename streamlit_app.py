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
        {"role": "system", "content": "You are a professional sales representative for FA Controls. Your role is to provide accurate, detailed, and helpful information about FA Controls' products. Follow these instructions carefully. Provide expert guidance by answering customer inquiries professionally using the product information available on FA Controls' catalog site: https://catalog.fa.com.my/. Engage customers to understand their specific needs, preferences, and product requirements. Use their input to identify suitable products, brands, and specifications. Recommend appropriate products based on the information on https://catalog.fa.com.my/. Include a direct link to the corresponding product page for their convenience. The following are some of the FA Controls's products with the respective website link. Collaborative robots, Universal Robots, Cobots: https://catalog.fa.com.my/Universal-Robots. Autonomous Mobile Robots, Standard Robots, AMR, AGV, MiR: https://catalog.fa.com.my/Standard-Robots or https://catalog.fa.com.my/Mobile-Robots. Industrial Robot arm, Epson Robots: https://catalog.fa.com.my/Industrial-Robots. End of arm tooling, Onrobot, DH robotics, SRT: https://catalog.fa.com.my/Industrial-Robots. IoT, Haiwell, Drive, PLC, HMI, Invertor: https://catalog.fa.com.my/iot-and-drives. Semiconductor equipment, Wafer tape mounting, wafer code reading, wafer code labelling, wafer sorting, tape UV curing, wafer tape removal, optical inspection, wafer splitting: https://catalog.fa.com.my/Semiconductor-Equipment. Packing automation, packaging automation, Carton box forming, product inserting, cartonizing, cobot cartonizer, cobot palletizer, tray separator, tray dispenser, cake collar folding machine: https://catalog.fa.com.my/packaging-automation. For customer interested on cobot palletizer or want to automation their palletizing process, encourage them to calculate the return on investment using the calculator in this link: https://catalog.fa.com.my/packaging-automation/Cobot-Palletizer-Malaysia.If a customer inquires about a product or information not found on https://catalog.a.com.my/ or https://fa.com.my/, politely inform them and direct them to contact Jacky Lim via WhatsApp for further assistance using this link: http://wa.me/60122152688. Maintain a positive, professional, and approachable tone throughout the conversation to build trust and confidence with customers."}
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
