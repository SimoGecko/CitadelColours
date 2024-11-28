import cv2
import pytesseract
import numpy as np

# Path to Tesseract-OCR installation (adjust for your system)
pytesseract.pytesseract.tesseract_cmd = 'c:/Program Files/Tesseract-OCR/tesseract.exe'

# User-provided parameters
image_path = 'c:/Users/Simone/Desktop/warhammer/PAINT/taleofpainters/Citadel_Colour_V2.0/Citadel_Colour_swatch_main_V2.0_uncompressed.png'  # Replace with your image file path

offset_x = 60
offset_y = 290
swatch_size = 280  # Width of a single swatch
swatch_subsize = 185
#swatch_height = 185#280  # Height of a single swatch
swatch_margin = 5
stride_x = 330  # Horizontal distance between swatch centers 3632/11
stride_y = 401  # Vertical distance between swatch centers 3606/9
grid_rows = 11  # Number of swatch rows
grid_cols = 12  # Number of swatch columns
text_height = stride_y-swatch_size
#241 217 133

def extract_swatches_from_grid(image_path, swatch_size, stride_x, stride_y, grid_rows, grid_cols):
    # Load the image
    image = cv2.imread(image_path)

    # Create a copy of the original image to modify
    output_image = image.copy()

    results = []
    
    for row in range(grid_rows):
        for col in range(grid_cols):
            # Calculate coordinates of the swatch area
            x = offset_x + col * stride_x
            y = offset_y + row * stride_y
            
            # Extract swatch and associated text regions
            x1, y1 = x + swatch_margin, y+swatch_margin
            swatch_region = image[y1:y1+swatch_subsize, x1:x1+swatch_subsize]
            text_region = image[y+swatch_size:y+swatch_size+text_height, x:x+swatch_size]  # Assume 30px text height below swatch

            # Calculate average color of the swatch
            avg_color = cv2.mean(swatch_region)[:3]
            avg_color = tuple(map(int, avg_color))  # Convert to integer RGB values
            avg_color_rgb = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_BGR2RGB)[0][0]
            avg_color_hex = '#{:02x}{:02x}{:02x}'.format(*avg_color_rgb)

            # Overwrite swatch area with the average color
            cv2.rectangle(output_image, (x1, y1), (x1+swatch_subsize, y1+swatch_subsize), avg_color, -1)

            # Extract text from the text region
            text = pytesseract.image_to_string(text_region, config='--psm 6').strip()
            text = text.replace('\n', ' ').replace('  ', ' ')

            # Store results
            results.append((text, avg_color_rgb, avg_color_hex))

    cv2.imwrite('output_image.png', output_image)
    return results


# Extract swatches
swatches = extract_swatches_from_grid(image_path, swatch_size, stride_x, stride_y, grid_rows, grid_cols)

# Print results
for name, a_rgb, a_hex in swatches:
    #print(f"Name: {name}, RGB: {avg_color}, Hex: {avg_color_hex}")
    print(f'{name:<40} {a_rgb}\t{a_hex}')
