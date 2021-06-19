# RPPOOP Mini-Project
# 2048-Game

#  Developers : S.R.S
#               a u a
#               n s g
#               k h a
#               e i r
#               t k 
#                 e 
#                 s 
#                 h 

# Importing requires modules
import random
import pygame
import tkinter as tk

import color as c


# Inheriting Game Class from tk.Frame
class Game(tk.Frame):
    # Class Constructor --> Creates a Game Window
    def __init__(self):
        # Calling the Constructor of tk.Frame 
        tk.Frame.__init__(self)
        # Putting Each element in a Grid
        # Hence Forth each element in Window will be put in a 2D Table
        self.grid()
        # Setting the window title
        self.master.title("2048")

        # Creating a Frame using tkinter Frame method
        # Setting the background-color, border, width and height of Frame
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=500, height=500)

        # Setting the frame layout to grid
        self.main_grid.grid(pady=(80, 0))

        # Make_GUI and StartGame
        self.make_GUI()
        self.start_game()

        # Binding the KeyDown events
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        # Window must display continously
        # Playing background Music

        pygame.mixer.init()
        pygame.mixer.music.load("Background.mp3")
        pygame.mixer.music.play()
        self.mainloop()

    # ---------------------- Function Definitions -------------------------------------------------------

    # make_GUI definition
    # This Function will construct the cells of main_grid, assign default data to the cells, create the 4 x 4 cell data matrix and create a Score Label
    def make_GUI(self):
        # Creating a 4 by 4 matrix (Cells of 2048 Game)
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                # Creating a Child Frame inside main_grid
                cell_frame = tk.Frame(
                    self.main_grid,  # Inherit the main grid (The cell is inside main_grid)
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100
                )
                # Setting the cells location inside main grid
                # Also Setting padding of cell
                cell_frame.grid(row=i, column=j, padx=5, pady=5)

                # Used to display the number value (This value will change once the game in Started)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)

                # The contents of cell
                cell_data = {"frame": cell_frame, "number": cell_number}
                # Insert the cell_data into the 4 x 4 matrix
                row.append(cell_data)
            # append that matrix into the cells
            self.cells.append(row)

            # Making the Score Header
        # Creating Score Frame inside MainWindow (self)
        score_frame = tk.Frame(self)
        # Placing the Score Frame
        score_frame.place(relx=0.5, x=100, y=40, anchor="center")
        # Creating "Score" Text Label Inside score_frame
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)

        # Creating Another Label to Display the Score (Inside Score Frame)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

        # Making the High Score Header
        # Creating High Score Frame inside MainWindow (self)
        high_score_frame = tk.Frame(self)
        # Placing the High Score Frame
        high_score_frame.place(relx=0.5, x=-100, y=40, anchor="center")
        # Creating "Score" Text Label Inside score_frame
        tk.Label(
            high_score_frame,
            text="Win Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)

        # Storing the Score into txt file with winning text
        with open(c.highScore, 'r') as file:
            highscore = 0
            hscore = file.readline()
            while (hscore != ''):
                if (hscore[0] != "0"):
                    zscore = int(hscore)
                    if (zscore > highscore):
                        highscore = zscore
                hscore = file.readline()

        # Creating Another Label to Display the High Score (Inside Score Frame)
        self.high_score_label = tk.Label(high_score_frame, text=highscore, font=c.HIGH_SCORE_FONT)
        self.high_score_label.grid(row=1)

    # Start Game Function
    # This function sets value of any two random cells to '2' so that we can start our game
    # Also it creates the logical matrix and sets the initial score to 0

    # !IMPORTANT
    # The LOGICAL MATRIX will be the matrix which will be modified and based on which our GUI will chnage
    # I.e. it is the Core part of our Game Logic

    def start_game(self):
        # Create matrix of zeroes (4 x 4 matrix)
        self.matrix = [[0] * 4 for _ in range(4)]

        # Fill 2 random cells with 2s
        # Randomly selecting the row and column from the list [0,1,2,3]
        row = random.randint(0, 3)
        col = random.randint(0, 3)

        # Placing the first '2' in random place in matrix
        self.matrix[row][col] = 2
        # Adding the first '2' into the GUI
        # Configuring the cell color
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        # Configuring the content,color,font and background
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")

        # Here we first check for an empty cell and then we add the second "2"
        # (This will prevent the first and second '2' gettinb the same position)
        while (self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)

        # Placing the first '2' in random place in matrix
        self.matrix[row][col] = 2
        # Adding the second '2' into the GUI
        # Configuring the cell color
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        # Configuring the content,color,font and background
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")

        # Setting the initial score to 0
        self.score = 0

    # Matrix Manipulation Functions

    # This function will compress the non zero numbers into the one side of the board or matrix
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]  # The Zero Matrix
        # Pushing all the elements to one side of the board
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        # Setting the new matrix as self.matrix
        # Note that no data is lost in this operation
        self.matrix = new_matrix

    # Combine Function
    # This function will fuse two adjacent cells with same value
    # By fuse, we mean that it will simply add the data of two cells and make a new cell from the two cells.
    # It will also increment the Score by value of newly created fused cell
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    # Reverse Function
    # This function will reverse every row of matrix
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                # Reverse the Order
                new_matrix[i].append(self.matrix[i][3 - j])

        # Setting the new matrix as self.matrix
        self.matrix = new_matrix

    # Tranpose Function
    # This Function will transpose the existing matrix
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]

        # Setting the new matrix as self.matrix
        self.matrix = new_matrix

    # add_new_tile Function
    # This function wiil add a new 2 or 4 tile randomly to an empty cell
    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            # Randomly Searching for an empty cell
            while (self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            # Assigning the value 2 or 4 at that random cell
            self.matrix[row][col] = random.choice([2 ** i for i in range(1, 10)])

            # Update GUI function

    # Update the GUI to match the logical matrix
    def update_GUI(self):
        # Iterating over each and every element of the logical matrix
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                # If cell_value is 0 --> Add the GUI of an empty cell
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR, text="")

                # Else --> Add the GUI of respective value cell
                else:
                    # giving the background according to the cell value
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLORS[cell_value])
                    # giving the foreground according to the cell value
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))

        # Updating the Score Label in GUI
        self.score_label.configure(text=self.score)
        # Updating the MainWindow GUI
        self.update_idletasks()

    # Arrow-Press Functions (KeyDown Events)

    # Left KeyDown Event
    def left(self, event):
        self.stack()  # to compress the non zero number into the left size
        self.combine()  # to combine the horizontal same cell into the one
        self.stack()  # to eliminate the newly created zero value cell
        self.add_new_tile()  # To add a new tile to Window
        self.update_GUI()  # To update the GUI accordingly
        self.game_over()  # To check is Game is Over

    # Right KeyDown Event
    def right(self, event):
        # Compress in Right Direction
        self.reverse()
        self.stack()

        self.combine()  # Combine Tiles
        self.stack()  # Eliminate zere valued cells
        self.reverse()  # Restore the original order of matrix
        self.add_new_tile()  # Add a new tile
        self.update_GUI()  # Update GUI
        self.game_over()  # To check is Game is Over

    # Up KeyDown Event
    def up(self, event):
        # Compress in Up direction
        self.transpose()
        self.stack()

        self.combine()  # Combine Tiles
        self.stack()  # Eliminate zere valued cells
        self.transpose()  # Restore the original order of matrix
        self.add_new_tile()  # Add a new tile
        self.update_GUI()  # Update GUI
        self.game_over()  # To check is Game is Over

    # Down KeyDown Event
    def down(self, event):
        # Compress in Down Direction
        self.transpose()
        self.reverse()
        self.stack()

        self.combine()  # Combine Tiles
        self.stack()  # Eliminate zere valued cells

        # Restore the original order of matrix
        self.reverse()
        self.transpose()

        self.add_new_tile()  # Add a new tile
        self.update_GUI()  # Update GUI
        self.game_over()  # To check is Game is Over

    # Functions to Check if any moves are possible

    # Check whether horizontal move exists
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    # Check whether vertical move exists
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # Check if Game is Over (Win/Lose)

    def game_over(self):
        # Check any 2048 in row if yes display YOU WIN
        if any(2048 in row for row in self.matrix):
            # Creating a GameOver Frame
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            # Placing the GameOver Frame
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            # Creating and Rendering the Label inside Game Over Frame
            # .pack() will render the label in GUI
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()

            # Storing the Score into txt file with winning text
            with open(c.highScore, 'a') as file:
                file.write(str(self.score))
                file.write("\n")

        # Else if no move exist --> Show Game Over
        elif not any(0 in row for row in
                     self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            # Creating a GameOver Frame
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            # Placing the GameOver Frame
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            # Creating and Rendering the Label inside Game Over Frame
            # .pack() will render the label in GUI
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
            # Storing the Score into txt file
            with open(c.highScore, 'a') as file:
                file.write("0")
                file.write(str(self.score))
                file.write("\n")


# Driver Code
def main():
    Game()


# Running the Game
if __name__ == "__main__":
    main()