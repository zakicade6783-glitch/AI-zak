import streamlit as st
from google import genai
from pypdf import PdfReader
import os

# 1. Habaynta Website-ka
st.set_page_config(page_title="Zaki AI Assistant", page_icon="🌐")
st.title("🌐 Zakarie AI (PDF Trained)")

# 2. API Key-gaaga
GOOGLE_API_KEY = "AIzaSyDyACY4Q1DHXN2Vjb1j8318KIOhXxIi2zc"
client = genai.Client(api_key=GOOGLE_API_KEY)

# 3. Shaqada akhrinta PDF-ka
def load_pdf_data(file_path):
    if not os.path.exists(file_path):
        return "Faylka data.pdf lama helin GitHub-kaaga."
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text if text else "PDF-ku waa madhan yahay."
    except Exception as e:
        return f"Cilad PDF: {e}"

# Soo saar xogta PDF-ka
training_context = load_pdf_data("data.pdf")

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("I weydii wax ku saabsan xogta PDF-ka..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Halkan waxaa laga saxay Indentation-kii (bannaanadii)
            full_prompt = f"Isticmaal xogtan soo socota si aad ugu jawaabto su'aasha: \n\n{training_context}\n\nSu'aasha: {prompt}"
            
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=full_prompt
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Cilad ayaa dhacday: {e}")
