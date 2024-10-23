from PIL import Image, ImageOps
import os

# Define the directory containing black and white images
input_dir = r"C:\Laval_Postdoc\Laval-imaging-analysis\UVP5_greenedge\export_149_20241018_1551"
output_dir = r"C:\Laval_Postdoc\Laval-imaging-analysis\UVP5_greenedge\uvp5_inverted_images"

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
        inverted_img = ImageOps.invert(img)

        # Remove the lower 28 pixels of the image (the size scale text)
        width, height = inverted_img.size
        cropped_img = inverted_img.crop((0, 0, width, height - 30))

        # Save the inverted image to the output directory
        output_path = os.path.join(output_dir, filename)
        cropped_img.save(output_path)

print(f"All images have been inverted and saved to {output_dir}")