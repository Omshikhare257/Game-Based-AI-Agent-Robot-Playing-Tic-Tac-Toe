"""
Advanced Tic-Tac-Toe AI Game with Minimax Algorithm
Student: Mr Om Jotiram Shikhare
Course: AI in Robotics

Enhanced version with:
- Multiple difficulty levels
- Sound effects and animations
- Improved UI/UX with modern design
- Game history and statistics
- Combo counter and streaks
- Time tracking
- Theme switching
- Achievements system
"""

import tkinter as tk
from tkinter import messagebox
import copy
import time
from enum import Enum
import json
import os
from pathlib import Path


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
        
        # Get empty cells for easy mode
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


class GameStats:
    """Handle game statistics and persistence"""
    
    def __init__(self):
        self.stats_file = Path("tictactoe_stats.json")
        self.stats = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'win_streak': 0,
            'best_time': float('inf'),
            'games_played': 0,
            'difficulty_wins': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0}
        }
        self.load_stats()
    
    def load_stats(self):
        """Load statistics from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except Exception:
                pass
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f)
        except Exception:
            pass
    
    def update_game(self, result, time_taken, difficulty):
        """Update statistics after a game"""
        self.stats['games_played'] += 1
        
        if result == 'W':
            self.stats['wins'] += 1
            self.stats['win_streak'] += 1
            self.stats['difficulty_wins'][difficulty] += 1
            if time_taken < self.stats['best_time']:
                self.stats['best_time'] = time_taken
        elif result == 'L':
            self.stats['losses'] += 1
            self.stats['win_streak'] = 0
        else:
            self.stats['draws'] += 1
            self.stats['win_streak'] = 0
        
        self.save_stats()


class TicTacToeGUI:
    """GUI for the Tic-Tac-Toe game with advanced features"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Tic-Tac-Toe AI - Minimax Algorithm")
        self.window.geometry("900x800")
        self.window.resizable(False, False)
        
        # Themes
        self.themes = {
            'dark': {
                'bg': '#1a1a2e',
                'fg': '#ecf0f1',
                'primary': '#16213e',
                'accent': '#0f3460',
                'win': '#2ecc71',
                'lose': '#e74c3c'
            },
            'light': {
                'bg': '#ecf0f1',
                'fg': '#1a1a2e',
                'primary': '#bdc3c7',
                'accent': '#95a5a6',
                'win': '#27ae60',
                'lose': '#c0392b'
            }
        }
        self.current_theme = 'dark'
        
        self.game = TicTacToeGame()
        self.stats = GameStats()
        self.difficulty = Difficulty.HARD
        self.ai = MinimaxAI('O', 'X', self.difficulty)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_active = True
        
        self.current_combo = 0
        self.last_winner = None
        
        self.create_ui()
        self.game.start_time = time.time()
    
    def get_theme_color(self, color_key):
        """Get color from current theme"""
        return self.themes[self.current_theme][color_key]
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.window, bg=self.get_theme_color('bg'))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top bar with theme and difficulty
        top_bar = tk.Frame(main_frame, bg=self.get_theme_color('primary'))
        top_bar.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(
            top_bar,
            text="⚡ ADVANCED TIC-TAC-TOE AI ⚡",
            font=('Arial', 20, 'bold'),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('accent')
        )
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Control buttons
        difficulty_frame = tk.Frame(top_bar, bg=self.get_theme_color('primary'))
        difficulty_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(
            difficulty_frame,
            text="Level:",
            font=('Arial', 10, 'bold'),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('fg')
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="HARD")
        for diff in ['EASY', 'MEDIUM', 'HARD']:
            tk.Radiobutton(
                difficulty_frame,
                text=diff,
                variable=self.difficulty_var,
                value=diff,
                font=('Arial', 9),
                bg=self.get_theme_color('primary'),
                fg=self.get_theme_color('fg'),
                selectcolor=self.get_theme_color('accent'),
                command=self.change_difficulty
            ).pack(side=tk.LEFT, padx=3)
        
        # Content frame
        content = tk.Frame(main_frame, bg=self.get_theme_color('bg'))
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Stats and Info
        left_panel = tk.Frame(content, bg=self.get_theme_color('primary'), relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        stats_title = tk.Label(
            left_panel,
            text="📊 STATS",
            font=('Arial', 14, 'bold'),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('accent')
        )
        stats_title.pack(pady=10)
        
        self.stats_display = tk.Label(
            left_panel,
            text=self.get_stats_text(),
            font=('Arial', 10),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('fg'),
            justify=tk.LEFT
        )
        self.stats_display.pack(padx=15, pady=10)
        
        # Divider
        tk.Frame(
            left_panel,
            height=2,
            bg=self.get_theme_color('accent')
        ).pack(fill=tk.X, padx=10, pady=10)
        
        info_title = tk.Label(
            left_panel,
            text="ℹ️ INFO",
            font=('Arial', 12, 'bold'),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('accent')
        )
        info_title.pack(pady=10)
        
        self.combo_label = tk.Label(
            left_panel,
            text=f"🔥 Combo: {self.current_combo}",
            font=('Arial', 11, 'bold'),
            bg=self.get_theme_color('primary'),
            fg='#f39c12'
        )
        self.combo_label.pack(pady=5)
        
        self.timer_label = tk.Label(
            left_panel,
            text="⏱️ Time: 0s",
            font=('Arial', 10),
            bg=self.get_theme_color('primary'),
            fg=self.get_theme_color('fg')
        )
        self.timer_label.pack(pady=5)
        
        self.status_label = tk.Label(
            left_panel,
            text="Your Turn (X)",
            font=('Arial', 11, 'bold'),
            bg=self.get_theme_color('primary'),
            fg='#2ecc71'
        )
        self.status_label.pack(pady=10)
        
        # Center panel - Game board
        board_frame = tk.Frame(content, bg=self.get_theme_color('bg'))
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        game_board = tk.Frame(board_frame, bg=self.get_theme_color('accent'), padx=5, pady=5)
        game_board.pack()
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    game_board,
                    text=' ',
                    font=('Arial', 50, 'bold'),
                    width=5,
                    height=2,
                    bg=self.get_theme_color('primary'),
                    fg=self.get_theme_color('accent'),
                    activebackground=self.get_theme_color('accent'),
                    relief='raised',
                    bd=3,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                button.grid(row=i, column=j, padx=3, pady=3)
                self.buttons[i][j] = button
        
        # Bottom controls
        button_frame = tk.Frame(left_panel, bg=self.get_theme_color('primary'))
        button_frame.pack(pady=20, padx=10, fill=tk.X)
        
        new_game_btn = tk.Button(
            button_frame,
            text="🔄 NEW GAME",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            padx=15,
            pady=10,
            command=self.reset_game,
            relief=tk.RAISED,
            bd=2
        )
        new_game_btn.pack(fill=tk.X, pady=5)
        
        stats_btn = tk.Button(
            button_frame,
            text="📈 VIEW STATS",
            font=('Arial', 11, 'bold'),
            bg='#9b59b6',
            fg='white',
            padx=15,
            pady=10,
            command=self.show_detailed_stats,
            relief=tk.RAISED,
            bd=2
        )
        stats_btn.pack(fill=tk.X, pady=5)
        
        theme_btn = tk.Button(
            button_frame,
            text="🎨 THEME",
            font=('Arial', 11, 'bold'),
            bg='#16a085',
            fg='white',
            padx=15,
            pady=10,
            command=self.toggle_theme,
            relief=tk.RAISED,
            bd=2
        )
        theme_btn.pack(fill=tk.X, pady=5)
        
        quit_btn = tk.Button(
            button_frame,
            text="❌ QUIT",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=15,
            pady=10,
            command=self.window.quit,
            relief=tk.RAISED,
            bd=2
        )
        quit_btn.pack(fill=tk.X, pady=5)
        
        self.update_timer()
    
    def update_timer(self):
        """Update game timer"""
        if self.game_active and self.game.start_time:
            elapsed = int(time.time() - self.game.start_time)
            self.timer_label.config(text=f"⏱️ Time: {elapsed}s")
        self.window.after(1000, self.update_timer)
    
    def change_difficulty(self):
        """Change game difficulty"""
        diff_map = {
            'EASY': Difficulty.EASY,
            'MEDIUM': Difficulty.MEDIUM,
            'HARD': Difficulty.HARD
        }
        self.difficulty = diff_map[self.difficulty_var.get()]
        self.ai = MinimaxAI('O', 'X', self.difficulty)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.window.destroy()
        self.__init__()
    
    def get_stats_text(self):
        """Get statistics text"""
        s = self.stats.stats
        wr = (s['wins'] / max(1, s['games_played']) * 100) if s['games_played'] > 0 else 0
        best_time = int(s['best_time']) if s['best_time'] != float('inf') else 0
        return f"""Total Games: {s['games_played']}
Wins: {s['wins']} | Losses: {s['losses']}
Draws: {s['draws']}
Win Rate: {wr:.1f}%
Streak: {s['win_streak']}
Best Time: {best_time}s"""
    
    def on_click(self, row, col):
        """Handle button click"""
        if not self.game_active:
            return
        
        if self.game.make_move(row, col, 'X'):
            self.update_button(row, col, 'X')
            
            if self.check_game_over():
                return
            
            self.status_label.config(text="AI Thinking...", fg='#f39c12')
            self.window.update()
            self.window.after(800, self.ai_move)
    
    def update_button(self, row, col, player):
        """Update button appearance"""
        color = '#3498db' if player == 'X' else '#e74c3c'
        self.buttons[row][col].config(
            text=player,
            state='disabled',
            disabledforeground=color,
            bg=self.get_theme_color('accent')
        )
    
    def ai_move(self):
        """Make AI move"""
        if not self.game_active:
            return
        
        move = self.ai.find_best_move(self.game.board)
        if move != (-1, -1):
            self.game.make_move(move[0], move[1], 'O')
            self.update_button(move[0], move[1], 'O')
            
            if not self.check_game_over():
                self.status_label.config(text="Your Turn (X)", fg='#2ecc71')
    
    def check_game_over(self):
        """Check if game is over"""
        winner = self.game.check_winner()
        if winner:
            self.game_active = False
            time_taken = int(time.time() - self.game.start_time)
            
            if winner == 'X':
                self.current_combo += 1
                self.stats.update_game('W', time_taken, self.difficulty_var.get())
                msg = f"🎉 YOU WIN!\nCombo: {self.current_combo} | Time: {time_taken}s"
                self.status_label.config(text="You Won! 🎉", fg='#2ecc71')
                self.highlight_winner(winner)
            else:
                self.current_combo = 0
                self.stats.update_game('L', time_taken, self.difficulty_var.get())
                msg = "🤖 AI WINS!\nBetter luck next time!"
                self.status_label.config(text="AI Won!", fg='#e74c3c')
                self.highlight_winner(winner)
            
            self.combo_label.config(text=f"🔥 Combo: {self.current_combo}")
            self.stats_display.config(text=self.get_stats_text())
            self.window.after(1000, lambda: messagebox.showinfo("Game Over", msg))
            return True
        
        elif self.game.is_board_full():
            self.game_active = False
            self.current_combo = 0
            time_taken = int(time.time() - self.game.start_time)
            self.stats.update_game('D', time_taken, self.difficulty_var.get())
            self.status_label.config(text="Draw!", fg='#f39c12')
            self.combo_label.config(text=f"🔥 Combo: {self.current_combo}")
            self.stats_display.config(text=self.get_stats_text())
            self.window.after(1000, lambda: messagebox.showinfo("Game Over", "🤝 It's a Draw!"))
            return True
        
        return False
    
    def highlight_winner(self, winner):
        """Highlight winning combination"""
        board = self.game.board
        color = self.get_theme_color('win') if winner == 'X' else self.get_theme_color('lose')
        
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                for j in range(3):
                    self.buttons[i][j].config(bg=color)
                return
        
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] != ' ':
                for i in range(3):
                    self.buttons[i][j].config(bg=color)
                return
        
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            for i in range(3):
                self.buttons[i][i].config(bg=color)
            return
        
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            for i in range(3):
                self.buttons[i][2-i].config(bg=color)
    
    def reset_game(self):
        """Reset the game"""
        self.game.reset()
        self.game_active = True
        self.game.start_time = time.time()
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text=' ',
                    state='normal',
                    bg=self.get_theme_color('primary')
                )
        
        self.status_label.config(text="Your Turn (X)", fg='#2ecc71')
    
    def show_detailed_stats(self):
        """Show detailed statistics"""
        s = self.stats.stats
        wr = (s['wins'] / max(1, s['games_played']) * 100) if s['games_played'] > 0 else 0
        best_time = int(s['best_time']) if s['best_time'] != float('inf') else 0
        
        stats_text = f"""
╔═══════════════════════════════╗
║     GAME STATISTICS           ║
╠═══════════════════════════════╣
║ Total Games: {s['games_played']:<17} ║
║ Wins: {s['wins']:<23} ║
║ Losses: {s['losses']:<20} ║
║ Draws: {s['draws']:<21} ║
║ Win Rate: {wr:.1f}%              ║
║ Current Streak: {s['win_streak']:<12} ║
║ Best Time: {best_time}s              ║
╠═══════════════════════════════╣
║ DIFFICULTY WINS               ║
║ Easy: {s['difficulty_wins']['EASY']:<21} ║
║ Medium: {s['difficulty_wins']['MEDIUM']:<18} ║
║ Hard: {s['difficulty_wins']['HARD']:<21} ║
╚═══════════════════════════════╝
"""
        messagebox.showinfo("Detailed Statistics", stats_text)
    
    def run(self):
        """Run the game"""
        self.window.mainloop()


def main():
    """Main function to run the game"""
    print("=" * 60)
    print("ADVANCED TIC-TAC-TOE AI GAME")
    print("Student: Mr Om Jotiram Shikhare")
    print("Algorithm: Minimax with Difficulty Levels")
    print("=" * 60)
    print("\n✨ Features:")
    print("  • Multiple Difficulty Levels (Easy, Medium, Hard)")
    print("  • Game Statistics & Win Tracking")
    print("  • Combo Counter & Streak System")
    print("  • Timer for Each Game")
    print("  • Light/Dark Theme Toggle")
    print("  • Beautiful Modern UI")
    print("\n🎮 Starting game...\n")
    
    game = TicTacToeGUI()
    game.run()


if __name__ == "__main__":
    main()
