import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import google.generativeai as gemini

# Function to configure Gemini
def configure_gemini(api_key):
    gemini.configure(api_key=api_key)

# Function to initialize Gemini model
def initialize_gemini_model():
    return gemini.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  system_instruction="""You are AI Assistant to resolve data science
                                  Queries of the user.""")

# Function to add a new chat button
def add_new_chat_button():
    st.sidebar.button('🔄 New Chat', on_click=start_new_chat)

# Function to handle new chat button click
def start_new_chat():
    # Clear previous messages and display initial greeting
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to Gemini AI Hub! How may I assist you 📝"}
    ]
    

# Function to add history button
def add_history_button():
    st.sidebar.button('📜 History', on_click=show_history)

# Function to display search history
def show_history():
    st.sidebar.title("Search History")
    for idx, query in enumerate(st.session_state.search_history[::-1], start=1):
        st.sidebar.write(f"{idx}. {query}")

# Function to add export button
def add_export_button():
    st.sidebar.button('📤 Export', on_click=export_data)

# Function to handle export button click
def export_data():
    # Generate a PDF report with the information
    generate_pdf_report()

# Function to generate PDF report
def generate_pdf_report():
    filename = "gemini_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    y = 750
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        c.drawString(50, y, f"{role}: {content}")
        y -= 20
    c.save()
    st.sidebar.write(f"Report exported as {filename}")

# Function to add settings button
def add_settings_button():
    st.sidebar.button('⚙️ Settings', on_click=redirect_to_settings)

# Function to handle settings button click
def redirect_to_settings():
    # Define the behavior when settings button is clicked
    pass

# Function to add email button
def add_email_button():
    st.sidebar.button('📧 Email', on_click=show_email_input)

# Function to display email input box
def show_email_input():
    email = st.sidebar.text_input("Enter your email:")
    if st.sidebar.button("Save"):
        save_email(email)

# Function to save the email
def save_email(email):
    st.session_state.email = email
    st.sidebar.write("Email saved successfully!")

# Main function
def main():
    st.title('🤖Data Alchemy: Transformative AI Tutorship')
    
    f = open(r"D:\internship\Data science\TASKS\gemini\keys\api_key.txt")
    api_key = f.read()
    
    configure_gemini(api_key)
    model = initialize_gemini_model()
    
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to Gemini AI Hub! How may I assist you 📝"}
        ]

    
    if "search_history" not in st.session_state.keys():
        st.session_state.search_history = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    user_input = st.chat_input()
    
    if user_input is not None:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.search_history.append(user_input)
        with st.chat_message("user"):
            st.write(user_input)
    
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = model.generate_content(user_input)
                st.write(ai_response.text)
        new_ai_message = {"role": "assistant", "content": ai_response.text}
        st.session_state.messages.append(new_ai_message)

    add_new_chat_button()
    add_settings_button()
    add_export_button()
    add_history_button()
    add_email_button()

if __name__ == "__main__":
    main()
