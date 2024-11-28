import colorsys
import json5 as json
from sklearn.decomposition import PCA
import numpy as np
import math

canvassize = 2048
margin = 50

# List of named colors and their hex values
with open('../colors_taleofp.json', 'r') as file:#colors_gwofficial colors_taleofp
    color_dict = json.load(file)

# Function to convert hex to RGB
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# Function to convert RGB to HSL (in HLS order)
def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    hls = colorsys.rgb_to_hls(r, g, b)
    return (hls[0], hls[2], hls[1])

# Function to convert RGB to CMYK
def rgb_to_cmyk(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k < 1:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    else:
        c = m = y = 0
    return (c, m, y, k)

def quantize_hue(hue, step=0.1):
    return (hue // step) * step


def relax_points(points, min_distance=0.1, iterations=100):
    # Copy the points to avoid modifying the original list
    relaxed_points = points.copy()
    move_factor = 0.2
    
    for _ in range(iterations):
        for i in range(len(relaxed_points)):
            for j in range(i + 1, len(relaxed_points)):
                # Calculate the distance between point i and point j
                x1, y1 = relaxed_points[i]
                x2, y2 = relaxed_points[j]
                distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                
                # If the distance is less than the minimum distance, apply a repulsion force
                if distance < min_distance and distance > 0:
                    '''
                    # Calculate the repulsion factor
                    repulsion = (min_distance - distance) / min_distance
                    # Move points away from each other based on the repulsion
                    dx, dy = (x2 - x1), (y2 - y1)
                    angle = np.arctan2(dy, dx)

                    # Adjust the positions of the points
                    relaxed_points[i] = (x1 - repulsion * np.cos(angle), y1 - repulsion * np.sin(angle))
                    relaxed_points[j] = (x2 + repulsion * np.cos(angle), y2 + repulsion * np.sin(angle))
                    '''
                    factor = (min_distance-distance)/2 * move_factor
                    dx, dy = (x2 - x1)/distance*factor, (y2 - y1)/distance*factor
                    relaxed_points[i] = (x1 - dx, y1 - dy)
                    relaxed_points[j] = (x2 + dx, y2 + dy)

    return relaxed_points

def normalize_points(points):
    min_x, max_x = np.min(points[:, 0]), np.max(points[:, 0])
    min_y, max_y = np.min(points[:, 1]), np.max(points[:, 1])

    ans = np.array([[(x - min_x) / (max_x - min_x), (y - min_y) / (max_y - min_y)] for x, y in points])
    return ans

def lerp(a, b, t):
    return a + (b-a)*t

def sigmoid(x, p):
    return (x**p)/(x**p + (1-x)**p)

# Sort the color list by Hue (H)
#sorted_colors = sorted(color_dict.items(), key=lambda x: (quantize_hue(rgb_to_hsl(hex_to_rgb(x[1]))[0]), rgb_to_hsl(hex_to_rgb(x[1]))[2]))

mode = 'WHEEL' # PCA

def hsl_to_wheel(hsl):
    h, s, l = hsl
    a = math.radians(h*360)
    d = lerp(l, 0.65, s)
    d = sigmoid(d, 2)
    x = canvassize/2 + math.cos(a) * (canvassize/2-margin)*d
    y = canvassize/2 + math.sin(a) * (canvassize/2-margin)*d
    return x,y

# run PCA
hsl_colors = {}
for name, hex_code in color_dict.items():
    rgb = hex_to_rgb(hex_code)
    h, s, l = rgb_to_hsl(rgb)
    hsl_colors[name] = h, s, l

if mode == 'PCA':
    hsl_values = np.array(list(hsl_colors.values()))

    # Apply PCA to reduce from 3D (HSV) to 2D
    pca = PCA(n_components=2)
    points = pca.fit_transform(hsl_values)

    # transform points
    points = normalize_points(points)
    points = relax_points(points, min_distance=0.05)
    points = normalize_points(points)

elif mode == 'WHEEL':
    hsl_values = np.array(list(hsl_colors.values()))
    points = [ hsl_to_wheel(hsl) for hsl in hsl_values ]
    points = relax_points(points, min_distance = 90)

name_to_points = {name: (points[i][0], points[i][1]) for i, name in enumerate(hsl_colors.keys())}

for name, hex_code in color_dict.items(): # sorted_colors:
    rgb = hex_to_rgb(hex_code)
    h, s, l = rgb_to_hsl(rgb)
    #c, m, y, k = rgb_to_cmyk(rgb)
    #print(f'drawCircle("{hex_code}", {canvassize*l:.2f}, {canvassize*h:.2f}, "{name}");')
    
    #if s >= 0.5:
        #continue

    if mode == 'PCA':
        x, y = name_to_points[name]
        print(f'    ["{hex_code}", {margin + (canvassize-margin*2)*x:.2f}, {margin + (canvassize-margin*2)*y:.2f}, "{name}"],')
    elif mode == 'WHEEL':
        x, y = name_to_points[name]
        print(f'    ["{hex_code}", {x:.2f}, {y:.2f}, "{name}"],')
