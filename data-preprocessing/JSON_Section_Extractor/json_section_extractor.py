import json
import os
import sys
import argparse

# reads bookPaths.json to obtain absolute path of the location of json files to be used.

def read_PATH_json():
    with open('booksPath.json', 'r') as file:
        return json.load(file)

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
def json_to_section(json_dict, pages, sections, nested_list=False): 
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
        for page in json_dict:
            try:
                for subpage in json_dict[page]:
                    section = json_section(subpage)
                    pages.append(page)
                    sections.append(str(" ".join(section)))
            except:
                continue


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Open the CSV file in write mode
def write_sections_to_txt(file, list1, list2, directory):
    # to obtain the filename without the end extension '.json', the last five(5) characters from the filename must be stripped off...
    # for eg: Algebra.json can be changed to Algebra by using Algebra.json[:-5], with the -5 taking care of the last five characters.
    filename = f"{file[:-5]}.txt"
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        for item1, item2 in zip(list1, list2):
            file.write(f"{item1}\t{item2}\n")


class ScriptUsage:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def version(self):
        print("Script version: 1.0")

    def instruction(self):
        print("Script instructions:")
        print("1. Provide the absolute path to the json files in the booksPath.json file.")
        print("2. Make sure the files in the path provided end with an json extension.")
        print("3. Provide the name of the directory that should be created in the root directory, in which results will be stored.")

    #def help(self):
    #    self.parser.print_help()
    
    def main(self):
        books_paths = read_PATH_json()
        parsed_books_path = books_paths['path_to_parsed_books']
        results_path = books_paths['directory']
        all_json_files = put_json_filenames_in_list(parsed_books_path)

        for file in all_json_files:
            pages = []
            sections = []
            json_dict = load_json_file(file, parsed_books_path)


            json_to_section(json_dict,pages, sections, nested_list=True)

            # second json structure
            if len(sections) == 0: # checks if all sections are empty strings. If yes, there is a tendency that the current json contain direct objects and not nested lists.
                json_to_section(json_dict, pages, sections) # return all sections using the second json structure as the standard.

            # write results to csv file
            create_directory(results_path)
            write_sections_to_txt(file, pages, sections, results_path)



    def parse_args(self):
        self.parser.add_argument('-v', '--version', action='store_true', help='Display script version')
        self.parser.add_argument('-i', '--instruction', action='store_true', help='Display script instructions')
        args = self.parser.parse_args()

        if args.version:
            self.version()
        elif args.instruction:
            self.instruction()
        else:
            self.main()


if __name__ == '__main__':
    usage = ScriptUsage()
    usage.parse_args()
