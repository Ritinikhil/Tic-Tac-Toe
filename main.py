import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
import speech_recognition as sr
import pyttsx3
import random


class ModernButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 10px;
                color: #ecf0f1;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)


class ControlButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setFont(QFont('Arial', 10))
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2573a7;
            }
        """)


class ModernComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QComboBox {
                background-color: #3498db;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px 15px;
                min-width: 100px;
            }
            QComboBox:hover {
                background-color: #2980b9;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)


class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Tic Tac Toe")
        self.setMinimumSize(1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 16px;
            }
        """)

        # Initialize game state
        self.initialize_game_state()
        self.init_ui()

    def initialize_game_state(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.current_size = 3
        self.current_difficulty = "Easy"
        self.educational_mode = False
        self.current_player = 'X'
        self.board = []
        self.animations = []

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Modern Tic Tac Toe")
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3498db; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Control Panel
        control_panel = self.create_control_panel()
        main_layout.addLayout(control_panel)

        # Game Grid Container
        grid_container = QFrame()
        grid_container.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        grid_layout = QVBoxLayout(grid_container)

        # Game Grid
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        grid_layout.addLayout(self.grid_layout)
        main_layout.addWidget(grid_container)

        # Status Panel
        self.status_label = QLabel("Player X's turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                padding: 10px;
                border-radius: 5px;
                font-size: 18px;
            }
        """)
        main_layout.addWidget(self.status_label)

        # Create initial board
        self.create_board(3)

    def create_control_panel(self):
        control_panel = QHBoxLayout()
        control_panel.setSpacing(15)

        # Grid Size Selection
        size_label = QLabel("Grid Size:")
        self.size_combo = ModernComboBox()
        self.size_combo.addItems(["3x3", "5x5", "7x7"])
        self.size_combo.currentTextChanged.connect(self.change_grid_size)

        # Difficulty Selection
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = ModernComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])

        # Control Buttons
        self.rules_btn = ControlButton("Game Rules")
        self.voice_btn = ControlButton("Voice Command")
        self.educational_btn = ControlButton("Educational Mode")

        # Connect buttons
        self.rules_btn.clicked.connect(self.show_rules)
        self.voice_btn.clicked.connect(self.activate_voice_command)
        self.educational_btn.clicked.connect(self.toggle_educational_mode)

        # Add widgets to control panel
        for widget in [size_label, self.size_combo, difficulty_label,
                       self.difficulty_combo, self.rules_btn, self.voice_btn,
                       self.educational_btn]:
            control_panel.addWidget(widget)

        return control_panel

    def change_grid_size(self, size_text):
        """Handle grid size changes from the combo box"""
        size = int(size_text[0])  # Extract the number from "3x3", "5x5", or "7x7"
        self.current_size = size
        self.create_board(size)
        self.reset_game()

    def reset_game(self):
        """Reset the game state"""
        self.current_player = 'X'
        self.board = [['' for _ in range(self.current_size)] for _ in range(self.current_size)]
        self.status_label.setText("Player X's turn")

    def create_board(self, size):
        # Clear existing board
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.board = [['' for _ in range(size)] for _ in range(size)]
        button_size = min(600 // size, 100)  # Responsive button size

        # Create new board
        for i in range(size):
            for j in range(size):
                button = ModernButton()
                button.setFixedSize(button_size, button_size)
                button.clicked.connect(lambda checked, row=i, col=j:
                                       self.make_move(row, col))
                self.grid_layout.addWidget(button, i, j)

        # Center the grid
        for i in range(size):
            self.grid_layout.setRowStretch(i, 1)
            self.grid_layout.setColumnStretch(i, 1)

    def make_move(self, row, col):
        button = self.grid_layout.itemAtPosition(row, col).widget()
        if button.text() == '' and not self.check_winner():
            button.setText(self.current_player)
            self.board[row][col] = self.current_player

            if self.check_winner():
                self.show_game_over(f"Player {self.current_player} wins!")
            elif self.is_board_full():
                self.show_game_over("It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.setText(f"Player {self.current_player}'s turn")

    def check_winner(self):
        size = self.current_size
        # Check rows and columns
        for i in range(size):
            if all(self.board[i][j] == self.current_player for j in range(size)):
                return True
            if all(self.board[j][i] == self.current_player for j in range(size)):
                return True

        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(size)):
            return True
        if all(self.board[i][size - 1 - i] == self.current_player for i in range(size)):
            return True
        return False

    def is_board_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def show_game_over(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, "Game Over", message)
        self.reset_game()
        self.create_board(self.current_size)

    def show_rules(self):
        rules = """
        Tic Tac Toe Rules:
        1. The game is played on a grid of 3x3, 5x5, or 7x7
        2. Players take turns putting their marks (X or O) in empty squares
        3. The first player to get their marks in a row (up, down, across, or diagonally) wins
        4. When all squares are full, the game is over. If no player has won, the game is a draw
        """
        QMessageBox.information(self, "Game Rules", rules)

    def activate_voice_command(self):
        # Placeholder for voice command functionality
        self.status_label.setText("Voice commands not implemented yet")

    def toggle_educational_mode(self):
        self.educational_mode = not self.educational_mode
        self.educational_btn.setStyleSheet(
            "background-color: lightgreen;" if self.educational_mode else ""
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    game = TicTacToe()
    game.show()
    sys.exit(app.exec())
