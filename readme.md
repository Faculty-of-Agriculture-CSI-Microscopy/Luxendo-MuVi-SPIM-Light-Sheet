# Luxendo-MuVi-SPIM-Light-Sheet tools


## `h5`-to-`tiff`-converter

This script processes HDF5 files containing 3D datasets and converts them to TIFF stacks. It includes a simple GUI built with Tkinter to select the input and output directories and provides options to process either a single folder or all subfolders.

### Features

- Select an input folder containing HDF5 files and JSON metadata files.
- Convert HDF5 files to TIFF stacks with proper voxel dimensions.
- Process files in a single folder or recursively through all subfolders.
- Maintain the original folder structure for output files in multi-folder processing mode.

### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python packages: `h5py`, `tifffile`

You can install the required packages using pip:

```bash
pip install h5py tifffile
```

### Using the Script

1. **Starting the Script:** Run the script using your IDE (Visual Studio/pyCharm/etc.), A GUI will appear.
   - **Optional:** You can run the script in its `.exe` form without IDE,
     - download here: [luxendo-h5-converter-v4](https://drive.google.com/file/d/1WM5jQPoOsyuh9N5cmqhcpchNJcUYdcZu/view?usp=sharing)
> [!NOTE]
> Windows might flag this file as a virus. Once you see the warning, you can click on `More info` and then `Run anyway` to use this program.

<img width="399" alt="2024-06-03_17h22_32" src="https://github.com/Faculty-of-Agriculture-CSI-Microscopy/Luxendo-MuVi-SPIM-Light-Sheet/assets/55537771/7fef56e4-555a-4ea2-bcd7-f3fb53d6dbb3">
<img width="399" alt="2024-06-03_17h22_41" src="https://github.com/Faculty-of-Agriculture-CSI-Microscopy/Luxendo-MuVi-SPIM-Light-Sheet/assets/55537771/a9c98f50-6388-49d0-b138-dafacfefe34e">




3. **Selecting Directories:**

   <img width="605" alt="Converter GUI" src="https://github.com/Faculty-of-Agriculture-CSI-Microscopy/Luxendo-MuVi-SPIM-Light-Sheet/assets/55537771/d2c51f3f-7f50-4adc-8966-cfd089fb9f69">
   
  - **Process Single Folder:**
    - Click the "Process Single Folder" button.
    - Select the input folder containing the HDF5 files.
    - Select the output folder where the TIFF files will be saved.
    - The script will process all HDF5 files in the selected input folder and save the converted TIFF files in the output folder.

  - **Process Entire Directory Tree:**
    - Click the "Process Entire Directory Tree" button.
    - Select the input folder containing the HDF5 files.
    - The script will process all HDF5 files in the selected folder and all its subfolders.
    - The converted TIFF files will be saved in their corresponding original folders within the input directory.
3. **Monitoring Progress:** The GUI window will display the processing status, including the current folder and file being processed.

4. **Completion:** a message will be displayed in the status window once processing is complete.










