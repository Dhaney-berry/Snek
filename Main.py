from tkinter import *
import random

# Constants
GAME_WIDTH = 900
GAME_HEIGHT = 700
SPEED = 50
SPACE = 40
BODY_PARTS = 5
SNAKESKIN = "olive drab"
FOOD_COLOR = "blanched almond"
BACKDROP = "DarkGoldenrod3"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:

            square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKESKIN)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH/SPACE)-1) * SPACE
        y = random.randint(0, int(GAME_HEIGHT/SPACE)-1) * SPACE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE, y + SPACE, fill=FOOD_COLOR)


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE
    elif direction == "left":
        x -= SPACE
    elif direction == "down":
        y += SPACE
    elif direction == "right":
        x += SPACE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKESKIN)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 2
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Set Boundaries
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

    window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font="consolas, 50", text=f"GAME OVER\nScore:{score}",
                       fill="white")


window = Tk()
window.title("Sneaky Snek")
window.resizable(False, False)
# Set Score Label
score = 0
direction = 'down'
label = Label(window, text="Score:{}".format(score), font=("consolas", 30))
label.pack()

# Create Canvas
canvas = Canvas(window, bg=BACKDROP, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Adjust position of window
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind keys
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
