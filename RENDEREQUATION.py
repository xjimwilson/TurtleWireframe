import math

print("renderequation init OK!")

def calculate(x, y, z, xrot, yrot):
    # Convert degrees to radians
    xr = math.radians(xrot)
    yr = math.radians(yrot)
    
    # Rotate around Y axis
    x1 = math.cos(yr) * x + math.sin(yr) * z
    z1 = -math.sin(yr) * x + math.cos(yr) * z
    
    # Rotate around X axis
    y1 = math.cos(xr) * y - math.sin(xr) * z1
    z2 = math.sin(xr) * y + math.cos(xr) * z1
    
    # Orthographic projection (ignore z2)
    X = x1
    Y = y1
    return X, Y
