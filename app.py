import random
import streamlit as st
from game import toss_coin
from questions import easy_questions, hard_questions
st.set_page_config(
    page_title="Head & Tail Quiz",
    page_icon="🪙",
    layout="centered"
)
# Session State
defaults = {
    "questions": [],
    "time_left": 15,
    "started": False,
    "score": 0,
    "question_index": 0,
    "coin_result": "",
    "player_name": ""
}
for key,value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
# CSS
st.markdown("""
<style>
.stApp{
background:#111111;
color:white;
}

h1,h2,h3{
color:gold;
text-align:center;
}
</style>
""",unsafe_allow_html=True)
st.title("🪙 Head & Tail Logo Quiz")
# HOME PAGE
if not st.session_state.started:
    player_name = st.text_input("Enter Your Name")
    if st.button("🎮 Start Game"):
        if player_name.strip()=="":
            st.warning("Please Enter Your Name")
        else:
            result = toss_coin()
            st.session_state.coin_result = result
            if result=="HEAD":
                st.session_state.questions = easy_questions.copy()
            else:
                st.session_state.questions = hard_questions.copy()
            random.shuffle(st.session_state.questions)
            st.session_state.player_name = player_name
            st.session_state.started=True
            st.session_state.score=0
            st.session_state.question_index=0
            st.rerun()
# GAME PAGE
else:
    st.success(
        f"Welcome {st.session_state.player_name}"
    )
    st.subheader("🪙 Coin Toss Result")
    st.success(
        st.session_state.coin_result
    )
    st.write("---")
    st.subheader("🏆 Score")
    st.progress(
        st.session_state.score / len(st.session_state.questions)
    )
    st.write(
        f"Score : {st.session_state.score}/{len(st.session_state.questions)}"
    )
    if st.session_state.question_index < len(st.session_state.questions):
        q = st.session_state.questions[
            st.session_state.question_index
        ]
        st.subheader(
            f"Question {st.session_state.question_index+1}"
        )
        st.image(
            q["image"],
            width=220
        )
        st.write(q["question"])
        answer = st.radio(
            "Choose Answer",
            q["options"],
            key=f"q{st.session_state.question_index}"
        )
        if st.button("Submit"):
            if answer == q["answer"]:
                st.success("Correct Answer ✅")
                st.session_state.score +=1
            else:
                st.error(
                    f"Wrong Answer ❌ Correct : {q['answer']}"
                )
            st.session_state.question_index +=1
            st.rerun()
    else:
        st.balloons()
        st.header("🎉 Quiz Completed")
        score = st.session_state.score
        total = len(st.session_state.questions)
        percentage = (score/total)*100
        st.success(
            f"Final Score : {score}/{total}"
        )
        st.write(
            f"Percentage : {percentage:.0f}%"
        )
        if percentage>=80:
            st.success("🏆 Excellent!")
        elif percentage>=50:
            st.info("👍 Good Job!")
        else:
            st.warning("😊 Keep Practicing!")
        if st.button("🔄 Play Again"):
            st.session_state.started=False
            st.session_state.score=0
            st.session_state.question_index=0
            st.session_state.player_name=""
            st.rerun()
            