import random
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QFrame

def create_board():
    board = [[0] * 4 for _ in range(4)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

def rotate_board(board):
    return [list(reversed(col)) for col in zip(*board)]

def merge_tiles(row):
    new_row = [0] * 4
    index = 0
    for tile in row:
        if tile != 0:
            if new_row[index] == 0:
                new_row[index] = tile
            elif new_row[index] == tile:
                new_row[index] *= 2
                index += 1
            else:
                index += 1
                new_row[index] = tile
    return new_row

def move_left(board):
    new_board = [merge_tiles(row) for row in board]
    return new_board

def move_right(board):
    new_board = [list(reversed(merge_tiles(row))) for row in board]
    return new_board

def move_up(board):
    rotated_board = rotate_board(board)
    new_board = rotate_board(move_left(rotated_board))
    return new_board

def move_down(board):
    rotated_board = rotate_board(board)
    new_board = rotate_board(move_right(rotated_board))
    return new_board

def can_move(board):
    for row in board:
        if 0 in row:
            return True
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return True
    return False

def has_won(board):
    for row in board:
        if 2048 in row:
            return True
    return False

COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

class Game2048Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("2048")

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)

        self.tiles = []

        self.init_board()

        central_widget = QFrame()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.resize(400, 400)

        self.board = create_board()
        self.update_board()

    def init_board(self):
        for i in range(4):
            row_tiles = []
            for j in range(4):
                tile = QLabel()
                tile.setAlignment(Qt.AlignCenter)
                tile.setFixedSize(80, 80)
                tile.setStyleSheet("background-color: #cdc1b4; color: #776e65; font-size: 24px; font-weight: bold")
                self.grid_layout.addWidget(tile, i, j)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def update_board(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                tile = self.tiles[i][j]
                tile.setText(str(value) if value != 0 else "")
                tile.setStyleSheet(
                    f"background-color: {COLORS.get(value, '#cdc1b4')}; color: {'#776e65' if value <= 4 else '#f9f6f2'}; font-size: {32 - len(str(value)) * 2}px; font-weight: {'bold' if value <= 4 else 'normal'}")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W or key == Qt.Key_Up:
            self.board = move_up(self.board)
        elif key == Qt.Key_S or key == Qt.Key_Down:
            self.board = move_down(self.board)
        elif key == Qt.Key_A or key == Qt.Key_Left:
            self.board = move_left(self.board)
        elif key == Qt.Key_D or key == Qt.Key_Right:
            self.board = move_right(self.board)
        else:
            super().keyPressEvent(event)
            return

        if has_won(self.board):
            print("Congratulations! You won!")
            # Perform any desired action when the player wins

        if not can_move(self.board):
            print("Game over. You lost.")
            # Perform any desired action when the game is over

        add_random_tile(self.board)
        self.update_board()

        super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Game2048Window()
    window.show()
    sys.exit(app.exec())