import streamlit as st
from google import genai

# 1. Habaynta Bilicda Website-ka (UI Setup)
st.set_page_config(page_title="Zaki AI Assistant", page_icon="🌐", layout="centered")

# Magaca iyo Header-ka
st.title("🌐 Zakarie AI Web Assistant")
st.markdown("---")

# 2. Xiriirka Google AI (API Connection)
# Hubi in API Key-gani uu yahay kii aad hore u isticmaali jirtay
GOOGLE_API_KEY = "AIzaSyDyACY4Q1DHXN2Vjb1j8318KIOhXxIi2zc"
client = genai.Client(api_key=GOOGLE_API_KEY)

# 3. Sidebar (Features-ka AI-ga)
with st.sidebar:
    st.header("Settings")
    ai_mode = st.selectbox("Dooro Shaqada AI-ga:", 
                           ["Kaaliye Guud", "Turjubaan Soomaali", "Code Helper"])
    st.markdown("---")
    if st.button("Tirtir Sheekada"):
        st.session_state.messages = []
    st.info("App-kan waxaa iska leh Zakarie.")

# 4. Xusuusta Sheekada (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Soo bandhig sheekada hore ee shaashadda
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Meesha Su'aasha laga qoro (Chat Input)
if prompt := st.chat_input("Maxaan ku caawiyaa?"):
    # Ku dar su'aasha user-ka xusuusta
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jawaabta AI-ga
    with st.chat_message("assistant"):
        with st.spinner("AI-ga ayaa jawaab diyaarinaya..."):
            try:
             # Halkii aad prompt kaliya u diri lahayd, ku dar xogtaada
xogta_zakarie = "Zakarie waa aqoonyahan barta computer-ka. Website-kan isagaa leh..."
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=f"Xogtaada: {xogta_zakarie}. Su'aasha: {prompt}"
)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:

                st.error(f"Cilad ayaa dhacday: {e}")

