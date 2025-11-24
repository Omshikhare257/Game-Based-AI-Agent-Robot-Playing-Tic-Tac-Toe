"""
Advanced Tic-Tac-Toe AI Game with Minimax Algorithm - Streamlit Version
Student: Mr Om Jotiram Shikhare
Course: AI in Robotics

Streamlit web app version with:
- Multiple difficulty levels
- Improved UI/UX with modern design
- Game history and statistics
- Combo counter and streaks
- Time tracking
"""

import streamlit as st
import copy
import time
import json
from pathlib import Path
from enum import Enum


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class TicTacToeGame:
    """Handles the game logic and board state"""
    
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.move_count = 0
        self.start_time = None
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.move_count += 1
            return True
        return False
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        return all(cell != ' ' for row in self.board for cell in row)
    
    def get_empty_cells(self):
        """Get all empty cells on the board"""
        empty = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty.append((i, j))
        return empty
    
    def reset(self):
        """Reset the board"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.move_count = 0
        self.start_time = time.time()


class MinimaxAI:
    """AI player using Minimax algorithm with difficulty levels"""
    
    def __init__(self, ai_player='O', human_player='X', difficulty=Difficulty.HARD):
        self.ai_player = ai_player
        self.human_player = human_player
        self.difficulty = difficulty
    
    def evaluate(self, board):
        """Evaluate the board state"""
        winner = self.check_winner_static(board)
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        return 0
    
    def check_winner_static(self, board):
        """Static method to check winner for a given board"""
        for row in board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]
        
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        
        return None
    
    def is_full_static(self, board):
        """Check if board is full"""
        return all(cell != ' ' for row in board for cell in row)
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm implementation"""
        score = self.evaluate(board)
        
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if self.is_full_static(board):
            return 0
        
        if is_maximizing:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.ai_player
                        best = max(best, self.minimax(board, depth + 1, False))
                        board[i][j] = ' '
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.human_player
                        best = min(best, self.minimax(board, depth + 1, True))
                        board[i][j] = ' '
            return best
    
    def find_best_move(self, board):
        """Find the best move using Minimax with difficulty adjustment"""
        import random
        
        # Get empty cells
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    empty_cells.append((i, j))
        
        # Easy mode: random move
        if self.difficulty == Difficulty.EASY:
            return random.choice(empty_cells) if empty_cells else (-1, -1)
        
        # Find best moves using minimax
        best_val = -float('inf')
        best_moves = []
        board_copy = copy.deepcopy(board)
        
        for i in range(3):
            for j in range(3):
                if board_copy[i][j] == ' ':
                    board_copy[i][j] = self.ai_player
                    move_val = self.minimax(board_copy, 0, False)
                    board_copy[i][j] = ' '
                    
                    if move_val > best_val:
                        best_val = move_val
                        best_moves = [(i, j)]
                    elif move_val == best_val:
                        best_moves.append((i, j))
        
        # Medium mode: 30% chance of random move
        if self.difficulty == Difficulty.MEDIUM:
            if random.random() < 0.3 and empty_cells:
                return random.choice(empty_cells)
            return random.choice(best_moves) if best_moves else (-1, -1)
        
        # Hard mode: always best move
        return random.choice(best_moves) if best_moves else (-1, -1)


def load_stats():
    """Load statistics from session state or file"""
    stats_file = Path("tictactoe_stats_streamlit.json")
    default_stats = {
        'wins': 0,
        'losses': 0,
        'draws': 0,
        'win_streak': 0,
        'best_time': float('inf'),
        'games_played': 0,
        'difficulty_wins': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0}
    }
    
    if stats_file.exists():
        try:
            with open(stats_file, 'r') as f:
                return json.load(f)
        except Exception:
            return default_stats
    return default_stats


def save_stats(stats):
    """Save statistics to file"""
    stats_file = Path("tictactoe_stats_streamlit.json")
    try:
        with open(stats_file, 'w') as f:
            json.dump(stats, f)
    except Exception:
        pass


def update_stats(stats, result, time_taken, difficulty):
    """Update statistics after a game"""
    stats['games_played'] += 1
    
    if result == 'W':
        stats['wins'] += 1
        stats['win_streak'] += 1
        stats['difficulty_wins'][difficulty] += 1
        if time_taken < stats['best_time']:
            stats['best_time'] = time_taken
    elif result == 'L':
        stats['losses'] += 1
        stats['win_streak'] = 0
    else:
        stats['draws'] += 1
        stats['win_streak'] = 0
    
    save_stats(stats)
    return stats


