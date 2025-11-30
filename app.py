import streamlit as st
import time
from backend import JumbleGame

if "backend" not in st.session_state:
    st.session_state.backend = JumbleGame()

backend: JumbleGame = st.session_state.backend

if backend.logged_in_user is None:
    st.title("JUMBLEE — Login / Register")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            ok, msg = backend.login_user(username, password)
            if ok:
                st.success(msg)
                if backend.name is None:
                    backend.name = backend.logged_in_user.title()
                st.rerun()
            else:
                st.error(msg)

    with register_tab:
        new_user = st.text_input("Create Username", key="reg_user")
        new_pass = st.text_input("Create Password", type="password", key="reg_pass")

        if st.button("Register"):
            ok, msg = backend.register_user(new_user, new_pass)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.info("If you already have an account — use Login tab. Otherwise register a new user.")
    st.stop()

st.sidebar.success(f"Logged in as: {backend.logged_in_user}")

if backend.name is None and backend.logged_in_user:
    backend.name = backend.logged_in_user.title()

col1, col2, col3 = st.columns([1.8, 3, 1])

with col2:
    try:
        st.image(
            r"C:\Users\chira\Desktop\SV_Python\Python_GUI_streamlit\Logo_Jumblee.jpg",
            width=200
        )
    except Exception:
        st.markdown("### JUMBLEE (image not found)")

st.title("JUMBLEE (Jumbled Words Game)")

starting_instr = st.checkbox("Show Game Starting Instructions")
if starting_instr:
    st.write("1. First you have enter your name in the name box below.")
    st.write("2. Then select a difficulty level: Easy, Medium, or Hard.")
    st.write("3. Choose the number of words you want to play with (1–50).")
    st.write("4. Click Start Game to begin.")

gameplay_instr = st.checkbox("Show Gameplay Rules")
if gameplay_instr:
    st.write("1. A jumbled word will be displayed on the screen.")
    st.write("2. Type your answer in the input box provided.")
    st.write("3. If you want hint click on the first letter hint button for first letter and for third letter hint click on the third letter hint button.")
    st.write("4. And if you want to skip the word click on the skip button.")
    st.write("5. And if you know the answer or try your answer click submit answer button to lock your answer.")
    st.write("6. Your score, level, total questions, accuracy and time taken per question will be shown after completing all the words.")

scoring_instr = st.checkbox("Show Scoring")
if scoring_instr:
    st.write("1. 10 points will be awarded for giving correct answers and within 5 seconds of time.")
    st.write("2. 7 points will be awarded for giving correct answers after 5 seconds of time.")
    st.write("3. 3 points will be awarded for giving correct answers after taking first hint.")
    st.write("4. 2 points will be awarded for giving correct answer after taking second hint.")
    st.write("5. No points will be deducted or awarded for skipping the word.")
    st.write("6. 5 points will be deducted for giving wrong answer.")
    st.write("7. 7 points will be deducted for giving wrong answer after taking first hint.")
    st.write("8. 9 points will be deducted for giving wrong answer after taking second hint.")

previous_instr = st.checkbox("Show Previous Instructions")
if previous_instr:
    st.write("1. Previous instructions will show you how many questions you have.")
    st.write("2. For saving for scores click on the save result to scoreboard.")
    st.write("3. For checking your previous scores click on the previous record button.")

if backend.name is None:
    name = st.text_input("Enter your display name:").title()
else:
    name = st.text_input("Enter your display name:", value=backend.name).title()

if backend.level is None:
    level = st.radio("Choose difficulty level:", ["easy", "medium", "hard"])
else:
    level = st.radio("Choose difficulty level:", ["easy", "medium", "hard"], index=["easy", "medium", "hard"].index(backend.level))
    st.success(f"{name} you chose {level} level. Good luck!")

total_words = st.slider("Select number of words (1-50):", min_value=1, max_value=50, value=5)

if st.button("Start Game"):
    if not name or not name.strip():
        st.warning("Please enter a valid display name first.")
    else:
        backend.start_new_game(name, level, total_words)
        if backend.logged_in_user is None:
            st.warning("No logged in user found. Please login again.")
        st.rerun()

