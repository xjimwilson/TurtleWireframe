import shared
print("importer OK!")

def readandextract(filename):
    draw = []
    with open(f"importedmodels/{filename}", "r") as f:
        for line in f:
            line = line.replace(" ","")
            if not line or line.startswith('.'):
                continue
            if line.startswith("linesize"):
                shared.linesize = int(line[9:])
                if type(shared.linesize) == str:
                    print(f"ERROR: line {line}, Linesize given as string (should be value)")
                shared.linetype = "size"
            else:
                values = [float(p) for p in line.split(",") if p.strip()]
                if len(values) == 4:
                    draw.append(tuple(values))
                    shared.linetype = "draw"
    return draw

