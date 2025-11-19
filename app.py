import streamlit as st
import google.generativeai as genai

st.title("🛠 Կարգավորումների Ստուգում")

# Քայլ 1. Ստուգում ենք՝ արդյոք Secrets-ը կարդում է
st.write("---")
st.subheader("1. Բանալու Ստուգում")

if "GOOGLE_API_KEY" in st.secrets:
    st.success("✅ Ծրագիրը ՏԵՍՆՈՒՄ է բանալին Secrets-ի մեջ:")
    key = st.secrets["GOOGLE_API_KEY"]
    # Ցույց ենք տալիս միայն առաջին 5 նիշը՝ համոզվելու համար, որ ճիշտ բանալին է
    st.write(f"Ձեր բանալու սկիզբը՝ `{key[:5]}...`")
    
    # Քայլ 2. Փորձում ենք միանալ Google AI-ին
    st.subheader("2. Google AI-ի Ստուգում")
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Բարև, ես աշխատում եմ։")
        st.success("✅ Google AI-ը պատասխանեց:")
        st.info(f"AI-ի պատասխանը: {response.text}")
        st.balloons()
    except Exception as e:
        st.error("❌ Բանալին կա, բայց AI-ը չի աշխատում:")
        st.error(f"Սխալի տեքստը: {e}")
        
else:
    st.error("❌ Ծրագիրը ՉԻ ՏԵՍՆՈՒՄ բանալին:")
    st.write("Խնդրում ենք նորից ստուգել Secrets բաժինը:")
    st.write("Այն ինչ տեսնում է ծրագիրը հիմա՝", st.secrets)
