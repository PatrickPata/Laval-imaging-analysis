# This script processes the output of the label studio segmentations and produces the mask files for the UVP data.

import ast
import os
import pathlib
from concurrent.futures import ThreadPoolExecutor

import csv
import cv2
import numpy as np
import pandas as pd


def create_folder_if_not_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def create_mask_from_polygon_data(data, root_folderpath: pathlib.Path):
    width = data["label"]["original_width"]
    height = data["label"]["original_height"]
    mask = np.zeros((height, width), dtype=np.uint8)

    # Step 2: Convert relative points to actual pixel coordinates
    scaled_points = [
        [int(x * width / 100), int(y * height / 100)] for x, y in data["label"]["points"]
    ]

    # Step 3: Convert points to integer coordinates for OpenCV
    polygon_points = np.array(scaled_points, np.int32)

    # OpenCV expects the points in a shape of (number_of_points, 1, 2)
    polygon_points = polygon_points.reshape((-1, 1, 2))

    # Step 4: Draw/Fill the polygon in the mask with a value of 1
    cv2.fillPoly(mask, [polygon_points], color=1)
    label_name = data['label']['polygonlabels'][0]
    output_subfolder = root_folderpath / label_name
    output_subfolder.mkdir(parents=True, exist_ok=True)
    # output_path = output_subfolder / f"{data['image'][-24:-4]}.png"
    output_path = output_subfolder / f"{data['image'].split('-',1)[1]}"
    cv2.imwrite(str(output_path), mask) #For UVP6/Appsilon, the masks are in 0,1

    # Step 5: Count the number of vertices/points in the polygeon
    num_vertices = len(scaled_points)

    # Step 6: Save the results in a CSV file
    csv_output_path = root_folderpath / "mask_vertices_count.csv"
    csv_file_exists = csv_output_path.exists()
    with open(csv_output_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header only if the CSV file does not exist yet
        if not csv_file_exists:
            csv_writer.writerow(["image", "label", "num_vertices"])
        csv_writer.writerow([data['image'], data['label']['polygonlabels'][0], num_vertices])


def process_row(row_data, root_folderpath):
    # Function to process a single row
    create_mask_from_polygon_data(row_data, root_folderpath)


def create_mask_from_csv(csv_path, masks_dst_folderpath, num_threads=4):
    # Convert the folder path to a pathlib Path object
    root_folderpath = pathlib.Path(masks_dst_folderpath)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Apply the necessary transformations to the "label" column
    df["label"] = df["label"].apply(lambda x: x.replace("true", "True"))
    df["label"] = df["label"].apply(ast.literal_eval)

    # Create a copy of df for the instances when there are 2 polygons
    df2 = df[df["label"].apply(lambda x: len(x) > 1)].copy()
    
    df2["label"] = df2["label"].apply(lambda x: x[1])
    df["label"] = df["label"].apply(lambda x: x[0])

    print(df["label"].head(6))
    print(df2["label"].head(6))

    # Ensure the destination folder exists
    create_folder_if_not_exists(root_folderpath)

    # Function to run multithreading on a DataFrame
    def run_multithreading(dataframe):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit tasks for each row
            futures = [
                executor.submit(process_row, row_data, root_folderpath)
                for idx, row_data in dataframe.iterrows()
            ]

            # Wait for all threads to complete
            for future in futures:
                future.result()

    # Run multithreading on the original DataFrame
    run_multithreading(df)

    # Run multithreading on the subset with a second label
    if not df2.empty:
        run_multithreading(df2)


if __name__ == "__main__":
    # csv_path = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\TEST.csv"
    csv_path = r"C:\Users\patri\OneDrive - Université Laval\Laval_Postdoc\Laval-imaging-analysis\UVP6_darkedge\project-15-at-2025-01-14-16-16-cc93788f.csv"
    root_folderpath = r"c:\Users\patri\project15_results" # TODO must export outside onedrive... also separate prosome and lipid segmentations to separate folders
    create_mask_from_csv(csv_path, root_folderpath)




