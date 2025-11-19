import streamlit as st
import google.generativeai as genai

st.title("🔍 Մոդելների Որոնում")
st.write("Եկեք տեսնենք, թե Google-ը որ մոդելներն է թույլ տալիս օգտագործել ձեր բանալիով:")

# 1. Ստուգում ենք բանալին
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Բանալին գտնված չէ։")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Փորձում ենք ստանալ ցուցակը
if st.button("Ցույց տալ հասանելի մոդելները"):
    try:
        st.info("Կապվում ենք Google-ին...")
        found_any = False
        
        # Հարցնում ենք Google-ին, թե ինչ կա "մենյուում"
        for m in genai.list_models():
            # Մեզ պետք են մենակ նրանք, որոնք տեքստ են գրում (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                st.success(f"✅ Գտնվեց: `{m.name}`")
                found_any = True
        
        if not found_any:
            st.warning("Ցավոք, հասանելի մոդելներ չգտնվեցին։ Գուցե API Key-ը սահմանափակում ունի՞:")
            
    except Exception as e:
        st.error(f"Սխալ տեղի ունեցավ: {e}")
        st.write("Խորհուրդ. Ստուգեք requirements.txt ֆայլը:")
