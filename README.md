# RAW Mover

RAW Mover is a simple, user-friendly desktop application designed to help photographers and enthusiasts organize their RAW image files. It automatically identifies paired RAW and JPG/PNG/JPEG files in a selected folder and moves the RAW files into a dedicated `RAW_Files` subfolder, keeping your main photo directories clean and organized.

## Features

*   **Effortless Organization:** Automatically moves RAW files to a designated subfolder.
*   **Intelligent Pairing:** Identifies RAW files that have a corresponding JPG/PNG/JPEG file based on their filename.
*   **Wide RAW Format Support:** Supports popular RAW formats including `.nef`, `.cr2`, `.cr3`, `.arw`, `.dng`, `.rw2`, `.orf`, `.pef`, `.raf`, `.srw`, `.x3f`.
*   **Intuitive Interface:** Easy-to-use graphical interface with drag-and-drop functionality for selecting folders.
*   **Progress Tracking:** Live updates on the moving process and overall status.

## How to Use

### 1. Download and Run

Simply download the `RAW Mover.exe` file and run it. No installation is required.

### 2. Select Your Photo Folder

You have two ways to select the folder containing your RAW and JPG/PNG/JPEG files:

*   **Browse Button:** Click the "Browse" button and navigate to your desired folder.
*   **Drag and Drop:** Drag and drop your photo folder directly onto the RAW Mover application window.

### 3. Start Moving RAWs

Once you've selected your folder, click the "Start Moving RAWs" button. The application will then:

*   Scan the selected folder for RAW and JPG/PNG/JPEG files.
*   Identify RAW files that have a matching JPG/PNG/JPEG file (e.g., `IMG_1234.NEF` will be matched with `IMG_1234.JPG`).
*   Create a new subfolder named `RAW_Files` within your selected folder (if it doesn't already exist).
*   Move all identified RAW files into this new `RAW_Files` subfolder.

You will see progress updates and log messages within the application window.

### 4. Review Results

After the process is complete, a summary message will be displayed, indicating how many RAW files were moved. Your original folder will contain only the JPG/PNG/JPEG files (and any other files that weren't paired or weren't RAWs), and the `RAW_Files` subfolder will contain your organized RAW images.

## Supported RAW Extensions

*   `.nef` (Nikon Electronic Format)
*   `.cr2` (Canon Raw 2)
*   `.cr3` (Canon Raw 3)
*   `.arw` (Sony Alpha Raw)
*   `.dng` (Adobe Digital Negative)
*   `.rw2` (Panasonic Raw)
*   `.orf` (Olympus Raw Format)
*   `.pef` (Pentax Electronic File)
*   `.raf` (Fujifilm Raw)
*   `.srw` (Samsung Raw)
*   `.x3f` (Sigma X3F Raw)

## Troubleshooting

*   **"Folder not found" error:** Ensure the selected folder exists and you have the necessary permissions to access it.
*   **"No paired RAW and JPG files found" message:** This means the application couldn't find any RAW files with a corresponding JPG/PNG/JPEG in the selected folder, or there were no RAW files at all.
*   **Files not moving:** Check if the files are open in another application or if you have write permissions to the folder.

## Support & Feedback

If you encounter any issues, have suggestions, or need custom tools, feel free to contact the developer via Facebook: [Bibhuti on Facebook](https://www.facebook.com/bibhutithecoolboy)

## Donation

If you find RAW Mover useful and would like to support its development, please consider making a donation by clicking the "Donate" button in the application.

Thank you for using RAW Mover!
