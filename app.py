import streamlit as st
import google.generativeai as genai

# 1. Կապում ենք Google Gemini-ն (Բանալին վերցնում ենք Secrets-ից)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error(AIzaSyCIE918qcz1qfHHWsx_JWGqL2vkTLeCE-Y")
    st.stop()

# Մոդելի կարգավորում
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Կայքի տեսքը
st.set_page_config(page_title="Դրոշների Վիկտորինա", page_icon="🌍")
st.title("🌍 Դրոշների Ուրախ Վիկտորինա")
st.write("Այս խաղը վարում է Արհեստական Բանականությունը (AI):")

# 3. Հիշողության պահպանում (որպեսզի էջը թարմացնելիս հարցը չկորի)
if "question" not in st.session_state:
    st.session_state.question = None
if "answer" not in st.session_state:
    st.session_state.answer = None

# 4. Նոր հարց ստանալու ֆունկցիա
def get_new_question():
    with st.spinner('AI-ը մտածում է նոր հարց... 🤖'):
        prompt = "Գրիր 1 հետաքրքիր վիկտորինայի հարց աշխարհի երկրների դրոշների մասին երեխաների համար հայերեն լեզվով: Նաև տուր 3 տարբերակ (ա, բ, գ), որոնցից մեկը ճիշտ է: Վերջում գրիր ճիշտ պատասխանը առանձին տողով:"
        response = model.generate_content(prompt)
        st.session_state.question = response.text
        st.session_state.answer = None # Մաքրել նախորդ պատասխանը

# Կոճակ՝ նոր հարցի համար
if st.button("🎲 Ստանալ Նոր Հարց") or st.session_state.question is None:
    get_new_question()

# 5. Ցույց տալ հարցը
if st.session_state.question:
    st.markdown("---")
    st.write(st.session_state.question)
    
    # Պատասխանի դաշտ
    user_answer = st.text_input("Գրիր քո պատասխանը (օրինակ՝ ա, բ կամ երկրի անունը) և սեղմիր Enter:")

    if user_answer:
        # Ստուգում ենք պատասխանը AI-ի միջոցով
        validation_prompt = f"Հարցը սա էր՝ '{st.session_state.question}': Երեխան պատասխանել է՝ '{user_answer}': Ասա ճիշտ է թե սխալ, և բացատրիր կարճ ու ուրախ հայերենով:"
        
        with st.spinner('Ստուգում ենք... 🧐'):
            result = model.generate_content(validation_prompt)
            
        if "ճիշտ" in result.text.lower():
            st.success(result.text)
            st.balloons()
        else:
            st.info(result.text)
