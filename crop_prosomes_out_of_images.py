# Script to crop out the sections of the image files that are not inside the prosome. This will be useful in retraining the lipid segmentation model on the prosome-only sections.

import os
from PIL import Image
import numpy as np

def apply_mask_to_all(image_dir, mask_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in the image directory
    for filename in os.listdir(mask_dir):
        image_path = os.path.join(image_dir, filename)
        mask_path = os.path.join(mask_dir, filename)

        # Check if corresponding mask file exists
        if os.path.isfile(image_path) and os.path.isfile(mask_path):
            # Load image and mask
            image = Image.open(image_path).convert("RGB")
            mask = Image.open(mask_path).convert("L")

            # Convert images to numpy arrays
            image_np = np.array(image)
            mask_np = np.array(mask)

            # Set all pixels outside the mask to zero in the image
            image_np[mask_np == 0] = [0, 0, 0]

            # Convert back to image and save the result in the output directory
            processed_image = Image.fromarray(image_np)
            output_path = os.path.join(output_dir, filename)
            processed_image.save(output_path)
            print(f"Processed and saved: {output_path}")

# # For UVP6 Darkedge
# apply_mask_to_all(r"C:\Users\patri\python_workspace\uvp6_939_images\images_with_prosome", r"C:\Users\patri\python_workspace\uvp6_939_images\prosome", r"C:\Users\patri\python_workspace\uvp6_939_images\images_of_cropped_prosome")

# For UVP6 Amundsen 2023 part 1
apply_mask_to_all(r"C:\Users\patri\python_workspace\uvp6_amundsen2023_part1\images_with_prosome", 
                  r"C:\Users\patri\python_workspace\uvp6_amundsen2023_part1\Prosome", 
                  r"C:\Users\patri\python_workspace\uvp6_amundsen2023_part1\images_of_cropped_prosome")
