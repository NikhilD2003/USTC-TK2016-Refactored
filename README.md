# USTC-TK2016 (Refactored & Fixed)

This repository is an improved, modernized, and debugged toolkit originally based on "USTC-TK2016", used to parse network traffic (`.pcap` files) and transform them into an image dataset formatted like MNIST. The dataset commonly processed with this tool is "USTC-TFC2016".

**Note:** This version is heavily optimized and debugged for modern Windows environments.

> **NOTICE:** This repository credits [echowei/DeepTraffic](https://github.com/echowei/DeepTraffic) and [davidyslu/USTC-TK2016](https://github.com/davidyslu/USTC-TK2016).

---

## 💡 What's Changed in this Refactored Version?
The original repository had a great conceptual foundation but failed to execute out-of-the-box due to legacy toolchains and missing files. This version introduces the following major fixes:

* **SplitCap Modernization (No more missing DLLs!):** Upgraded the underlying SplitCap tool to a newer version. The original repo relied on an old version of SplitCap that required external `.dll` files (like `PacketParser.dll`), which were missing from the repository. The new version has these features built-in, completely eliminating the dependency crashes.
* **PowerShell (`.ps1`) Script Fixes:** Rewrote and corrected errors in the PowerShell execution scripts to interface correctly with modern Python versions and handle dataset processing without throwing execution blocks.
* **Python Dependency Updates:** Completely replaced deprecated packages (e.g., swapped out the ancient `PIL 1.1.6` for modern `Pillow` and updated `numpy`).
* **General Bug Fixes:** Patched various code and logic errors that prevented the pipeline from completing the conversion process.
* **System Requirements Documented:** Identified and documented the explicit requirement for `.NET Framework 3.5` to run the updated SplitCap tool on modern Windows machines, preventing the script from failing silently or throwing cryptic environment errors.

---
## Prerequisites
* **Python 3.8+**
* **Windows PowerShell** (for running the `.ps1` extraction scripts)
* **.NET Framework 3.5:** This is strictly required for the updated SplitCap tool to execute. 
  * *How to enable on Windows:* Press the Windows key, search for "Turn Windows features on or off", check the box for `.NET Framework 3.5 (includes .NET 2.0 and 3.0)`, and click OK to install.

## ⚙️ Installation

1. **Clone this repository on your machine:**
   
   # Clone the refactored repository
   $ git clone [https://github.com/](https://github.com/)[Your-Username]/[Your-Repo-Name].git
   $ cd [Your-Repo-Name]

2. **Install the required modern packages:**
  # Run the command at the root of the repository
  $ pip install -r requirements.txt 

## 🚀 Execution Pipeline
Step 1: Prepare the Data
Download the traffic dataset (e.g., USTC-TFC2016) and put the .pcap files directly into the directory 1_Pcap\.

Step 2: Extract Sessions
Open Windows PowerShell and run 1_Pcap2Session.ps1. This takes the raw PCAP files from Step 1 and uses the updated SplitCap tool to divide them.

Configuration: * To split the PCAP file by each session, ensure lines 10 and 14 in 1_Pcap2Session.ps1 are uncommented, and lines 11 and 15 are commented.

To split the PCAP file by each flow, ensure lines 11 and 15 are uncommented, and lines 10 and 14 are commented.
# Make sure your current directory is correct
PS> .\1_Pcap2Session.ps1
Output Generated: If successful, this creates new subdirectories inside 2_Session\:

AllLayers\ - Contains the raw separated PCAP files.

L7\ - Contains the Layer 7 (Application Layer) separated PCAP files.
(These extracted sessions are now ready to be filtered and trimmed in Step 3).

Step 3: Process and Trim Sessions
Run 2_ProcessSession.ps1. This script takes the files from 2_Session\ and standardizes their sizes so they can be converted into uniform images.
PS> .\2_ProcessSession.ps1

Output Generated:
If successful, this creates several subdirectories inside 3_ProcessedSession\:

FilteredSession\ - Contains the top 60,000 largest PCAP files extracted from the previous step.

TrimedSession\ - Contains the filtered PCAP files uniformly trimmed to exactly 784 bytes (to represent a 28x28 image). If a file is shorter than 784 bytes, it appends 0x00 to pad it.

Test\ & Train\ - The trimmed sessions are randomly split and sorted into these two subfolders for machine learning.
(These standardized Test and Train files are passed to Python in Step 4).

Step 4: Convert Sessions to PNG Images
Run the Python script 3_Session2Png.py. This reads the 784-byte files from the 3_ProcessedSession\Test\ and Train\ folders and uses the Pillow library to render them as 28x28 grayscale images.

PS> python 3_Session2Png.py

Output Generated:
If successful, this creates image files inside the 4_Png\ directory:

Test\ - Contains .png images for testing.

Train\ - Contains .png images for training.
(These images represent your network traffic visually and are used in the final step).

Step 5: Generate MNIST Format Dataset
Run the final script 4_Png2Mnist.py. This script converts the .png images from Step 4 into the official binary format used by the MNIST database, making it plug-and-play for standard machine learning models.

PS> python 4_Png2Mnist.py

Output Generated:
If successful, you will see the final compiled training datasets in the 5_Mnist\ folder:

-train-images-idx1-ubyte

-train-images-idx3-ubyte

-train-images-idx1-ubyte.gz

-train-images-idx3-ubyte.gz

You are done! The data in 5_Mnist\ is now ready to be fed into your classification models.
