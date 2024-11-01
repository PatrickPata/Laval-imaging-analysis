# Convert prosome mask png files [0 255] to bmp files [0 1] for the appsilon model
import os
from PIL import Image
import numpy as np

# Define the directory containing the .png files
input_directory = r"C:\Users\patri\python_workspace\data\segmentations_prosome"
output_directory = r"C:\Users\patri\python_workspace\data\prosome\segmentations_processed"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.png'):
        try:
            # Open the image file
            img_path = os.path.join(input_directory, filename)
            img = Image.open(img_path)

            # Convert the image to a numpy array and normalize values
            img_array = np.array(img) / 255.0

            # Scale back to 8-bit values (0–255) and convert to uint8
            img_array = img_array.astype(np.uint8)

            # Convert back to image format in mode 'L' (grayscale 8-bit)
            img_normalized = Image.fromarray(img_array, mode='L')

            # Update filename: remove "-Prosome_mask" and replace underscores with spaces
            new_filename = filename.replace('-Prosome_mask', '').replace('_', ' ').replace('.png', '.bmp')

            # Save the image as .bmp in the output directory
            output_path = os.path.join(output_directory, new_filename)
            img_normalized.save(output_path, 'BMP')

            print(f"Saved {new_filename} to {output_directory}")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print("Conversion complete.")


def check_write_permission(directory):
    try:
        # Try creating a temporary file in the specified directory
        test_file = os.path.join(directory, 'temp_permission_test.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        
        # If successful, delete the temporary file
        os.remove(test_file)
        print(f"Write permission verified for directory: {directory}")
        return True
    except Exception as e:
        print(f"No write permission for directory: {directory}. Error: {e}")
        return False

# Example usage
output_directory = r"C:\Users\patri\python_workspace\data\prosome\segmentations_processed"
check_write_permission(output_directory)




