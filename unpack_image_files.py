import os
import shutil

# Define the root directory containing subfolders and the destination directory
root_dir = r"C:\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\export_5108_20241018_1518"
destination_dir = r"C:\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\export_5108_20241018_1518_white_bg"

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Walk through all subdirectories in the root directory
for subdir, _, files in os.walk(root_dir):
    for file in files:
        # Get the full file path
        file_path = os.path.join(subdir, file)
        
        # Move the file to the destination directory
        shutil.move(file_path, destination_dir)

print(f"All files have been moved to {destination_dir}")
