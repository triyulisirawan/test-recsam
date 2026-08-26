import random
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Computational Fluency Game",
    page_icon="🧮",
    layout="centered"
)

# --- Level Settings ---
LEVEL_SETTINGS = {
    'basic': {'max_num': 12},
    'intermediate': {'max_num': 25},
    'advanced': {'max_num': 50}
}
MAX_QUESTIONS_PER_LEVEL = 5

# --- Bilingual UI Messages ---
MESSAGES = {
    'en': {
        'title': "🚀 Computational Fluency Game 🚀",
        'info': "You have **{lives} ❤️ lives**. Advance levels by answering 3 questions correctly in a row or completing 5 questions in a level.",
        'choose_lang': "Select Language / Pilih Bahasa",
        'choose_level': "Choose your starting difficulty level:",
        'start_game': "Start Game",
        'restart_game': "Play Again / Restart",
        'question': "Question {q_num}: What is **{num1} {operation} {num2}**? 🤔",
        'submit': "Submit Answer",
        'correct': "Correct! 🎉",
        'incorrect': "Incorrect. ❌ The correct answer was **{correct_answer}**.",
        'no_lives': "Oh no! 😭 You've run out of lives.",
        'level_up_streak': "🎉 Level Up! You mastered **{level_name}** by answering 3 correctly in a row! 🚀",
        'level_up_completed': "✅ Level Up! You completed all questions in **{level_name}**! 🚀",
        'next_level': "Next level unlocked! Prepare yourself! 👇",
        'all_levels_completed': "🏆 Congratulations! You've completed all levels! You are a Math Master! ✨",
        'game_over': "--- Game Over! 🏁 ---",
        'questions_answered': "Total Questions Attempted: **{q_count}** 📝",
        'final_score': "Final Score: **{score}** 🏆",
        'try_again': "Better luck next time! 👍"
    },
    'id': {
        'title': "🚀 Permainan Kelancaran Berhitung 🚀",
        'info': "Anda memiliki **{lives} ❤️ nyawa**. Naikkan level dengan menjawab 3 pertanyaan dengan benar berturut-turut atau menyelesaikan 5 pertanyaan dalam satu level.",
        'choose_lang': "Pilih Bahasa / Select Language",
        'choose_level': "Pilih tingkat kesulitan awal Anda:",
        'start_game': "Mulai Permainan",
        'restart_game': "Main Lagi / Reset",
        'question': "Pertanyaan {q_num}: Berapakah **{num1} {operation} {num2}**? 🤔",
        'submit': "Kirim Jawaban",
        'correct': "Benar! 🎉",
        'incorrect': "Salah. ❌ Jawaban yang benar adalah **{correct_answer}**.",
        'no_lives': "Oh tidak! 😭 Nyawa Anda habis.",
        'level_up_streak': "🎉 Naik Level! Anda menguasai level **{level_name}** dengan menjawab 3 benar berturut-turut! 🚀",
        'level_up_completed': "✅ Naik Level! Anda menyelesaikan semua pertanyaan di level **{level_name}**! 🚀",
        'next_level': "Level selanjutnya terbuka! Bersiaplah! 👇",
        'all_levels_completed': "🏆 Selamat! Anda telah menyelesaikan semua level! Anda adalah Master Matematika! ✨",
        'game_over': "--- Permainan Selesai! 🏁 ---",
        'questions_answered': "Total Pertanyaan yang Dicoba: **{q_count}** 📝",
        'final_score': "Skor Akhir: **{score}** 🏆",
        'try_again': "Semoga berhasil di lain waktu! 👍"
    }
}

# --- Helper Functions ---
def generate_question(max_num):
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)

    if operation == '/':
        num2 = random.randint(1, max_num)
        max_possible_quotient = max_num // num2 if num2 != 0 else 1
        if max_possible_quotient == 0:
            max_possible_quotient = 1
        correct_answer = random.randint(1, max_possible_quotient)
        num1 = num2 * correct_answer
    else:
        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1

        if operation == '+':
            correct_answer = num1 + num2
        elif operation == '-':
            correct_answer = num1 - num2
        else:
            correct_answer = num1 * num2

    return num1, operation, num2, correct_answer

def init_game(lang, start_level):
    level_names = list(LEVEL_SETTINGS.keys())
    st.session_state.game_state = {
        'active': True,
        'lang': lang,
        'score': 0,
        'lives': 3,
        'total_questions_attempted': 0,
        'level_names': level_names,
        'current_level_index': level_names.index(start_level),
        'question_count_in_level': 0,
        'consecutive_correct': 0,
        'current_question': None,
        'game_over': False,
        'completed_all': False,
        'feedback': None
    }
    next_question()

