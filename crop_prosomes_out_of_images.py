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

# Example usage
apply_mask_to_all(r"C:\Users\patri\python_workspace\data\images_processed", r"C:\Users\patri\python_workspace\data\prosome\data\segmentations_processed", r"C:\Users\patri\python_workspace\data\cropped_prosome_annotation")