if backend.name is not None and backend.word_pairs:
    st.markdown("---")
    st.subheader(f"Player: {backend.name} | Level: {backend.level} | Score: {backend.score}")

    if not backend.is_over():
        jumbled = backend.current_jumbled()
        st.write(f"Jumbled word ({backend.index + 1}/{backend.total_words}): **{jumbled}**")

        elapsed = int(time.time() - backend.start_time) if backend.start_time else 0
        st.write(f"⏱ Time elapsed: {elapsed:.2f} seconds")

        cols = st.columns(3)
        with cols[0]:
            if st.button("Hint (First letter)"):
                hint = backend.get_hint()
                if hint is not None:
                    st.info(f"Hint — first letter: **{hint}**")
                else:
                    st.info("No more hints available.")
        with cols[1]:
            if st.button("Hint (Third letter)"):
                if backend.hint_stage == 0:
                    _ = backend.get_hint()
                hint2 = backend.get_hint()
                if hint2 is not None and hint2 != "":
                    st.info(f"Hint — third letter: **{hint2}**")
                elif hint2 == "":
                    st.info("Third letter not available for this word.")
                else:
                    st.info("No more hints available.")
        with cols[2]:
            if st.button("Skip Word"):
                res = backend.submit_answer("")
                st.warning(f"You skipped. Correct answer: **{res['correct_answer']}**")
                st.rerun()

        key = f"answer_{backend.session_id}_{backend.index}"
        user_ans = st.text_input("Enter your answer:", key=key)

        if st.button("Submit Answer"):
            res = backend.submit_answer(user_ans)
            if res.get("user_result") is True:
                st.success(f"{res['message']} +{res['points']} points")
            elif res.get("user_result") is False:
                st.error(f"{res['message']} (Correct: {res['correct_answer']}) -> {res['points']} points")
            else:
                st.info(f"{res['message']} (Correct: {res['correct_answer']})")
            st.rerun()

    else:
        st.success(f"Game finished! Final score: {backend.score} out of {backend.total_words * 10}")
        st.write(f"Accuracy: {backend.accuracy_percent():.2f}%")
        st.write(f"Average time per question: {backend.average_time():.3f} seconds")

        st.subheader("Detailed history")
        for rec in backend.history:
            st.write(
                f"Q{rec['index']}: {rec['jumbled']} → Given: {rec['given']} | "
                f"Correct: {rec['correct']} | Time: {rec['time_taken']}s | Points: {rec['points']} | {rec['result']}"
            )

        if st.button("Save result to scoreboard"):
            ok = backend.save_scores_to_file()
            if ok:
                st.success("Saved to your user scoreboard.")
            else:
                st.error("Failed to save. Make sure you are logged in.")

        prev_scores = backend.get_previous_scores()
        if prev_scores:
            st.markdown("### Previous saved records (latest first)")
            for rec in reversed(prev_scores[-10:]):
                st.write(f"📅 {rec['date']} | Level: {rec['level']} | Score: {rec['score']} | Accuracy: {rec['accuracy']}% | Avg Time: {rec['avg_time']}s")

            if len(prev_scores) >= 1:
                last_saved = prev_scores[-1]
                try:
                    last_score = last_saved["score"]
                    current = backend.score
                    if current > last_score:
                        st.success(f"🔥 You improved compared to your last saved score ({last_score}). Current: {current}")
                    elif current < last_score:
                        st.warning(f"⬇ Your current score ({current}) is lower than your last saved ({last_score}).")
                    else:
                        st.info(f"➖ Same as last saved score: {current}")
                except Exception:
                    pass

        if st.button("Play Again"):
            st.session_state.backend = JumbleGame()
            st.session_state.backend.logged_in_user = backend.logged_in_user  # keep login
            st.rerun()

st.markdown("---")
st.header("View your previous records")
if st.button("Show My Scoreboard"):
    prev_scores = backend.get_previous_scores()

    if not prev_scores:
        st.info("You have no previous game records.")
    else:
        for rec in reversed(prev_scores):
            st.write(f"📅 {rec['date']} | Level: {rec['level']} | Score: {rec['score']} | Accuracy: {rec['accuracy']}% | Avg Time: {rec['avg_time']}s")

if st.sidebar.button("Logout"):
    st.session_state.backend = JumbleGame()
    st.sidebar.success("You have been logged out.")
    st.rerun()