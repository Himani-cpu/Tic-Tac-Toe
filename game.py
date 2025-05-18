import streamlit as st
import numpy as np
import pandas as pd
import random
from datetime import datetime
import base64
from streamlit.components.v1 import html

# Initialize session state
def initialize_game():
    return {
        'board': np.full((3, 3), '', dtype=str),
        'current_player': 'X',
        'winner': None,
        'game_over': False,
        'move_count': 0,
        'player_names': {'X': 'Player 1', 'O': 'AI'},
        'player_emojis': {'X': '😊', 'O': '🤖'},
        'player_colors': {'X': '#FF5733', 'O': '#3385FF'},
        'scores': {'X': 0, 'O': 0, 'ties': 0},
        'game_history': [],
        'theme': 'light',
        'game_mode': 'single_player',
        'difficulty': 'moderate',
        'animations': True
    }

if 'game_state' not in st.session_state:
    st.session_state.game_state = initialize_game()

# WORKING CONFETTI FUNCTION
def trigger_confetti():
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    function fire() {
        confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 },
            zIndex: 1000
        });
    }
    fire();
    </script>
    """
    html(confetti_js, height=0, width=0)

# AI moves
def ai_move():
    board = st.session_state.game_state['board']
    difficulty = st.session_state.game_state['difficulty']
    
    # Easy mode - random moves
    if difficulty == 'easy':
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else (None, None)
    
    # Moderate mode - blocks wins but doesn't force them
    elif difficulty == 'moderate':
        # Check if AI can win
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    if check_winner(board) == 'O':
                        board[i][j] = ''
                        return (i, j)
                    board[i][j] = ''
        
        # Block player's winning move
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    if check_winner(board) == 'X':
                        board[i][j] = ''
                        return (i, j)
                    board[i][j] = ''
        
        # Take center if available
        if board[1][1] == '':
            return (1, 1)
        
        # Take a corner
        corners = [(0,0), (0,2), (2,0), (2,2)]
        random.shuffle(corners)
        for corner in corners:
            if board[corner[0]][corner[1]] == '':
                return corner
        
        # Take any available space
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else (None, None)
    
    # Hard mode - uses minimax algorithm
    elif difficulty == 'hard':
        best_score = -float('inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, 0, False)
                    board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif np.all(board != ''):
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    return None

def make_move(row, col):
    game_state = st.session_state.game_state
    
    if game_state['game_over'] or game_state['board'][row][col] != '':
        return
    
    game_state['board'][row][col] = game_state['current_player']
    game_state['move_count'] += 1
    
    # Check for winner
    winner = check_winner(game_state['board'])
    if winner:
        game_state['winner'] = winner
        game_state['game_over'] = True
        game_state['scores'][winner] += 1
        game_state['game_history'].append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'player1': game_state['player_names']['X'],
            'player2': game_state['player_names']['O'],
            'winner': game_state['player_names'][winner] if winner != 'tie' else 'Tie',
            'mode': 'Multiplayer' if game_state['game_mode'] == 'multiplayer' else 'Single Player',
            'difficulty': game_state['difficulty'] if game_state['game_mode'] == 'single_player' else 'N/A'
        })
        if game_state['animations']:
            trigger_confetti()  # This will now work
    elif game_state['move_count'] == 9:
        game_state['game_over'] = True
        game_state['winner'] = 'tie'
        game_state['scores']['ties'] += 1
        game_state['game_history'].append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'player1': game_state['player_names']['X'],
            'player2': game_state['player_names']['O'],
            'winner': 'Tie',
            'mode': 'Multiplayer' if game_state['game_mode'] == 'multiplayer' else 'Single Player',
            'difficulty': game_state['difficulty'] if game_state['game_mode'] == 'single_player' else 'N/A'
        })
    else:
        game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
        if game_state['game_mode'] == 'single_player' and game_state['current_player'] == 'O':
            row, col = ai_move()
            if row is not None and col is not None:
                make_move(row, col)

def display_board():
    game_state = st.session_state.game_state
    theme = game_state['theme']
    
    # Define button styles with larger emoji size
    button_styles = {
        'light': {
            'background': '#ffffff',
            'color': '#000000',
            'hover': '#f0f0f0'
        },
        'dark': {
            'background': '#2e2e2e',
            'color': '#ffffff',
            'hover': '#3e3e3e'
        },
        'neon': {
            'background': '#0f0f23',
            'color': '#00ff41',
            'hover': '#1f1f33'
        },
        'pastel': {
            'background': '#ffd6e0',
            'color': '#6b5b95',
            'hover': '#ffecf1'
        }
    }
    
    # Apply button styles with larger emoji size
    st.markdown(f"""
    <style>
        div.stButton > button:first-child {{
            background-color: {button_styles[theme]['background']};
            color: {button_styles[theme]['color']};
            border-radius: 10px;
            border: 2px solid {button_styles[theme]['color']};
            height: 120px;
            width: 100%;
            font-size: 64px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
        }}
        div.stButton > button:first-child:hover {{
            background-color: {button_styles[theme]['hover']};
            transform: scale(1.02);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    for row in range(3):
        cols = st.columns([1, 1, 1])
        for col in range(3):
            with cols[col]:
                cell_value = game_state['board'][row][col]
                display_value = ''
                if cell_value == 'X':
                    display_value = f"{game_state['player_emojis']['X']}"
                elif cell_value == 'O':
                    display_value = f"{game_state['player_emojis']['O']}"
                
                if st.button(
                    display_value,
                    key=f'{row}-{col}',
                    on_click=make_move,
                    args=(row, col),
                    disabled=game_state['game_over'] or cell_value != ''
                ):
                    pass

def reset_game():
    game_state = st.session_state.game_state
    game_state['board'] = np.full((3, 3), '', dtype=str)
    game_state['current_player'] = 'X'
    game_state['winner'] = None
    game_state['game_over'] = False
    game_state['move_count'] = 0

def download_game_history():
    game_state = st.session_state.game_state
    df = pd.DataFrame(game_state['game_history'])
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="tic_tac_toe_history.csv">Download Game History</a>'
    st.markdown(href, unsafe_allow_html=True)

def display_leaderboard():
    game_state = st.session_state.game_state
    
    if not game_state['game_history']:
        st.info("No games played yet. Start playing to see leaderboard!")
        return
    
    # Create leaderboard data
    leaderboard_data = []
    for game in game_state['game_history']:
        if game['winner'] != 'Tie':
            leaderboard_data.append({
                'Player': game['winner'],
                'Wins': 1,
                'Mode': game['mode'],
                'Date': game['date']
            })
    
    if not leaderboard_data:
        st.info("No winners yet. Play more games!")
        return
    
    df = pd.DataFrame(leaderboard_data)
    leaderboard = df.groupby('Player').agg({
        'Wins': 'sum',
        'Mode': lambda x: x.mode()[0],
        'Date': 'max'
    }).reset_index().sort_values('Wins', ascending=False)
    
    # Display with nice formatting
    st.subheader("🏆 Player Rankings")
    
    cols = st.columns([1, 3, 2, 2])
    with cols[0]:
        st.markdown("**Rank**")
    with cols[1]:
        st.markdown("**Player**")
    with cols[2]:
        st.markdown("**Wins**")
    with cols[3]:
        st.markdown("**Last Win**")
    
    for i, (_, row) in enumerate(leaderboard.iterrows()):
        cols = st.columns([1, 3, 2, 2])
        with cols[0]:
            st.markdown(f"#{i+1}")
        with cols[1]:
            st.markdown(f"**{row['Player']}**")
        with cols[2]:
            st.progress(row['Wins'] / max(leaderboard['Wins']), 
                        text=f"{row['Wins']} wins")
        with cols[3]:
            st.markdown(row['Date'].split()[0])

def main():
    game_state = st.session_state.game_state
    
    # Sidebar for settings
    with st.sidebar:
        st.header("🎛️ Game Settings")
        
        # Theme selection
        game_state['theme'] = st.selectbox(
            "Select Theme",
            ['light', 'dark', 'neon', 'pastel'],
            index=['light', 'dark', 'neon', 'pastel'].index(game_state['theme'])
        )
        
        # Animation toggle
        game_state['animations'] = st.toggle(
            "Animations", 
            value=game_state['animations']
        )
        
        # Game mode selection
        game_mode = st.radio(
            "Game Mode",
            ['single_player', 'multiplayer'],
            format_func=lambda x: "Single Player" if x == 'single_player' else "Multiplayer",
            index=0 if game_state['game_mode'] == 'single_player' else 1
        )
        
        if game_mode != game_state['game_mode']:
            game_state['game_mode'] = game_mode
            if game_mode == 'single_player':
                game_state['player_names']['O'] = 'AI'
                game_state['player_emojis']['O'] = '🤖'
            else:
                game_state['player_names']['O'] = 'Player 2'
                game_state['player_emojis']['O'] = '😎'
            reset_game()
        
        # Difficulty level (only for single player)
        if game_state['game_mode'] == 'single_player':
            game_state['difficulty'] = st.select_slider(
                "AI Difficulty",
                options=['easy', 'moderate', 'hard'],
                value=game_state['difficulty']
            )
        
        # Player names (only for multiplayer)
        if game_state['game_mode'] == 'multiplayer':
            game_state['player_names']['X'] = st.text_input("Player 1 Name", value=game_state['player_names']['X'])
            game_state['player_names']['O'] = st.text_input("Player 2 Name", value=game_state['player_names']['O'])
            
            col1, col2 = st.columns(2)
            with col1:
                game_state['player_emojis']['X'] = st.selectbox(
                    "Player 1 Emoji",
                    ['😊', '😎', '🤠', '❌', '⭕', '🐱', '🐶'],
                    index=['😊', '😎', '🤠', '❌', '⭕', '🐱', '🐶'].index(game_state['player_emojis']['X'])
                )
            with col2:
                game_state['player_emojis']['O'] = st.selectbox(
                    "Player 2 Emoji",
                    ['😊', '😎', '🤠', '❌', '⭕', '🐱', '🐶'],
                    index=['😊', '😎', '🤠', '❌', '⭕', '🐱', '🐶'].index(game_state['player_emojis']['O'])
                )
        
        st.button("Reset Game", on_click=reset_game)
    
    # Main game area
    st.title("🎮 Tic-Tac-Toe")
    st.subheader(f"⚡ Game Mode: {'Single Player' if game_state['game_mode'] == 'single_player' else 'Multiplayer'} ⚡")
    
    # Display current player or winner
    if game_state['winner']:
        if game_state['winner'] == 'tie':
            st.success("It's a tie! 🤝")
        else:
            winner_name = game_state['player_names'][game_state['winner']]
            st.success(f"🎉 {winner_name} {game_state['player_emojis'][game_state['winner']]} wins! 🎉")
    elif not game_state['game_over']:
        current_player_name = game_state['player_names'][game_state['current_player']]
        st.write(f"Current turn: {current_player_name} {game_state['player_emojis'][game_state['current_player']]}")
    
    # Display the board with larger emojis
    display_board()
    
    # Scoreboard
    st.subheader("🧮 Scoreboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(game_state['player_names']['X'], game_state['scores']['X'])
    with col2:
        st.metric("Ties", game_state['scores']['ties'])
    with col3:
        st.metric(game_state['player_names']['O'], game_state['scores']['O'])
    
    # Game history
    st.subheader("📜 Game History")
    if game_state['game_history']:
        df = pd.DataFrame(game_state['game_history'])
        st.dataframe(df.sort_values('date', ascending=False))
        download_game_history()
    else:
        st.info("No games played yet. Start playing to see history!")
    
    # Leaderboard
    display_leaderboard()

if __name__ == "__main__":
    main()