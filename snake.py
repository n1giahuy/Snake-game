# Import necessary modules from tkinter for GUI and random for generating random positions for food
from tkinter import *
import random

# Define constants for the game
GAME_WIDTH = 1000          # Width of the game window
GAME_HEIGHT = 500          # Height of the game window
SPEED = 70                 # Speed of the game, in milliseconds
SPACE_SIZE = 50            # Size of each grid space
BODY_PARTS = 3             # Initial number of body parts in the snake
SNAKE_COLOR = "#00FF00"    # Color of the snake
FOOD_COLOR = "#FF0000"     # Color of the food
BACKGROUND_COLOR = "#000000"  # Background color of the game window

# Define the Snake class to handle the snake's properties and behavior
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []  # List to store the coordinates of the snake's body
        self.squares = []      # List to store the graphical representation of the snake's body

        # Initialize the snake's body at the starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create the squares representing the snake's body on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Define the Food class to handle the food's properties and behavior
class Food:
    def __init__(self):
        # Generate a random position for the food within the game boundaries
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Create the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Function to handle the next turn of the game, including movement and collision detection
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    # Update the position of the snake's head based on the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert the new head position at the beginning of the snake's coordinates
    snake.coordinates.insert(0, (x, y))

    # Create the new square for the snake's head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()  # Create new food
    else:
        # If the snake didn't eat food, remove the last part of the snake's body
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collision
    if check_collision(snake):
        game_over()  # End the game if there is a collision
    else:
        window.after(SPEED, next_turn, snake, food)  # Schedule the next turn

# Function to change the direction of the snake based on user input
def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != 'right':
        direction = new_direction
    elif new_direction == "right" and direction != 'left':
        direction = new_direction
    elif new_direction == "up" and direction != 'down':
        direction = new_direction
    elif new_direction == "down" and direction != 'up':
        direction = new_direction

# Function to check for collisions with the wall or the snake's own body
def check_collision(snake):
    x, y = snake.coordinates[0]

    # Check if the snake hits the wall
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# Function to handle game over scenario
def game_over():
    canvas.delete(ALL)  # Clear the canvas
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Initialize the main window for the game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initialize the game variables
score = 0
direction = 'down'

# Create and place the score label at the top of the window
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create the canvas where the game will be played
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Update the window to get correct dimensions for centering
window.update()

# Center the game window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind the arrow keys to change the snake's direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create the initial snake and food objects
snake = Snake()
food = Food()

# Start the game loop by calling next_turn
next_turn(snake, food)

# Run the Tkinter main loop
window.mainloop()
