# NSMQ - Kwame AI Project

- **Author:** Ernest Samuel
- **Team:** Data Preprocessing Team
- **Date:** June 25, 2023


## General Information

This README provides an overview of two essential scripts developed for the "NSMQ - Kwame AI Project." The scripts are designed to streamline data processing tasks related to HTML content structuring and JSON to text file conversion. Each script comes with detailed explanations of its functions, instructions for running the scripts, and information about library dependencies.

---

## HTML Parsing for Textbook Content Structuring and JSON to Text File Conversion Scripts


These scripts have been developed to facilitate data processing tasks in the context of the "NSMQ - Kwame AI Project." Below, we outline the functionality of each script along with instructions for running them.

### HTML Parsing for Textbook Content Structuring
- File name: extract_textbook_from_url_notebook_.ipynb

#### Functions
1. **unique(array):** Eliminates duplicate items from a processed dataset.
2. **extract_rawTable_of_content(link, homePage):** Extracts the table of contents of a textbook from a website.
3. **extract_url(link, pageList, maxNmber, char):** Assembles URLs by concatenating the link with content-specific page identifiers.
4. **extract_url_content(url, file_name):** Extracts and structures content from a URL, saving it as a JSON file.
5. **extract_textbook(url_list, textbook_name):** Extracts content iteratively, saving it as a JSON file named after the textbook.


### JSON to Text File Conversion Script
- File name: json_to_txt_script_notebook_.ipynb

#### Functions
1. **convert_dict_to_strings():** Converts a dictionary of strings into a list of strings.
2. **convert_list_to_strings():** Transforms a list of lists into a list of strings.
3. **convert_to_txt_or_csv(input_filename, output_format):** Reads input JSON, formats sections, and generates output in .csv or .txt format.


### Running the Scripts

To run the scripts, follow the instructions below based on your preferred environment.

#### Using Google Colab
1. Upload the notebook to your Google Drive.
2. Open the notebook using Google Colab.
3. Follow the notebook's instructions to run the respective functions.

#### Using Anaconda/Jupyter Notebook
1. Ensure Anaconda is installed on your system.
2. Open Anaconda Navigator and launch Jupyter Notebook.
3. Navigate to the folder containing the notebook.
4. Open the notebook and run the relevant functions.

#### Using Visual Studio Code (VSC)
1. Open VSC and navigate to the folder containing the notebook.
2. Open the notebook and run the relevant functions.

### Library Dependencies

Both scripts include the necessary libraries for their functions. If any library is not already installed, the scripts will attempt to install them when executed. If you encounter any issues, ensure you have an active internet connection and administrative privileges to install libraries.

---

This documentation provides an overview of the two scripts, their functionality, instructions for running them, and information about library dependencies. It aims to provide clarity and guidance for users and collaborators participating in the "NSMQ - Kwame AI Project."
