# Purpose of the script
The purpose of the script developed to return a section from a JSON file is to extract specific information from a book that has been parsed. The JSON file contains structured data from the book, and the script is designed to locate and return a particular section of the book, based on the information provided. This script can be used to extract information from multiple books, and the extracted data can be used for various purposes such as analysis, research, etc.

## Useful Information
In the case of the JSON structures provided, one (*Algebra.json*) has a nested structure with a list of items, while the others (*Chemistry 2e.json*, *College Physics 2e.json*) have a flat structure with each item as a direct child. Therefore, it is important to handle both structures differently to ensure that all data is captured correctly. By using two different blocks of code within the **json_to_section** function, toggled by the value of *nested_list* argument, and each tailored to handle a specific structure, we can ensure that all data is captured regardless of the JSON file's format. This ensures that we do not miss any important information and can process the data accurately and efficiently.

## Function
The main.py file accepts a path to json files of parsed books. These files contain portions called sections. The file then returns all sections alongside their page numbers in a csv file format; a csv file for each json file.

## Intructions
- Open the booksPath.json file
- Replace the **./parsed_books/** value with the **absolute** path location of the json files
- Replace the **results** value with the name of the directory you want results to be saved
- Run the json_section_extractor.py file
