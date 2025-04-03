# For the LOKI 2015 images, removes the white area and scale bar
from PIL import Image, ImageOps
import os

# Define the directory containing black and white images
input_dir = r"C:\Users\patri\python_workspace\loki2015\data\images_processed_with_scale"
output_dir = r"C:\Users\patri\python_workspace\loki2015\data\images_processed"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        # Open the image
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)

        # Invert the colors of the image
        # inverted_img = ImageOps.invert(img)

        # Keep colors of the image
        inverted_img = img

        width, height = inverted_img.size
        
        # # Remove the lower 30 pixels of the image (the size scale text)
        # cropped_img = inverted_img.crop((0, 0, width, height - 30))

        # Set the bottom 33 pixels to black
        for y in range(height - 33, height):
            for x in range(width):
                inverted_img.putpixel((x, y), (0, 0, 0))

        # Save the inverted image to the output directory
        output_path = os.path.join(output_dir, filename)
        # cropped_img.save(output_path)
        inverted_img.save(output_path)

print(f"All images have been inverted and saved to {output_dir}")