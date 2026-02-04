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
                shared.linetype = "size"
                print("found linesize")
                try:
                    shared.linesize = int((line[8:]).strip())
                    print(shared.linesize)
                except:
                    print("couldnt change linesize shared variable")
            else:
                values = [float(p) for p in line.split(",") if p.strip()]
                if len(values) == 4:
                    shared.linetype = "draw"
                    draw.append(tuple(values))
                    
    return draw

