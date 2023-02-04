import streamlit as st
import bingo

game = bingo.BingoGame()


def run_app():
    global game
    st.title("Bingo Caller")

    with st.sidebar:
        new_game = st.button("New game")
        load_game = st.button("Load previous game")
        save_game = st.button("Save actual game")

    col1, col2 = st.columns(2)

    if new_game:
        game.reset()

    if load_game:
        if not game.load_game():
            st.warning("No existing previous game")

    if save_game:
        if game.save_game():
            st.success("Game successfully saved")

    with col1:
        hide_table_row_index = """
        <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
        </style>
        """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        st.write(game.table_numbers.to_html(), unsafe_allow_html=True)

    with col2:
        next_call = st.button("Next Call")
        if next_call:
            number = game.call()
            st.write(f"## {number}")
