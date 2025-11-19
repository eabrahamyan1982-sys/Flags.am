import streamlit as st
import google.generativeai as genai

# Էջի կարգավորում
st.set_page_config(page_title="Դրոշների Վիկտորինա", page_icon="🇦🇲")

# 1. Ստուգում ենք բանալին
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Բանալին գտնված չէ։ Խնդրում ենք ստուգել Secrets բաժինը։")
    st.stop()

# 2. Կապում ենք Google AI-ն
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Օգտագործում ենք ամենաթարմ մոդելը
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🇦🇲 Դրոշների Ուրախ Վիկտորինա")
st.write("Այս խաղը վարում է Արհեստական Բանականությունը (AI):")

# Հիշողություն (Session State)
if "question" not in st.session_state:
    st.session_state.question = None

# Ֆունկցիա՝ հարց ստանալու համար
def get_new_question():
    with st.spinner('AI-ը մտածում է նոր հարց... 🤖'):
        try:
            prompt = "Գրիր 1 հետաքրքիր վիկտորինայի հարց աշխարհի երկրների դրոշների մասին երեխաների համար հայերեն լեզվով: Միայն հարցը գրիր, առանց պատասխանի:"
            response = model.generate_content(prompt)
            st.session_state.question = response.text
        except Exception as e:
            st.error(f"Սխալ տեղի ունեցավ: {e}")

# Կոճակ
if st.button("🎲 Ստանալ Նոր Հարց"):
    get_new_question()

# Եթե հարց կա, ցույց տալ այն
if st.session_state.question:
    st.info(st.session_state.question)
    
    # Պատասխանի դաշտ
    user_answer = st.text_input("Գրիր քո պատասխանը այստեղ և սեղմիր Enter:", key="user_input")

    if user_answer:
        validation_prompt = f"Հարցը՝ '{st.session_state.question}'. Երեխայի պատասխանը՝ '{user_answer}'. Ստուգիր՝ ճիշտ է թե սխալ, և պատասխանիր ուրախ հայերենով (օգտագործիր էմոջիներ):"
        
        with st.spinner('Ստուգում ենք...'):
            try:
                res = model.generate_content(validation_prompt)
                st.success(res.text)
                st.balloons()
            except:
                st.error("Չհաջողվեց ստուգել պատասխանը։")
