# Python script to crop riddle section of National Science and Math Quiz video

## Instruction to install anaconda

You need to have anaconda installed to proceed with the following steps.
This will ensure you can create and activate the conda environment.

Follow the link below to install Anaconda.

[Anaconda](https://www.anaconda.com/download/)

## Create a conda environment using the yaml file provided

```bash
conda env create -f environment.yml
```

## Activate environment

```bash
conda activate brilla-ai
```

## Deactivate environment

```bash
conda deactivate
```

Please note that, on Windows, a separate anaconda command shell will be installed to use the above commands. The above can be done on a Mac terminal once Anaconda is installed.

## Instruction file (ins.json)

- Provide root path containing videos as a value of **"root_path"**. Root path should be an absolute path.
- A Windows root path may need additional backslashes.
- **Original example**: "C:\Users\name\software_projects\nsmqai_test\Videos". The original example will throw an error in the instuction file.
- Modify by including additional backslashes as shown in the modified version. **Modified version**: "C:\\Users\\name\\software_projects\\nsmqai_test\\Videos".
- Provide the destination path of cropped videos as a value of **"destination_path"**.
- The root path and destination paths are required in order to run the script.
- Ensure the videos are in mp4 format.

**Please note that, python script and instruction file should be in the same directory.**

## How to use script

**Estimated run time using 10 sample videos**: about 1 hour.

Execute python script

```bash
python crop_riddle_fs_video.py
```
