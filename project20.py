import turtle
import time
import random

# Define the file for storing the high score
high_score_file = "data.txt"

# Function to read the high score from a file
def read_high_score():
    try:
        with open(high_score_file, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to save the high score to a file
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Initial settings
delay = 0.1
score = 0
high_score = read_high_score()

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.shapesize(0.5, 0.5)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.shapesize(0.5, 0.5)
food.penup()
food.goto(0, 100)

segments = []

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("yellow")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)
scoreboard.write(f"Score: 0  High Score: {high_score}", align="center", font=("Times New Roman", 12, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 10)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 10)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 10)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 10)

def update_score():
    global score, high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    scoreboard.clear()
    scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Times New Roman", 12, "normal"))

# Keyboard bindings
wn.listen()
wn.onkey(go_up, "w")
wn.onkey(go_down, "s")
wn.onkey(go_left, "a")
wn.onkey(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the segments of the body
        for segment in segments:
            segment.goto(1000, 1000)  # Out of the screen

        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0
        update_score()

    # Check for collision with the food
    if head.distance(food) < 10:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.shapesize(0.5, 0.5)
        new_segment.penup()
        segments.append(new_segment)

        # Increase the score
        score += 1
        update_score()

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 10:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide the segments of the body
            for segment in segments:
                segment.goto(1000, 1000)  # Out of the screen

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0
            update_score()

    time.sleep(delay)

wn.mainloop()