def get_cell_style(cell, winner_cells=None, row=None, col=None):
    """Get CSS style for a cell"""
    if cell == 'X':
        color = '#3498db'
    elif cell == 'O':
        color = '#e74c3c'
    else:
        color = '#95a5a6'
    
    bg_color = '#2ecc71' if winner_cells and (row, col) in winner_cells else '#34495e'
    
    return f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    ">
        {cell if cell != ' ' else ''}
    </div>
    """


def get_winning_cells(game):
    """Get winning cell positions"""
    board = game.board
    
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != ' ':
            return [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return [(0, 2), (1, 1), (2, 0)]
    
    return None


def main():
    st.set_page_config(
        page_title="Tic-Tac-Toe AI",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #1a1a2e;
    }
    .stButton>button {
        width: 100%;
        height: 120px;
        font-size: 60px;
        font-weight: bold;
        border-radius: 10px;
        background-color: #34495e;
        color: #ecf0f1;
        border: 2px solid #16213e;
    }
    .stButton>button:hover {
        background-color: #0f3460;
        border-color: #3498db;
    }
    .stButton>button:disabled {
        background-color: #2c3e50;
        color: #7f8c8d;
    }
    h1 {
        color: #3498db;
        text-align: center;
    }
    h2, h3 {
        color: #ecf0f1;
    }
    .metric-card {
        background-color: #16213e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = TicTacToeGame()
        st.session_state.game.start_time = time.time()
        st.session_state.game_active = True
        st.session_state.combo = 0
        st.session_state.stats = load_stats()
    
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = Difficulty.HARD
    
    if 'ai' not in st.session_state:
        st.session_state.ai = MinimaxAI('O', 'X', st.session_state.difficulty)
    
    # Header
    st.markdown("<h1>⚡ ADVANCED TIC-TAC-TOE AI ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #95a5a6;'>Powered by Minimax Algorithm | By Mr Om Jotiram Shikhare</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎮 Game Controls")
        
        # Difficulty selection
        st.markdown("### 🎚️ Difficulty Level")
        difficulty_option = st.radio(
            "Select difficulty:",
            ["EASY", "MEDIUM", "HARD"],
            index=2,
            key="diff_radio"
        )
        
        diff_map = {'EASY': Difficulty.EASY, 'MEDIUM': Difficulty.MEDIUM, 'HARD': Difficulty.HARD}
        if diff_map[difficulty_option] != st.session_state.difficulty:
            st.session_state.difficulty = diff_map[difficulty_option]
            st.session_state.ai = MinimaxAI('O', 'X', st.session_state.difficulty)
        
        st.markdown("---")
        
        # Statistics
        st.markdown("## 📊 Statistics")
        stats = st.session_state.stats
        wr = (stats['wins'] / max(1, stats['games_played']) * 100) if stats['games_played'] > 0 else 0
        best_time = int(stats['best_time']) if stats['best_time'] != float('inf') else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Games", stats['games_played'])
            st.metric("Wins", stats['wins'])
            st.metric("Losses", stats['losses'])
        with col2:
            st.metric("Draws", stats['draws'])
            st.metric("Win Rate", f"{wr:.1f}%")
            st.metric("Streak", stats['win_streak'])
        
        st.metric("Best Time", f"{best_time}s")
        st.metric("🔥 Combo", st.session_state.combo)
        
        st.markdown("---")
        
        # Timer
        if st.session_state.game_active and st.session_state.game.start_time:
            elapsed = int(time.time() - st.session_state.game.start_time)
            st.markdown(f"### ⏱️ Time: {elapsed}s")
        
        st.markdown("---")
        
        # Buttons
        if st.button("🔄 NEW GAME", use_container_width=True):
            st.session_state.game = TicTacToeGame()
            st.session_state.game.start_time = time.time()
            st.session_state.game_active = True
            st.rerun()
        
        if st.button("📈 RESET STATS", use_container_width=True):
            st.session_state.stats = {
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'win_streak': 0,
                'best_time': float('inf'),
                'games_played': 0,
                'difficulty_wins': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0}
            }
            save_stats(st.session_state.stats)
            st.rerun()
    
    # Main game area
    game = st.session_state.game
    winner = game.check_winner()
    winner_cells = get_winning_cells(game) if winner else None
    
    # Status message
    if winner:
        if winner == 'X':
            st.success("🎉 YOU WIN! Congratulations!")
        else:
            st.error("🤖 AI WINS! Better luck next time!")
    elif game.is_board_full():
        st.warning("🤝 It's a Draw!")
    elif st.session_state.game_active:
        st.info("🎯 Your Turn (X) - Click any empty cell!")
    
    # Game board
    st.markdown("<br>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            with cols[j]:
                cell = game.board[i][j]
                if cell == ' ' and st.session_state.game_active and not winner:
                    if st.button('⬜', key=f"btn_{i}_{j}", use_container_width=True):
                        # Player move
                        game.make_move(i, j, 'X')
                        
                        # Check if player won
                        if game.check_winner() == 'X':
                            st.session_state.game_active = False
                            time_taken = int(time.time() - game.start_time)
                            st.session_state.combo += 1
                            st.session_state.stats = update_stats(
                                st.session_state.stats, 'W', time_taken, difficulty_option
                            )
                            st.rerun()
                        elif game.is_board_full():
                            st.session_state.game_active = False
                            time_taken = int(time.time() - game.start_time)
                            st.session_state.combo = 0
                            st.session_state.stats = update_stats(
                                st.session_state.stats, 'D', time_taken, difficulty_option
                            )
                            st.rerun()
                        else:
                            # AI move
                            ai_move = st.session_state.ai.find_best_move(game.board)
                            if ai_move != (-1, -1):
                                game.make_move(ai_move[0], ai_move[1], 'O')
                                
                                # Check if AI won
                                if game.check_winner() == 'O':
                                    st.session_state.game_active = False
                                    time_taken = int(time.time() - game.start_time)
                                    st.session_state.combo = 0
                                    st.session_state.stats = update_stats(
                                        st.session_state.stats, 'L', time_taken, difficulty_option
                                    )
                                elif game.is_board_full():
                                    st.session_state.game_active = False
                                    time_taken = int(time.time() - game.start_time)
                                    st.session_state.combo = 0
                                    st.session_state.stats = update_stats(
                                        st.session_state.stats, 'D', time_taken, difficulty_option
                                    )
                        st.rerun()
                else:
                    # Display cell content
                    st.markdown(get_cell_style(cell, winner_cells, i, j), unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>🎓 AI in Robotics Project | Made with ❤️ and Python</p>
        <p>Algorithm: Minimax with Alpha-Beta Pruning</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()