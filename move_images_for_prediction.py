# This is the script for moving the copepod images that were not segmented to a folder of imags for prediction
# Note that the reference folder is the folder with segmentation masks, and thus excluded.

import os
import shutil


## The code below copies all image files that have lipid/prosome masks to a separate folder for the segmentation runs

def move_different_files(source_folder, destination_folder, reference_folder):
    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the list of file names from the reference folder
    reference_filenames = set(os.listdir(reference_folder))

    # Walk through all subdirectories of the source folder
    for root, _, files in os.walk(source_folder):
        for filename in files:
            source_path = os.path.join(root, filename)

            # Check if the filename is in the reference list
            if filename not in reference_filenames:
                destination_path = os.path.join(destination_folder, filename)
                
                # Move the file to the destination folder
                shutil.copy(source_path, destination_path)
                print(f"Copied: {filename} from {source_path}")

# Example usage
# source_folder = r"C:\Users\patri\python_workspace\uvp6_darkedge_939_images\images_with_prosome" # UVP6 DE images with no lipid segmented
# source_folder = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_amundsen2023\Calanus\100\processed" # UVP6 Amund 2023 part 1 that were not segmented
# source_folder = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_amundsen2023\Calanus\100\images for prediction" # UVP6 Amundsen 2023 part2, all not segmented or processed
source_folder = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\export_5108_20250311_1406_Calanus_no_visible_lipid_sac\export_5108_20250311_1406\100" # UVP6 DE, Calanus not classified as with visible lipid sac
destination_folder = r"C:\Users\patri\python_workspace\uvp6_de_amund23p2_predictions\images_for_prediction"
reference_folder = r"C:\Users\patri\python_workspace\uvp6_de_amund23p1_lipid\data\segmentations_processed"

move_different_files(source_folder, destination_folder, reference_folder)

