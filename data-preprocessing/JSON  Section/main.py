import json
import os
import csv

# absolute location of the json files
PATH = "."

# search for json files in the directory and add their names to a list
def put_json_filenames_in_list():
    json_files = [] 
    for filename in os.listdir(PATH):
        if filename.endswith(".json"):
            json_files.append(filename)
    return json_files

# load all json file
def load_json_file(json_file):
    with open(PATH+json_file, "r") as file:
        entire_json = json.load(file)
        return entire_json[0]

# obtain the section from json file
def Section(json_dictionary):
    try:
        section=json_dictionary["Section"]
        return section
    except:
        return ''



ALL_JSON_FILES = put_json_filenames_in_list()


for file in ALL_JSON_FILES:
    PAGES = []
    SECTIONS = []
    json_dict = load_json_file(file)


    for page in json_dict:
        try:
            for subpage in json_dict[page][0][1]:
                section = Section(subpage)
                PAGES.append(page)
                SECTIONS.append(str(" ".join(section)))
        except:
            continue

    # second json structure
    if len(SECTIONS) == 0:
        for page in json_dict:
            try:
                for subpage in json_dict[page]:
                    section = Section(subpage)
                    PAGES.append(page)
                    SECTIONS.append(str(" ".join(section)))
            except:
                continue



    filename = f"{file[:-5]}.csv"

    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers
        writer.writerow(['PAGE', 'SECTION'])
        
        # Write the data row by row
        for i in range(len(PAGES)):
            writer.writerow([PAGES[i], SECTIONS[i]])

