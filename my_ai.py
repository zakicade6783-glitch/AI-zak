import streamlit as st
from google import genai

# 1. Habaynta Bilicda Website-ka
st.set_page_config(page_title="Zaki AI Assistant", page_icon="🌐", layout="centered")

st.title("🌐 Zakarie AI Web Assistant")
st.markdown("---")

# 2. Xiriirka Google AI (API Key-gaaga cusub)
GOOGLE_API_KEY = "AIzaSyDyACY4Q1DHXN2Vjb1j8318KIOhXxIi2zc"
client = genai.Client(api_key=GOOGLE_API_KEY)

# 3. Sidebar
with st.sidebar:
    st.header("Settings")
    ai_mode = st.selectbox("Dooro Shaqada AI-ga:", 
                           ["Kaaliye Guud", "Turjubaan Soomaali", "Code Helper"])
    st.markdown("---")
    if st.button("Tirtir Sheekada"):
        st.session_state.messages = []
    st.info("App-kan waxaa iska leh Zakarie.")

# 4. Xusuusta Sheekada
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Xogta aad rabto in AI-gu barto (Training Data)
xogta_zakarie = """
Magaca ninka iska leh website-kan waa Zakarie. 
Zakarie waa aqoonyahan barta cilmiga computer-ka. 
Website-kan waxaa loogu talagalay inuu dadka caawiyo isagoo isticmaalaya Gemini AI.
"""

# 6. Meesha Su'aasha
if prompt := st.chat_input("Maxaan ku caawiyaa?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI-ga ayaa jawaab diyaarinaya..."):
            try:
                # Halkani waa halka tababarka laga siinayo AI-ga
                full_prompt = f"Xogta rasmiga ah: {xogta_zakarie}. \nSu'aasha isticmaalaha: {prompt}"
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=full_prompt
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Cilad ayaa dhacday: {e}")
