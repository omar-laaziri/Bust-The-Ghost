from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLineEdit, QLabel, QCheckBox, QMessageBox
from game_logic import DistanceSense, update_probabilities, probabilities, bust, PlaceGhost, get_probabilities
from config import GRID_HEIGHT, GRID_WIDTH, INITIAL_CREDITS, BUSTS_ALLOWED, COLORS

class GhostBusterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bust the Ghost")
        self.credits = INITIAL_CREDITS
        self.busts_remaining = BUSTS_ALLOWED
        self.gx, self.gy = PlaceGhost()
        print(f"Ghost is at ({self.gx}, {self.gy})")
        self.initUI()

    def initUI(self):
        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        # Create the grid of buttons
        self.grid_buttons = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                button = QPushButton('', self)
                button.setFixedSize(50, 50)  # Adjust size as needed
                button.clicked.connect(lambda checked, x=i, y=j: self.on_grid_button_click(x, y))
                self.layout.addWidget(button, i, j)
                self.grid_buttons[i][j] = button

        # Entry fields for bust command
        self.entry_x = QLineEdit(self)
        self.entry_y = QLineEdit(self)
        self.layout.addWidget(self.entry_x, GRID_HEIGHT, 0)
        self.layout.addWidget(self.entry_y, GRID_HEIGHT, 1)
        self.entry_x.setText('X')
        self.entry_y.setText('Y')

        # Bust button
        bust_button = QPushButton('Bust', self)
        bust_button.clicked.connect(self.on_bust_button_click)
        self.layout.addWidget(bust_button, GRID_HEIGHT, 2, 1, 2)

        # Peep checkbox
        self.peep_checkbox = QCheckBox("Peep", self)
        self.peep_checkbox.stateChanged.connect(self.on_peep_toggle)
        self.layout.addWidget(self.peep_checkbox, GRID_HEIGHT, 4, 1, 2)

        # Labels for credits and busts remaining
        self.credits_label = QLabel(f"Credits: {self.credits}", self)
        self.layout.addWidget(self.credits_label, GRID_HEIGHT + 1, 0, 1, 3)

        self.busts_label = QLabel(f"Busts Remaining: {self.busts_remaining}", self)
        self.layout.addWidget(self.busts_label, GRID_HEIGHT + 1, 3, 1, 3)



    def on_grid_button_click(self, x, y):
        if self.credits > 0 and self.busts_remaining > 0:
            color = DistanceSense(x, y, self.gx, self.gy)  # Adjusted to use DistanceSense
            self.grid_buttons[x][y].setStyleSheet(f"background-color: {color};")
            self.credits -= 1
            update_probabilities(color, x, y)
            self.credits_label.setText(f"Credits: {self.credits}")
            if self.peep_checkbox.isChecked():
                self.update_peep()
        else:
            QMessageBox.information(self, "Game Over", "No more credits or busts remaining!")


    def on_bust_button_click(self):
        try:
            bust_x, bust_y = int(self.entry_x.text()), int(self.entry_y.text())
            if bust_x < 0 or bust_x >= GRID_WIDTH or bust_y < 0 or bust_y >= GRID_HEIGHT:
                print(bust_x, bust_y)
                QMessageBox.critical(self, "Error", "Invalid grid coordinates for busting.")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid integer coordinates.")
            return

        success, message = bust(bust_x, bust_y, self.gx, self.gy)
        QMessageBox.information(self, "Bust Attempt", message)
        if not success:
            self.busts_remaining -= 1
            self.busts_label.setText(f"Busts Remaining: {self.busts_remaining}")
            if self.busts_remaining <= 0:
                QMessageBox.information(self, "Game Over", "You've run out of busts!")
                self.close()
        else:
            self.close()

    def on_peep_toggle(self, state):
        self.update_peep()

    def update_peep(self):
        current_probabilities = get_probabilities()  # Use the function to get current probabilities
        if self.peep_checkbox.isChecked():
            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    prob_text = f"{current_probabilities[i][j]:.2f}"
                    self.grid_buttons[i][j].setText(prob_text)
        else:
            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    self.grid_buttons[i][j].setText('')

