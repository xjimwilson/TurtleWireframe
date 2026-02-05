#SETUP---------------------------------------------------------------------------------------------
from RENDEREQUATION import calculate
from bad3dreader import readandextract
import turtle as t
import keyboard as kb
import shared

screen = t.Screen()
screen.tracer(0)
t.hideturtle()

rotx, roty = 30, 30
xoffset, yoffset, zoffset = 0, 0, 0
speed = 0.6
zoom = 3.5
pennormalizescale = 0.6

showgrid = True
showaxis = False
keylifted = True

print("render init OK!")

#SETUP---------------------------------------------------------------------------------------------
def calculaterender(x,y,z,xrot,yrot,draw):

    zx, zy, zz = x * zoom, y * zoom, z * zoom

    if draw == 1:
        t.pendown()
    else:
        t.penup()

    pos = calculate(zx,zy,zz,xrot,yrot)
    t.goto(pos[0], pos[1])
    t.penup()

def control():
    global rotx, roty, speed, zoom, showgrid

    #rotationmouse
    


    #rotationkeyboard
    if kb.is_pressed("up"):
        rotx -= speed
    if kb.is_pressed("down"):
        rotx += speed
    if kb.is_pressed("right"):
        roty -= speed
    if kb.is_pressed("left"):
        roty += speed


    #zoom
    if kb.is_pressed("i"):
        if zoom < 20:
            zoom *= 1.01 
    if kb.is_pressed("o"):
        if zoom > 0.5:
            zoom /= 1.01 


    #speed
    if kb.is_pressed("-"):
        if speed > 0.1:
            speed /= 1.01
    if kb.is_pressed("="):
        if speed < 5:
            speed *= 1.01

    #grid
    if kb.is_pressed("g"):
        showgrid = True
    if kb.is_pressed("h"):
        showgrid = False

    #axis
    if kb.is_pressed("a") and keylifted == True:
        showaxis = True
        keylifted = False
    if not kb.is_pressed("a"):
        keylifted = True
        showaxis = False
    
def pensizescaled(size):
    t.pensize(size*pennormalizescale*zoom)

def render():

    t.clear()

    drawgrid() # draw grid before import so depth is correct
    drawimport()

    screen.update()

def drawimport():
    commands = readandextract(shared.filename) #reads the .bad3d file
    # commands is a list of ("size", int) or ("draw", (x,y,z,drawflag))

    pensizescaled(1)
    t.color("gray10")

    for cmd in commands:
        if cmd[0] == "size":
            pensizescaled(cmd[1])
        elif cmd[0] == "draw":
            x, y, z, d = cmd[1]
            calculaterender(x, y, z, rotx, roty, d)

def drawgrid():
    if showgrid == True:
        

        if zoom > 5:
            commands = readandextract("floorgrid/floorgridsmall.bad3d")
        elif zoom > 2:
            commands = readandextract("floorgrid/floorgridnormal.bad3d")
        else:
            commands = readandextract("floorgrid/floorgridlarge.bad3d")

        t.pensize(1)

        for cmd in commands:
            if cmd[0] == "draw":
                x, y, z, d = cmd[1]
                t.color("lightgrey")
                calculaterender(x, y, z, rotx, roty, d)


def drawaxis():
    pensizescaled(2)
    # X axis
    t.color("red")
    calculaterender(0,0,0,rotx,roty,0)
    calculaterender(100,0,0,rotx,roty,1)
    t.penup()
    pos = calculate(110, 0, 0, rotx, roty)
    t.goto(pos[0], pos[1])
    t.pendown()

    # Y axis
    t.color("green")
    calculaterender(0,0,0,rotx,roty,0)
    calculaterender(0,100,0,rotx,roty,1)
    t.penup()
    pos = calculate(0, 110, 0, rotx, roty)
    t.goto(pos[0], pos[1])
    t.pendown()

    # Z axis
    t.color("blue")
    calculaterender(0,0,0,rotx,roty,0)
    calculaterender(0,0,100,rotx,roty,1)
    t.penup()
    pos = calculate(0, 0, 110, rotx, roty)
    t.goto(pos[0], pos[1])
    t.pendown()

    t.color("black") 
    
#INPUTS--------------------------------------------------------------------------------------------
