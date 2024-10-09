import ast
import os
import pathlib
from concurrent.futures import ThreadPoolExecutor

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
    output_path = (
        root_folderpath / f"{data['image'][-40:-4]}-{data['label']['polygonlabels'][0]}_mask.png"
    )
    cv2.imwrite(str(output_path), mask * 255)


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
    df["label"] = df["label"].apply(lambda x: x[0])

    # Ensure the destination folder exists
    create_folder_if_not_exists(root_folderpath)

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for each row
        futures = [
            executor.submit(process_row, row_data, root_folderpath)
            for idx, row_data in df.iterrows()
        ]

        # Wait for all threads to complete
        for future in futures:
            future.result()


if __name__ == "__main__":
    csv_path = r"C:\Laval_Postdoc\Laval-imaging-analysis\mask_vs_points\project-11-points.csv"
    root_folderpath = r"C:\Laval_Postdoc\Laval-imaging-analysis\mask_vs_points\masks\project11"
    create_mask_from_csv(csv_path, root_folderpath)
