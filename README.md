# 🕹️ Tic-Tac-Toe

Welcome to the ultimate Tic-Tac-Toe game built with Python and Streamlit! This modern web-based version of the classic game supports both Single Player (with AI) and Multiplayer (local) modes — with smart difficulty levels, custom emojis, dark/light themes, and more.

## 🚀 Features

🧍🏻‍♀️ **Single Player Mode**

Play 😎 against an intelligent AI 🤖 with 3 difficulty levels:

🟡 Easy: Random moves.

🟠 Medium: Blocks your winning moves.

🔴 Hard: Uses Minimax algorithm (unbeatable).

👫🏻 **Multiplayer Mode**

Two players take turns on the same device.

🎨 **Theme Toggle**

❄️ Light, 🌚 Dark, 🧩 Neon, 💗 Pastel mode options for better visual experience.

😄 **Custom Player Emojis**

Choose from emojis like '😊', '😎', '🤠', '❌', '⭕', '🐱', '🐶' for personalized gameplay.

🧠 **Smart Turn Handling**

Automatically detects whose turn it is and updates the UI.

🔁 **Instant Game Reset**

Click "New Round" anytime to restart the game.

📱 **Responsive Layout**

Works smoothly on desktop and mobile devices.

🔢 **Scoreboard**

Track how many games each player (or AI) has won.

Display 🎉 wins, 👎🏼 losses, and 🤝 ties.

📜 **Game History**

Maintain a list of all moves for each round.

🏆 **Player Ranking**

Show a summary of wins per player name (useful for Multiplayer or across different sessions).


## 🧰 Tech Stack
Frontend/UI: Streamlit

Backend Logic: Python

AI Logic: Minimax Algorithm (for unbeatable mode)


## 📦 Setup Instructions

**Clone the Repository**

bash
git clone https://github.com/Himani-cpu/Tic-Tac-Toe.git
cd tic-tac-toe-streamlit

**Install Dependencies**

pip install -r requirements.txt

**Run the App**

python -m streamlit run game.py


## 📁 Project Structure

game.py

requirements.txt

README.md


## 📖 How It Works

When in Single Player Mode, the AI calculates the best possible move based on difficulty.

In Multiplayer, each player takes turns clicking the board.

All UI updates are controlled with st.session_state to preserve state between reruns.


## 🙌 Acknowledgments

Inspired by the classic paper-pencil game 📝

Minimax AI adapted from various open-source references







