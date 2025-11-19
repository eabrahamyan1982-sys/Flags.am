import streamlit as st
import google.generativeai as genai

# Կայքի կարգավորումներ
st.set_page_config(page_title="Դրոշների Վիկտորինա", page_icon="🇦🇲")

# Ստուգում ենք բանալին
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Բանալին բացակայում է Secrets-ից:")
    st.stop()

# Կապում ենք Google AI-ն
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Փոխեցինք մոդելը gemini-pro-ի, որը ավելի կայուն է
model = genai.GenerativeModel('gemini-pro')

st.title("🇦🇲 Դրոշների Ուրախ Վիկտորինա")
st.write("Այս խաղը վարում է Արհեստական Բանականությունը (AI):")

# Հիշողության պահպանում
if "question" not in st.session_state:
    st.session_state.question = None

def get_new_question():
    with st.spinner('AI-ը մտածում է նոր հարց... 🤖'):
        try:
            prompt = "Գրիր 1 հետաքրքիր վիկտորինայի հարց աշխարհի երկրների դրոշների մասին երեխաների համար հայերեն լեզվով: Միայն հարցը գրիր, առանց պատասխանի:"
            response = model.generate_content(prompt)
            st.session_state.question = response.text
        except Exception as e:
            st.error(f"Սխալ եղավ: {e}")

# Կոճակ
if st.button("🎲 Ստանալ Նոր Հարց") or st.session_state.question is None:
    get_new_question()

# Ցույց տալ հարցը և ստուգել
if st.session_state.question:
    st.info(st.session_state.question)
    
    user_answer = st.text_input("Գրիր պատասխանը այստեղ և սեղմիր Enter:", key="user_input")

    if user_answer:
        validation_prompt = f"Հարցը՝ '{st.session_state.question}'. Երեխայի պատասխանը՝ '{user_answer}'. Ստուգիր՝ ճիշտ է թե սխալ, և պատասխանիր ուրախ հայերենով (օգտագործիր էմոջիներ):"
        
        with st.spinner('Ստուգում ենք...'):
            try:
                res = model.generate_content(validation_prompt)
                if "ճիշտ" in res.text.lower() or "ապրես" in res.text.lower():
                    st.success(res.text)
                    st.balloons()
                else:
                    st.warning(res.text)
            except:
                st.error("AI-ը չկարողացավ պատասխանել, փորձեք նորից:")
