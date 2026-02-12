import tkinter as tk
from tkinter import ttk
import render

pref = None

gridlines = True
axis = False
lod = True

windowsizex,windowsizey = 400, 400
mainwindowsizex, mainwindowsizey = 800, 600

def closewindow():
    pref.destroy()


def initpref(parent):
    global gridlines_var, gridlines, pref, axis_var, axis, lod_var, lod

    pref = tk.Toplevel(parent)

    pref.geometry(f"{windowsizex}x{windowsizey}")
    pref.maxsize(windowsizex, windowsizey)
    pref.minsize(windowsizex, windowsizey)

    pref.title("Preferences")
    pref.attributes('-topmost', True)
    pref.attributes('-toolwindow', True)

    tk.Label(pref, text="Show gridlines (Enabling impacts performance)").pack()

    gridlines_var = tk.BooleanVar(value=gridlines)
    gridlines = gridlines_var.get()

    def _on_grid_change(*args):
        global gridlines
        gridlines = gridlines_var.get()

    try:
        gridlines_var.trace_add("write", _on_grid_change)
    except AttributeError:
        gridlines_var.trace("w", _on_grid_change)

    tk.Radiobutton(pref, text="Enabled", variable=gridlines_var, value=True).pack(anchor=tk.CENTER)
    tk.Radiobutton(pref, text="Disabled", variable=gridlines_var, value=False).pack(anchor=tk.CENTER)


    tk.Label(pref, text="\nShow axis").pack()

    axis_var = tk.BooleanVar(value=axis)
    axis = axis_var.get()
    
    def _on_axis_change(*args):
        global axis
        axis = axis_var.get()

    try:
        axis_var.trace_add("write", _on_axis_change)
    except AttributeError:
        axis_var.trace("w", _on_axis_change)

    tk.Radiobutton(pref, text="Enabled", variable=axis_var, value=True).pack(anchor=tk.CENTER)
    tk.Radiobutton(pref, text="Disabled", variable=axis_var, value=False).pack(anchor=tk.CENTER)


    tk.Label(pref, text="\nEnable LOD (Disabling impacts performance)").pack()

    lod_var = tk.BooleanVar(value=lod)
    lod = lod_var.get()
    
    def _on_lod_change(*args):
        global lod
        lod = lod_var.get()

    try:
        lod_var.trace_add("write", _on_lod_change)
    except AttributeError:
        lod_var.trace("w", _on_lod_change)

    tk.Radiobutton(pref, text="Enabled", variable=lod_var, value=True).pack(anchor=tk.CENTER)
    tk.Radiobutton(pref, text="Disabled", variable=lod_var, value=False).pack(anchor=tk.CENTER)


    tk.Label(pref,text="\nWindow size:\n").pack()
    combo_box = ttk.Combobox(
        pref,
        values=["1920x1080", "1366x768", "1280x720", "800x600", "640x480", "500x500"],
        state="readonly"
    )

    combo_box.pack(pady=5)

    combo_box.set("800x600") # resolution on init

    def onsizeselect(event):
        global mainwindowsizex, mainwindowsizey

        resolutiontuple = str(event.widget.get()).replace("x"," ").split()
        mainwindowsizex = resolutiontuple[0]
        mainwindowsizey = resolutiontuple[1]

        render.updatewindowsize()

    combo_box.bind("<<ComboboxSelected>>", onsizeselect)

    tk.Label(pref, text="").pack()
    tk.Button(pref, text="Reset view", width=20, command=render.resetview).pack()

def checkwindowexists():
    if pref.winfo_exists():
        return True
    else:
        return False