import turtle
def draw_star(size, color):
    angle = 120
    turtle.fillcolor(color)
    turtle.begin_fill()

    for side in range(6):
        turtle.forward(size)
        turtle.right(angle)
        turtle.forward(size)
        turtle.right(60 - angle)

    return
if __name__ == "__main__":
    draw_star(100, "purple")

