# This is the script for moving the prosome/lipid masks created from label studio to a separate folder to input in the segmentation model.

import os
import shutil

def copy_and_rename_files(source_folder, target_folder, string_to_remove):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Iterate over files in the source folder
    for filename in os.listdir(source_folder):
        # Check if the filename contains the string to remove
        if string_to_remove in filename:
            # Create the new filename by removing the string
            # new_filename = filename.replace(string_to_remove, '')
            # new_filename = new_filename[9:]
            
            new_filename = filename.replace('-Prosome_mask', '').replace('_', ' ')
            
            # Construct full file paths
            source_file = os.path.join(source_folder, filename)
            target_file = os.path.join(target_folder, new_filename)
            
            # Copy the file to the target folder with the new name
            shutil.copy2(source_file, target_file)
            print(f'Copied and renamed: {filename} -> {new_filename}')

# Example usage
source_folder =  r"C:\Users\patri\python_workspace\data\segmentations_prosome"
target_folder =  r"C:\Users\patri\python_workspace\data\segmentations_prosome_ed"
string_to_remove = '-Prosome_mask'

copy_and_rename_files(source_folder, target_folder, string_to_remove)


# ## The code below copies all image files that have lipid/prosome masks to a separate folder for the segmentation runs

# def move_similar_files(source_folder, destination_folder, reference_folder):
#     # Ensure destination folder exists
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     # Get the list of file names from the reference folder
#     reference_filenames = set(os.listdir(reference_folder))

#     # Iterate through files in the source folder
#     for filename in os.listdir(source_folder):
#         source_path = os.path.join(source_folder, filename)

#         # Check if it's a file and if the filename is in the reference list
#         if os.path.isfile(source_path) and filename in reference_filenames:
#             destination_path = os.path.join(destination_folder, filename)
            
#             # Move the file to the destination folder
#             shutil.move(source_path, destination_path)
#             print(f"Moved: {filename}")

# # Example usage
# source_folder = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\UVP6_darkedge_copepod_black_bg"
# destination_folder = r"C:\Users\patri\project15_results\images_with_masks"
# reference_folder = r"C:\Users\patri\project15_results\lipid_masks"

# move_similar_files(source_folder, destination_folder, reference_folder)
