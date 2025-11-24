# Game-Based-AI-Agent-Robot-Playing-Tic-Tac-Toe
 Build a Tic-Tac-Toe AI with GUI.
 TISS Tata institute of social science College project
 
# 🎮 Advanced Tic-Tac-Toe AI with Minimax Algorithm

An intelligent Tic-Tac-Toe game featuring an AI opponent powered by the **Minimax Algorithm** with multiple difficulty levels and modern UI.

**Student:** Mr Om Jotiram Shikhare 

---

## ✨ Features

- **Smart AI** using Minimax Algorithm (Easy, Medium, Hard modes)
- **Beautiful UI** with Dark/Light theme toggle
- **Game Statistics** tracking (wins, losses, streaks, best time)
- **Real-time Timer** and combo counter
- **Persistent Data** saved automatically

---

## 🧠 Minimax Algorithm

The AI uses the Minimax algorithm to make optimal decisions:

- **Evaluation**: +10 for AI win, -10 for human win, 0 for draw
- **Recursive Search**: Explores all possible moves
- **Depth Penalty**: Prefers quicker wins
- **Difficulty Levels**:
  - **Easy**: Random moves
  - **Medium**: 70% optimal, 30% random
  - **Hard**: Always optimal (unbeatable)

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7+
- Tkinter (comes with Python)

### Run the Game
```bash
git clone https://github.com/yourusername/tictactoe-ai-minimax.git
cd tictactoe-ai-minimax
python tictactoe_ai.py
```

---

## 🎮 How to Play

1. Select difficulty level (Easy/Medium/Hard)
2. Click any cell to place your 'X'
3. AI responds with 'O'
4. Get 3 in a row to win!
5. Use buttons to start new game, view stats, or change theme

---

## 📁 Project Structure

```
tictactoe-ai-minimax/
├── tictactoe_ai.py          # Main game file
├── tictactoe_stats.json     # Auto-generated stats
└── README.md                # This file
```

---

## 🔧 Technical Details

### Main Classes
- **TicTacToeGame**: Game logic and board management
- **MinimaxAI**: AI implementation with Minimax algorithm
- **GameStats**: Statistics tracking and persistence
- **TicTacToeGUI**: User interface and event handling

### Key Algorithm
```python
def minimax(board, depth, is_maximizing):
    if game_over:
        return evaluate_score(board)
    
    if is_maximizing:
        return max(minimax for all possible moves)
    else:
        return min(minimax for all possible moves)
```

---

## 👨‍💻 Author

**Mr Om Jotiram Shikhare**  
webapp link (web_app.py) :-https://game-based-ai-agent-robot-playing-tic-tac-toe-bpfqyqtdf9yxrs93.streamlit.app/
