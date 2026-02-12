#SETUP---------------------------------------------------------------------------------------------
from re import L
from RENDEREQUATION import calculate
from bad3dreader import readandextract
import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import keyboard as kb
import shared, preferences
from platform import system

rotx, roty = 30.0, 30.0
xoffset, yoffset, zoffset = 0, 0, 0
dy, dx = 30,30
speed = 0.6
zoom = 3.0
pennormalizescale = 0.6

showgrid = True
showaxis = False
akeylifted = True
pkeylifted = True

print("render init OK!")

def initTurtleCanvas():
    global canvas, root, screen, t

    root = tk.Tk()
    
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()
    
    root.title("Render")
    
    screen = TurtleScreen(canvas)
    t = RawTurtle(screen)
    screen.tracer(0)
    t.hideturtle()

    print("canvas init OK!")
    
def updatewindowsize():
    global canvas, screen, t, root
    root.geometry(f"{preferences.mainwindowsizex}x{preferences.mainwindowsizey}")
    root.maxsize(preferences.mainwindowsizex, preferences.mainwindowsizey)
    root.minsize(preferences.mainwindowsizex, preferences.mainwindowsizey)

    try:
        canvas.destroy()
    except NameError:
        pass

    canvas = tk.Canvas(root, width=preferences.mainwindowsizex, height=preferences.mainwindowsizey)
    canvas.pack()

    screen = TurtleScreen(canvas)
    t = RawTurtle(screen)
    screen.tracer(0)
    t.hideturtle()
    initmousebind()

def initmousebind():
    def on_click_tk(event):
        # event.x / event.y are canvas coords
        global startx, starty
        startx, starty = event.x, event.y

    def on_drag_tk(event):
        global startx, starty, dx, dy
        # calculate displacement relative to last press/previous drag
        dx += (event.x - (startx or 0)) * speed
        dy += (event.y - (starty or 0)) * speed

        startx, starty = event.x, event.y


    canvas.bind("<Button-1>", on_click_tk)
    canvas.bind("<B1-Motion>", on_drag_tk)


def showpopup(type):
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)

    root.update_idletasks() #speeds up all the tasks so we get good values (read it on a website)

    rootx = root.winfo_rootx()
    rooty = root.winfo_rooty()
    rootw = int(preferences.mainwindowsizex)
    rooth = int(preferences.mainwindowsizey)

    x = rootx + max(0, (rootw - 250) // 2)
    y = rooty + rooth - 75

    overlay.geometry(f"{250}x{75}+{int(x)}+{int(y)}")

    if type == "zoom":
        message = f"Zoom: {zoom:.2f}"
    elif type == "resetview":
        message = "Successfully Reset Camera"
    else:
        message = str(type) #js prints out whatever was inputted

    msg = tk.Message(overlay, text=message, width=250 - 20)
    msg.pack(expand=True, fill="both", padx=10, pady=10)
    overlay.after(2000, overlay.destroy)


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

def resetview():
    global zoom,rotx,roty,dx,dy,xoffset,yoffset,zoffset

    rotx, roty = 30.0, 30.0
    dx,dy = 30.0, 30.0
    xoffset, yoffset, zoffset = 0, 0, 0
    zoom = 3

    showpopup("resetview")

def control():
    global rotx, roty, speed, zoom, showgrid, akeylifted, pkeylifted, showaxis

    if dy or dx > 0:
        rotx = dy * speed
        roty = dx * speed
        
    #preferences window toggle
    if kb.is_pressed("p") and pkeylifted == True:
        pkeylifted = False

        #alr so if the window cant be referenced then we gotta assume it doesnt even exist
        try:
            if preferences.checkwindowexists() == True:
                preferences.closewindow()
            else:
                preferences.initpref(root) #if it's been initialised already, we can call checkwindowexists
        except:   
            preferences.initpref(root) #when it doesnt exist we initialise

    if not kb.is_pressed("p"):
        pkeylifted = True

    #zoom
    if kb.is_pressed("i"):
        if zoom < 20:
            zoom *= 1.01 
        showpopup("zoom")
    if kb.is_pressed("o"):
        if zoom > 0.5:
            zoom /= 1.01
        showpopup("zoom")
    
    
def pensizescaled(size):
    t.pensize(size*pennormalizescale*zoom)

def render():
    t.clear()

    drawgrid() # draw grid before import so depth is correct
    drawimport()
    drawaxis()

    screen.update()

def drawimport():
    commands = readandextract(shared.filename) #reads the .bad3d file
    # commands is a list of ("size", int) or ("draw", (x,y,z,drawflag))

    pensizescaled(1)
    t.color("black")

    for cmd in commands:
        if cmd[0] == "size":
            pensizescaled(cmd[1])
        elif cmd[0] == "draw":
            x, y, z, d = cmd[1]
            calculaterender(x, y, z, rotx, roty, d)

def drawgrid():
    if preferences.gridlines == True:
        if preferences.lod == True:
            if zoom > 5:
                commands = readandextract("floorgrid/floorgridsmall.bad3d")
            elif zoom > 2:
                commands = readandextract("floorgrid/floorgridnormal.bad3d")
            elif zoom > 0.8:
                commands = readandextract("floorgrid/floorgridlarge.bad3d")
            else:
                commands = readandextract("floorgrid/floorgridhuge.bad3d")
        else:
            commands = readandextract("floorgrid/floorgridhuge.bad3d")

        t.pensize(1)

        for cmd in commands:
            if cmd[0] == "draw":
                x, y, z, d = cmd[1]
                t.color("lightgrey")
                calculaterender(x, y, z, rotx, roty, d)

def drawaxis():
    if preferences.axis == True:
        pensizescaled(3)
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