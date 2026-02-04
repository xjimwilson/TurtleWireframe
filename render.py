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
zoom = 2.0
showgrid = True

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
        if zoom > 0.1:
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

    

def render():

    t.clear()

    drawimport()
    drawgrid()

    screen.update()

def drawimport():
    importedvals = readandextract(shared.filename) #reads the .bad3d file
    print(shared.linetype)
    if shared.linetype == "draw":
        for x, y, z, d in importedvals:
            calculaterender(x,y,z,rotx,roty,d)
    elif shared.linetype == "size":
        print("yea")
        t.pensize(shared.linesize)

def drawgrid():
    if showgrid == True:
        importedvals = readandextract("floorgrid.bad3d")
        for x, y, z, d in importedvals:
            t.color("lightgrey")
            calculaterender(x,y,z,rotx,roty,d)
            t.color("black")


def drawaxis():
    t.pensize(2)
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
    t.pensize(1)   

    
#INPUTS--------------------------------------------------------------------------------------------