def next_question():
    gs = st.session_state.game_state
    current_level_name = gs['level_names'][gs['current_level_index']]
    max_num = LEVEL_SETTINGS[current_level_name]['max_num']
    
    gs['question_count_in_level'] += 1
    gs['total_questions_attempted'] += 1
    num1, op, num2, ans = generate_question(max_num)
    gs['current_question'] = {
        'num1': num1,
        'op': op,
        'num2': num2,
        'correct_answer': ans
    }

def handle_answer(user_answer):
    gs = st.session_state.game_state
    correct = gs['current_question']['correct_answer']
    lang = gs['lang']
    msg = MESSAGES[lang]

    if user_answer == correct:
        gs['score'] += 10
        gs['consecutive_correct'] += 1
        gs['feedback'] = ('success', msg['correct'])
    else:
        gs['lives'] -= 1
        gs['consecutive_correct'] = 0
        gs['feedback'] = ('error', msg['incorrect'].format(correct_answer=correct))

    # Check Game Over by Lives
    if gs['lives'] <= 0:
        gs['game_over'] = True
        gs['active'] = False
        return

    # Check Level Up Conditions
    level_up = False
    current_level_name = gs['level_names'][gs['current_level_index']]

    if gs['consecutive_correct'] >= 3:
        level_up = True
        st.toast(msg['level_up_streak'].format(level_name=current_level_name.capitalize()), icon="🎉")
    elif gs['question_count_in_level'] >= MAX_QUESTIONS_PER_LEVEL:
        level_up = True
        st.toast(msg['level_up_completed'].format(level_name=current_level_name.capitalize()), icon="✅")

    if level_up:
        gs['current_level_index'] += 1
        gs['question_count_in_level'] = 0
        gs['consecutive_correct'] = 0

        # Check Win Condition
        if gs['current_level_index'] >= len(gs['level_names']):
            gs['game_over'] = True
            gs['completed_all'] = True
            gs['active'] = False
            return

    next_question()

# --- Main App Interface ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = {'active': False}

gs = st.session_state.game_state

st.title("🧮 Math Fluency Game")

# Game Configuration / Setup Menu
if not gs['active'] and not gs.get('game_over', False):
    lang = st.selectbox("Language / Bahasa", options=['id', 'en'], format_func=lambda x: "Bahasa Indonesia" if x == 'id' else "English")
    msg = MESSAGES[lang]

    st.subheader(msg['title'])
    start_level = st.selectbox(msg['choose_level'], options=['basic', 'intermediate', 'advanced'])

    if st.button(msg['start_game'], type="primary"):
        init_game(lang, start_level)
        st.rerun()

# Active Game View
elif gs['active']:
    lang = gs['lang']
    msg = MESSAGES[lang]

    st.caption(msg['info'].format(lives=gs['lives']))

    # Status Dashboard
    col1, col2, col3 = st.columns(3)
    current_level_name = gs['level_names'][gs['current_level_index']]
    col1.metric("Level", current_level_name.capitalize())
    col2.metric("Score", gs['score'])
    col3.metric("Lives", "❤️ " * gs['lives'])

    st.divider()

    # Display Feedback from Previous Answer
    if gs['feedback']:
        f_type, f_msg = gs['feedback']
        if f_type == 'success':
            st.success(f_msg)
        else:
            st.error(f_msg)

    # Question Display
    q = gs['current_question']
    st.subheader(
        msg['question'].format(
            q_num=gs['question_count_in_level'],
            num1=q['num1'],
            operation=q['op'],
            num2=q['num2']
        )
    )

    # Input Form
    with st.form(key=f"q_form_{gs['total_questions_attempted']}"):
        user_input = st.number_input("Jawaban Anda:", value=None, step=1, placeholder="Ketik angka di sini...")
        submit_btn = st.form_submit_button(msg['submit'], type="primary")

        if submit_btn:
            if user_input is not None:
                handle_answer(int(user_input))
                st.rerun()
            else:
                st.warning("Masukkan angka terlebih dahulu!")

# Game Over View
elif gs.get('game_over', False):
    lang = gs['lang']
    msg = MESSAGES[lang]

    st.header(msg['game_over'])

    if gs['feedback']:
        f_type, f_msg = gs['feedback']
        if f_type == 'error':
            st.error(f_msg)

    st.metric(label="Skor Akhir", value=gs['score'])
    st.write(msg['questions_answered'].format(q_count=gs['total_questions_attempted']))

    if gs['completed_all']:
        st.balloons()
        st.success(msg['all_levels_completed'])
    else:
        st.info(msg['try_again'])

    if st.button(msg['restart_game'], type="primary"):
        st.session_state.game_state = {'active': False}
        st.rerun()