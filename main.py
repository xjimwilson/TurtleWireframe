from render import initTurtleCanvas, initmousebind, render, control, initTurtleCanvas, initmousebind
import time
import shared

running = True

print("bootstrap init OK!")
time.sleep(0.1)# wait for everything to load

print("")
print("Enter filename of .bad3d file OR press enter to load demo")
filename = input()
if filename == "":
    print("demo importing...")
    shared.filename = "boxandarrow.bad3d" # demo file
elif "." in filename:
    if ".bad3d" not in filename:
        print("invalid filetype, must be .bad3d")
        input("Press enter to exit")
        exit()
    else:
        shared.filename = filename.replace(" ", "")        
else:
    shared.filename = filename.replace(" ", "") + ".bad3d"

print("import OK!")

initTurtleCanvas()
initmousebind()

print("render initalising...")
print("\n\nPress P to open preferences menu...")
while running:
    control()
    render()