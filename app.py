import streamlit as st
import google.generativeai as genai

# --- ԿԱՅՔԻ ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ ---
st.set_page_config(page_title="Flags.am - Բացահայտիր Աշխարհը", page_icon="🇦🇲", layout="wide")

# --- ՍՏՈՒԳՈՒՄ ԵՆՔ ԲԱՆԱԼԻՆ ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Խնդրում ենք ավելացնել GOOGLE_API_KEY-ը Secrets բաժնում:")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- ՄԵՆՅՈՒԻ ՍՏԵՂԾՈՒՄ (Tabs) ---
# Այստեղ մենք ստեղծում ենք էջերը, ինչպես ձեր դիզայնում էր
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Գլխավոր", "🧠 Վիկտորինա", "🎨 Ստեղծիր Դրոշ", "🛒 Խանութ"])

# --- ԷՋ 1: ԳԼԽԱՎՈՐ (HOME) ---
with tab1:
    st.title("Բացահայտիր աշխարհը դրոշների միջոցով 🌍")
    st.markdown("### Սովորիր պատմությունը, ստուգիր գիտելիքներդ և զվարճացիր:")
    
    # Գեղեցիկ բաժիններ (Cards)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📚 **Դրոշների Պատմություն**\n\nԻմացիր, թե ինչ են նշանակում գույները։")
    with col2:
        st.success("🧠 **Վիկտորինա**\n\nԽաղա AI-ի հետ և շահիր մրցանակներ։")
    with col3:
        st.warning("🛍️ **Գնել Դրոշ**\n\nՊատվիրիր որակյալ դրոշներ։")

    st.divider()
    st.write("👈 Ընտրիր բաժինը վերևի մենյուից:")

# --- ԷՋ 2: ՎԻԿՏՈՐԻՆԱ (QUIZ - AI) ---
with tab2:
    st.header("🇦🇲 Դրոշների Ուրախ Վիկտորինա")
    st.caption("Այս խաղը վարում է Արհեստական Բանականությունը (Gemini 2.5)։")

    if "question" not in st.session_state:
        st.session_state.question = None

    def get_new_question():
        with st.spinner('AI-ը հարց է հորինում... 🤖'):
            try:
                prompt = "Գրիր 1 հետաքրքիր հարց դրոշների մասին երեխաների համար հայերենով: Առանց պատասխանի:"
                response = model.generate_content(prompt)
                st.session_state.question = response.text
            except Exception as e:
                st.error(f"Սխալ: {e}")

    col_game1, col_game2 = st.columns([1, 2])
    
    with col_game1:
        if st.button("🎲 Նոր Հարց", use_container_width=True):
            get_new_question()

    with col_game2:
        if st.session_state.question:
            st.info(st.session_state.question)
            user_answer = st.text_input("Գրիր պատասխանը:", key="quiz_input")
            
            if user_answer:
                with st.spinner('Ստուգում ենք...'):
                    val_prompt = f"Հարց: {st.session_state.question}. Պատասխան: {user_answer}. Ստուգիր և պատասխանիր հայերեն:"
                    res = model.generate_content(val_prompt)
                    st.success(res.text)
                    if "ճիշտ" in res.text.lower():
                        st.balloons()

# --- ԷՋ 3: ՍՏԵՂԾԻՐ ԴՐՈՇ (Creative) ---
with tab3:
    st.header("🎨 Նկարագրիր քո երազանքների դրոշը")
    desc = st.text_area("Օրինակ՝ Կապույտ դրոշ, մեջտեղում ոսկե առյուծ...")
    if st.button("Հորինել Պատմություն"):
        if desc:
            with st.spinner('AI-ը հորինում է այս դրոշի պատմությունը...'):
                story_prompt = f"Երեխան հորինել է դրոշ՝ '{desc}'. Հորինիր մի փոքրիկ լեգենդ այս երկրի մասին հայերենով:"
                story = model.generate_content(story_prompt)
                st.write(story.text)

# --- ԷՋ 4: ԽԱՆՈՒԹ (Shop) ---
with tab4:
    st.header("🛍️ Դրոշների Խանութ")
    st.write("Շուտով այստեղ կլինեն Հայաստանի լավագույն դրոշները...")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_Armenia.svg/320px-Flag_of_Armenia.svg.png", caption="Հայաստանի Եռագույն")
