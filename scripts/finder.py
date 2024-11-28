import json
import math
import re
import json5 as json # more robust json parser. supports comments and trailing commas

# Convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Parse an RGB string like rgb(r, g, b)
def parse_rgb(rgb_string):
    match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', rgb_string)
    if match:
        return tuple(map(int, match.groups()))
    raise ValueError(f"Invalid RGB format: {rgb_string}")

# Calculate Euclidean distance between two RGB colors
def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def parse_color(color):
    # Parse the input color if it's in hex or rgb format
    if isinstance(color, str):
        if color.startswith('#'):
            return hex_to_rgb(color)
        elif color.startswith('rgb'):
            return parse_rgb(color)
        else:
            return hex_to_rgb(color)
            #raise ValueError("Invalid color format")
    return None

# Find the closest color name
def closest_color_name(color, named_colors_rgb):
    # Find the closest color by Euclidean distance
    closest_color = min(named_colors_rgb, key=lambda name: color_distance(named_colors_rgb[name], color))
    return closest_color

if __name__ == "__main__":
    # Load colors from JSON file
    with open('colors_taleofp.json', 'r') as file:
        colors_dict = json.load(file)

    # Convert named colors to RGB format
    named_colors_rgb = {}
    for name, value in colors_dict.items():
        named_colors_rgb[name] = parse_color(value)

    print("Enter a color (in hex or rgb format) or 'q' to quit: ")
    while True:
        # Ask user for input color
        user_input = input("> ").strip()

        if user_input.lower() == 'q':
            break

        try:
            input_color = parse_color(user_input)
            closest_name = closest_color_name(input_color, named_colors_rgb)
            distance = color_distance(named_colors_rgb[closest_name], input_color)
            print(f"Closest color: {closest_name} (distance={distance:.2f})\n")
        except ValueError as e:
            print(f"Error: {e}")