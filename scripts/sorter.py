import colorsys
import json5 as json

# List of named colors and their hex values
with open('../colors_taleofp.json', 'r') as file:
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

# Sort the color list by Hue (H)
#sorted_colors = sorted(color_list, key=lambda x: rgb_to_hsl(hex_to_rgb(x[1]))[0])
#sorted_colors = sorted(color_dict.items(), key=lambda x: rgb_to_hsl(hex_to_rgb(x[1]))[0])
sorted_colors = sorted(color_dict.items(), key=lambda x: (quantize_hue(rgb_to_hsl(hex_to_rgb(x[1]))[0]), rgb_to_hsl(hex_to_rgb(x[1]))[2]))

# Open the file for writing the sorted colors
with open("output/sorted_colors.md", "w") as file:
    # HEX RGB HSL CMYK
    file.write('<style>\n.colorbox { width: 100px; height: 30px; border: 1px solid #000; }\n</style>\n\n')
    file.write('| Name | Color | HEX | RGB | HSL | CMYK |\n')
    file.write('| ---- | ----- | --- | --- | --- | ---- |\n')
    for name, hex_code in sorted_colors:
# Get RGB from HEX
        rgb = hex_to_rgb(hex_code)
        h, s, l = rgb_to_hsl(rgb)
        c, m, y, k = rgb_to_cmyk(rgb)
        rgb_str = f'rgb{rgb}'
        hsl_str = f'hsl({h*360:.0f}, {s*100:.0f}%, {l*100:.0f}%)' #°
        cmyk_str = f'cmyk({c*100:.0f}%, {m*100:.0f}%, {y*100:.0f}%, {k*100:.0f}%)'
        # Print the output in the desired format
        file.write(f'| {name} | <div class="colorbox" style="background:{hex_code};" /> | `{hex_code.upper()}` | `{rgb_str}` | `{hsl_str}` | `{cmyk_str}` |\n')

        #file.write(f"{name}: {hex_code}\n")
        #file.write(f'| {name} | <div class="color-box" style="background: {hex_code}"></div> | `{rgb_to_hsl(hex_to_rgb(hex_code))}` |\n')



# Display the sorted colors
#for name, hex_code in sorted_colors:
    #| Morghast Bone | <div style="background: #ba9f81; width: 100px; height: 25px;"></div> |
    #print(f"{name}: {hex_code}")