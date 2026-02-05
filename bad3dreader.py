import shared
print("importer OK!")

def checkfileexists(filename):
    try:
        open(f"importedmodels/{filename}")
        passed = True
        
    except:
        print(f"File {filename} could not be opened (does it exist? is it in /importedmodels directory?)")
        passed = False

    return passed

def readandextract(filename):
    """
    Returns an ordered list of commands:
      - ("size", int)
      - ("draw", (x, y, z, drawflag))
    This preserves the file order so the renderer can process commands sequentially.
    """
    commands = []

    with open(f"importedmodels/{filename}", "r") as f:
        for line in f:
            # Normalize and skip comments / blank lines
            line = line.replace(" ", "").strip()
            if not line or line.startswith('.'):
                continue

            if line.startswith("linesize"):
                try:
                    currentlinesize = int(line[len("linesize"):].strip())
                    commands.append(("size", currentlinesize))
                except Exception:
                    print("couldnt get currentlinesize")
            else:
                # parse draw tuple: x,y,z,draw
                parts = [p for p in line.split(",") if p.strip()]
                try:
                    currentvalues = [float(p) for p in parts]
                except Exception:
                    # skip malformed line
                    continue

                if len(currentvalues) == 4:
                    commands.append(("draw", tuple(currentvalues)))

    return commands

