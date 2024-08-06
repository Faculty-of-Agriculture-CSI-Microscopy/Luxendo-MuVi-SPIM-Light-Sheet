import h5py
import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import tifffile
import json
import logging
import gc

# Function to select a directory
def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title=title)
    root.destroy()
    return folder_selected

# Function to update the status in the GUI and log file
def update_status(status_text):
    status_window.insert(tk.END, status_text + "\n")
    status_window.update()
    status_window.see(tk.END)  # Scroll to the bottom
    logging.info(status_text)

# Function to read voxel dimensions from JSON file
def read_voxel_dimensions(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        print(f"Contents of {json_file_path}: {data}")
        processing_info = data.get("processingInformation", {})
        voxel_size = processing_info.get("voxel_size_um", None)
        if voxel_size is None:
            raise KeyError(f"Key 'voxel_size_um' not found in {json_file_path}")
        print(f"Read voxel dimensions from {json_file_path}: width={voxel_size['width']}, height={voxel_size['height']}, depth={voxel_size['depth']}")
        return voxel_size["width"], voxel_size["height"], voxel_size["depth"]

# Function to find the corresponding JSON file
def find_json_file(h5_filename, directory):
    base_name = os.path.splitext(h5_filename)[0].split('.')[0]  # Extract base name before any extension
    for file in os.listdir(directory):
        if file.endswith('.json') and base_name in file:
            return os.path.join(directory, file)
    return None

# Function to process files in a directory
def process_files_in_directory(directory, output_directory=None, process_subfolders=False):
    for root, _, files in (os.walk(directory) if process_subfolders else [(directory, [], os.listdir(directory))]):
        update_status(f"Processing folder: {root}")
        for filename in files:
            if filename.endswith('.h5'):
                file_path = os.path.join(root, filename)
                json_file_path = find_json_file(filename, root)

                if json_file_path:
                    update_status(f"Found HDF5 file: {filename}")
                    update_status(f"Found JSON file: {os.path.basename(json_file_path)}")
                    files_found_value.config(text=f"HDF5: {filename}\nJSON: {os.path.basename(json_file_path)}")
                    try:
                        voxel_width, voxel_height, voxel_depth = read_voxel_dimensions(json_file_path)
                        voxel_dimensions_value.config(text=f"Width: {voxel_width} µm, Height: {voxel_height} µm, Depth: {voxel_depth} µm")
                        print(f"Voxel dimensions for {filename}: width={voxel_width}, height={voxel_height}, depth={voxel_depth}")
                        with h5py.File(file_path, 'r') as h5file:
                            if 'Data' in h5file:
                                dataset = h5file['Data'][:]
                                # Determine the output file path
                                if output_directory:
                                    output_file_dir = output_directory
                                else:
                                    output_file_dir = root

                                if not os.path.exists(output_file_dir):
                                    os.makedirs(output_file_dir)
                                output_file = os.path.join(output_file_dir, filename.replace('.h5', '.tiff'))

                                # Update the status window
                                update_status(f"Processing {filename}...")

                                # Save the 3D dataset as a TIFF stack with calibration
                                metadata = {
                                    'spacing': voxel_depth,
                                    'unit': 'um',
                                    'axes': 'ZYX',
                                    'creator': 'Daniel Waiger with GPT-4'
                                }
                                
                                extratags = [
                                    (305, 's', 20, "tifffile.py, changed", True),  # Software
                                ]

                                print(f"Metadata: {metadata}")

                                tifffile.imwrite(
                                    output_file, 
                                    dataset, 
                                    imagej=True, 
                                    resolution=(1 / voxel_width, 1 / voxel_height),
                                    metadata=metadata,
                                    extratags=extratags
                                )

                                # Update the status window and log file
                                update_status(f"Saved 3D dataset to {output_file}")
                            else:
                                update_status(f"No 'Data' dataset found in {file_path}")
                    except KeyError as e:
                        update_status(str(e))
                        print(str(e))
                    finally:
                        # Run garbage collection
                        gc.collect()
                else:
                    update_status(f"No JSON metadata file found for {filename}")
                    print(f"No JSON metadata file found for {filename}")

# Setup logging
log_file_path = os.path.join(os.getcwd(), 'processing_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# Setup the status window
status_root = tk.Tk()
status_root.title("Processing Status")
status_window = Text(status_root, height=20, width=150)
status_window.pack()

# Add labels to display filenames and voxel dimensions
files_found_label = tk.Label(status_root, text="Files Found:")
files_found_label.pack()

files_found_value = tk.Label(status_root, text="")
files_found_value.pack()

voxel_dimensions_label = tk.Label(status_root, text="Voxel Dimensions:")
voxel_dimensions_label.pack()

voxel_dimensions_value = tk.Label(status_root, text="")
voxel_dimensions_value.pack()

# Function to start processing for single folder
def process_single_folder():
    update_status("Selecting input directory...")
    input_directory = select_directory("Select Input Folder")
    update_status(f"Selected input directory: {input_directory}")

    update_status("Selecting output directory...")
    output_directory = select_directory("Select Output Folder")
    update_status(f"Selected output directory: {output_directory}")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    update_status("Processing files in the selected folder only...")
    process_files_in_directory(input_directory, output_directory=output_directory, process_subfolders=False)
    gc.collect()  # Run garbage collection at the end

# Function to start processing for all child folders
def process_all_folders():
    update_status("Selecting input directory...")
    input_directory = select_directory("Select Input Folder")
    update_status(f"Selected input directory: {input_directory}")

    update_status("Processing files in all child folders...")
    process_files_in_directory(input_directory, process_subfolders=True)
    gc.collect()  # Run garbage collection at the end

# Add buttons to choose between processing a single folder or all child folders
process_single_button = tk.Button(status_root, text="Process Single Folder", command=process_single_folder)
process_single_button.pack()

# process_all_button = tk.Button(status_root, text="Process All Subfolders", command=process_all_folders)
# process_all_button.pack()

status_root.mainloop()
