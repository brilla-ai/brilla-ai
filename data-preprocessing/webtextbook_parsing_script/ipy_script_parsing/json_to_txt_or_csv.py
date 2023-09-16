"""
Data Converter Script

This Python script extracts structured data from a JSON file, applies formatting, and saves it as a .txt or .csv file.

Instructions:
1. Ensure you have the required libraries installed: json, os, and csv.
2. Save this code in a separate Python file, e.g., data_converter.py.
3. Import this code file in your main script using:
   `from json_to_txt_or_csv import convert_to_txt_or_csv`.
4. When you want to convert a JSON file to either a text file or a CSV file, call the `convert_to_txt_or_csv` function with the appropriate arguments.
5. Replace `"example.json"` with the path to your input JSON file and set `output_format` to either `"txt"` or `"csv"`.
6. Run your main script to execute the data conversion process.

Author: Ernest Samuel
Date: 16/09/2023

"""


import json
import os
import csv

# Data processing functions

def convert_dict_to_strings(dict_of_strings):
    """
    Converts a dictionary of strings to a list of strings.

    Args:
        dict_of_strings: A dictionary of strings.

    Returns:
        A list of strings.
    """
    new_list = []
    if isinstance(dict_of_strings, dict):
        raise TypeError("dict_of_strings must not be a dictionary")

    for dic in dict_of_strings:
        for key, value in dic.items():
            new_list.append(f"{key}: {value}")

    return new_list

def convert_list_to_strings(list_of_lists):
    """
    Converts a list of lists to a list of strings.

    Args:
        list_of_lists: A list of lists.

    Returns:
        A list of strings.
    """
    new_list = []
    for list_item in list_of_lists:
        new_list.append("\n".join(map(str, list_item)))
    return new_list

# Main function

def convert_to_txt_or_csv(input_filename, output_format="txt"):
    """
    Extracts structured data from a JSON file, applies formatting, and saves it as a .txt or .csv file.

    Args:
        input_filename (str): The name of the input JSON file for processing.
        output_format (str): The desired output file format (txt or csv).
    """

    # Read the input JSON file
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)

    # Extract input file information
    input_dir, base_name = os.path.split(input_filename)
    base_name_without_extension, _ = os.path.splitext(base_name)

    # Prepare the output folder
    output_folder = os.path.join(input_dir, "formatted_files")
    os.makedirs(output_folder, exist_ok=True)

    # Container for formatted sections
    formatted_sections = []

    # Container for CSV data
    csv_data = []

    # Iterate through pages and sections
    for page_data in data:
        for page_title in page_data.keys():
            sections = page_data[page_title]
            for section in sections:
                # Construct formatted section
                formatted_section = f"__section__\n**{section['title']}**\n"
                formatted_section += "\n\n_paragraph_ \n".join(section['Section']) + "\n"
                formatted_section += "\n**Lists**\n"
                formatted_section += "\n".join(convert_list_to_strings(section['lists'])) + "\n"
                formatted_section += "\n**Table**\n"
                formatted_section += "\n".join(convert_list_to_strings(section['tables'])) + "\n"
                formatted_section += "\n**Figures**\n"
                formatted_section += "\n".join(convert_dict_to_strings(section['figures'])) + "\n\n"
                formatted_sections.append(formatted_section)

                # Prepare numbered CSV data
                paragraph_numbered = [f"_paragraph_{i+1}\n {p}" for i, p in enumerate(section['Section'])]
                lists_numbered = [f"_list_{i+1}\n {l}" for i, l in enumerate(convert_list_to_strings(section['lists']))]
                tables_numbered = [f"_table_{i+1}\n {t}" for i, t in enumerate(convert_list_to_strings(section['tables']))]
                figures_numbered = [f"_figure_{i+1}\n {f}" for i, f in enumerate(convert_dict_to_strings(section['figures']))]

                csv_row = {
                    "Section Title": section['title'],
                    "Paragraphs": "\n".join(paragraph_numbered),
                    "Lists": "\n".join(lists_numbered),
                    "Table": "\n".join(tables_numbered),
                    "Figures": "\n".join(figures_numbered)
                }
                csv_data.append(csv_row)

    # Determine the output file name and format
    if output_format == "txt":
        output_file_name = os.path.join(output_folder, f"{base_name_without_extension}.txt")
        formatted_output = "\n\n".join(formatted_sections)
    elif output_format == "csv":
        output_file_name = os.path.join(output_folder, f"{base_name_without_extension}.csv")

        # Use csv.DictWriter to write CSV data
        with open(output_file_name, 'w', encoding="utf-8", newline='') as csv_file:
            fieldnames = ["Section Title", "Paragraphs", "Lists", "Table", "Figures"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)

        formatted_output = None  # No formatted output for CSV
    else:
        print("Invalid output format. Supported formats are 'txt' and 'csv'.")
        return

    # Save the formatted data to the output file
    if formatted_output:
        with open(output_file_name, 'w') as output_file:
            output_file.write(formatted_output)

    print(f"{base_name_without_extension} Data extracted and saved as .{output_format} successfully in {output_folder}.")
