import json
import os
import csv

# reads bookPaths.json to obtain absolute path of the location of json files to be used.

def read_PATH_json():
    with open('bookPaths.json', 'r') as file:
        return json.load(file)['path_to_parsed_books']

# search for json files in the directory and add their names to a list
def put_json_filenames_in_list(parsed_books_path):
    json_files = [] 
    for filename in os.listdir(parsed_books_path):
        if filename.endswith(".json"):
            json_files.append(filename)
    return json_files

# load all json file
def load_json_file(json_file, parsed_books_path):
    with open(parsed_books_path+json_file, "r") as file:
        entire_json = json.load(file)
        return entire_json[0]

# obtain the section from json object (dictionary).
def json_section(json_dictionary):
    try:
        section=json_dictionary["Section"]
        return section
    except:
        return ''


# nested_list argument is optional as it has a default false value. The argument is used to distinguish the two json formats used. Thus it handles the json files based on whether or not they contain nested lists or direct objects in a single list.
def json_to_section(json_dictionary, nested_list=False): 
    if nested_list:
        for page in json_dict:
            try:
                for subpage in json_dict[page][0][1]:
                    section = json_section(subpage)
                    pages.append(page)
                    sections.append(str(" ".join(section)))
            except:
                continue
    else:
        for page in json_dictionary:
            try:
                for subpage in json_dictionary[page]:
                    section = json_section(subpage)
                    pages.append(page)
                    sections.append(str(" ".join(section)))
            except:
                continue

def write_sections_to_csv(file, pages, sections):
    # to obtain the filename without the end extension '.json', the last five(5) characters from the filename must be stripped off...
    # for eg: Algebra.json can be changed to Algebra by using Algebra.json[:-5], with the -5 taking care of the last five characters.
        
    filename = f"{file[:-5]}.csv"
        # Open the CSV file in write mode
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers
        writer.writerow(['PAGE', 'SECTION'])
        
        # Write the data row by row
        for i in range(len(pages)):
            writer.writerow([pages[i], sections[i]])


parsed_books_path = read_PATH_json()
all_json_files = put_json_filenames_in_list(parsed_books_path)


if __name__ == '__main__':

    for file in all_json_files:
        pages = []
        sections = []
        json_dict = load_json_file(file, parsed_books_path)


        json_to_section(json_dict, nested_list=True)

        # second json structure
        if len(sections) == 0: # checks if all sections are empty strings. If yes, there is a tendency that the current json contain direct objects and not nested lists.
            json_to_section(json_dict) # return all sections using the second json structure as the standard.

        # write results to csv file
        write_sections_to_csv(file, pages, sections)

