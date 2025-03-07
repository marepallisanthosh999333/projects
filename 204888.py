import random
import streamlit as st

# Set page config for Streamlit
st.set_page_config(page_title="2048 Game", layout="centered")

# Define colors and fonts for the game
GRID_COLOR = "#bbb0a9"
EMPTY_CELL_COLOR = "#ffd1ae"
CELL_COLORS = {
    2: "#fcece1",
    4: "#f4e9cb",
    8: "#efb07c",
    16: "#f49444",
    32: "#ff7357",
    64: "#e54b2d",
    128: "#ece18f",
    256: "#fbe02c",
    512: "#ffda47",
    1024: "#ebb41e",
    2048: "#fbd84c",
}
CELL_NUMBER_COLOR = {
    2: "#61544f",
    4: "#61544f",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff",
}

# Initialize session state
if "matrix" not in st.session_state:
    st.session_state.matrix = [[0] * 4 for _ in range(4)]
    st.session_state.score = 0

# Function to start or reset the game
def start_game():
    st.session_state.matrix = [[0] * 4 for _ in range(4)]
    st.session_state.score = 0
    insert_tile()
    insert_tile()

# Function to insert a new tile
def insert_tile():
    row, col = random.randint(0, 3), random.randint(0, 3)
    while st.session_state.matrix[row][col] != 0:
        row, col = random.randint(0, 3), random.randint(0, 3)
    st.session_state.matrix[row][col] = random.choice([2, 4])

# Function to compress cells
def compress():
    new_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if st.session_state.matrix[i][j] != 0:
                new_matrix[i][pos] = st.session_state.matrix[i][j]
                pos += 1
    st.session_state.matrix = new_matrix

# Function to combine cells
def combine():
    for i in range(4):
        for j in range(3):
            if st.session_state.matrix[i][j] != 0 and st.session_state.matrix[i][j] == st.session_state.matrix[i][j + 1]:
                st.session_state.matrix[i][j] *= 2
                st.session_state.score += st.session_state.matrix[i][j]
                st.session_state.matrix[i][j + 1] = 0

# Function to reverse the matrix
def reverse():
    st.session_state.matrix = [row[::-1] for row in st.session_state.matrix]

# Function to transpose the matrix
def transpose():
    st.session_state.matrix = [list(row) for row in zip(*st.session_state.matrix)]

# Move functions
def move_left():
    compress()
    combine()
    compress()
    insert_tile()

def move_right():
    reverse()
    move_left()
    reverse()

def move_up():
    transpose()
    move_left()
    transpose()

def move_down():
    transpose()
    move_right()
    transpose()

# Check for game over
def is_game_over():
    if any(2048 in row for row in st.session_state.matrix):
        return "win"
    if any(0 in row for row in st.session_state.matrix):
        return None
    for i in range(4):
        for j in range(3):
            if st.session_state.matrix[i][j] == st.session_state.matrix[i][j + 1]:
                return None
    for i in range(3):
        for j in range(4):
            if st.session_state.matrix[i][j] == st.session_state.matrix[i + 1][j]:
                return None
    return "lose"

# Draw the game grid
def draw_grid():
    for row in st.session_state.matrix:
        cols = st.columns(4)
        for j, val in enumerate(row):
            color = CELL_COLORS.get(val, EMPTY_CELL_COLOR)
            text_color = CELL_NUMBER_COLOR.get(val, "#61544f")
            cols[j].markdown(
                f"<div style='background-color:{color}; color:{text_color}; "
                f"height:100px; text-align:center; font-size:30px; "
                f"line-height:100px; border-radius:5px;'>{val if val != 0 else ''}</div>",
                unsafe_allow_html=True,
            )

# Handle game over
def handle_game_over():
    status = is_game_over()
    if status == "win":
        st.success("🎉 You Win! 🎉")
    elif status == "lose":
        st.error("Game Over! 😢")

# Render UI
st.title("2048 Game")
st.write("Score:", st.session_state.score)

# Game control buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        move_left()
with col2:
    if st.button("⬆️"):
        move_up()
with col3:
    if st.button("➡️"):
        move_right()
if st.button("⬇️"):
    move_down()

draw_grid()
handle_game_over()

if st.button("Restart Game"):
    start_game()