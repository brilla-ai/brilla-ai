# Web Textbook Parsing Script

This Python script extracts content from selected online textbooks, converts the extracted data to JSON, and optionally converts it to TXT or CSV format.

## Instructions

### 1. Install Required Libraries
Before running this script, make sure to install the required libraries by executing the following commands in your command-line/terminal:

- To install the 'requests' library, run: `pip install requests`
- To install the 'beautifulsoup4' library, run: `pip install beautifulsoup4`
- To install the 'pandas' library, run: `pip install pandas`

### 2. Set Up the Script
1. Save this file in the same folder as `json_to_txt_or_csv.py` and `url_textbook_to_json.py`.
2. Each scripts contains additional instructions that could be useful
2. Prepare a CSV file with columns 'BOOKS' for textbook names and 'URL' for textbook URLs.
3. Update the `csv_file` variable with the path to your CSV file.

### 3. Extract Content from Textbooks
Run this script to extract content from selected textbooks and save it as JSON.

### 4. (Optional) Convert to TXT or CSV
If needed, change the `output_format` variable to either 'txt' or 'csv' to convert the JSON to your desired format.

## Author
Ernest Samuel

## Date
16/09/2023
