import turtle

s = turtle.getscreen()

snake = turtle.Turtle()
food1 = turtle.Turtle()

snake.shape("square")
food1.shape("square")
snake.penup()
food1.penup()
food1.goto(100,-100)

while True:
    
    snake.forward(3)
    

    def up():
        snake.setheading(90)

    def down():
        snake.setheading(270)

    def left():
        snake.setheading(180)

    def right():
        snake.setheading(0)

    turtle.listen()

    turtle.onkey(up , "Up")
    turtle.onkey(down , "Down")
    turtle.onkey(left , "Left")
    turtle.onkey(right , "Right")
    
    food1_pos = food1.pos()
    snake_pos = snake.pos()
    
    if food1_pos == snake_pos:
        
        snake.pendown()
        snake.forward(1)
        snake.penup()
       


turtle.mainloop()