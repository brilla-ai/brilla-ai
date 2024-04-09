"""
This script extracts content from online textbooks, structures it, and saves it in JSON format.

Instructions:
1. Make sure you have Python installed.
2. Install the required libraries by running the following commands:
   - pip install requests
   - pip install beautifulsoup4
   - pip install pandas
3. Prepare a CSV file (openstax_textbooks_sheet.csv) with columns 'BOOKS' for textbook names and 'URL' for URLs.
4. Modify the 'selected_textbooks' variable to select specific textbooks by changing the indices.
5. Run this script to extract content, save it as JSON, and optionally convert it to other formats.

Author: Ernest Samuel
Date: 16/09/2023
"""

# ------------- Install, if missing, and import libraries ----------------------- #
# Install, if missing, and import libraries
"""
Instructions for libraries instructions if you dont have it installed

1. Before running this script, make sure to install the required libraries by executing the following commands in your command-line/terminal:
   - To install the 'requests' library, run: pip install requests
   - To install the 'beautifulsoup4' library, run: pip install beautifulsoup4
   - To install the 'pandas' library, run: pip install pandas

2. Once you have installed the required libraries, you can use this script to import them and perform your desired tasks.

"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

import os
from urllib.parse import urljoin
import json

#--------------------------- cleaning functions ------------------------------#
def unique(array):
    """
    Remove duplicates from a list while preserving the order of elements.
    
    Args:
        array (list): The input list containing elements.
        
    Returns:
        list: A new list with duplicates removed.
    """
    return list(dict.fromkeys(array))

def remove_items(superset_of_item, set_of_item):
    """
    Remove items in list 'set_of_item' from list 'superset_of_item' and return the filtered list.
    
    This function filters out a subset 'set_of_item' from a superset 'superset_of_item' list.
    It is used to exclude specific items from a list based on another list.
    
    Args:
        superset_of_item (list): The superset list.
        set_of_item (list): The subset list to be removed from 'superset_of_item'.
        
    Returns:
        list: A new list with items from 'set_of_item' removed from 'superset_of_item'.
    """
    superset_of_item = [item for item in superset_of_item if item not in set_of_item]
    return superset_of_item

#---------------------------------------------------------------------------------------------#
#-------------------------Extract table of content as url ----------------------------------------------------#

def extract_rawTable_of_content(link, homePage):
    """
    Extracts URLs of chapters from the table of contents of an online textbook.

    Args:
        link (str): Base URL of the textbook pages.
        homePage (str): First landing page of the online view of the textbook.

    Returns:
        list: A list of unique URLs representing chapters.
    """
    
    # Construct the complete URL for the table of contents page
    website_link = link + homePage
    url_list = []

    # Send a GET request to the website
    response = requests.get(website_link)
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table of contents div using its class
        table_of_contents_div = soup.find('div')

        if table_of_contents_div:
            # Find all the <a> tags within the table of contents div
            a_tags = table_of_contents_div.find_all('a')

            # Extract the href attribute from each <a> tag and store it in the list
            for a_tag in a_tags:
                href = a_tag.get('href')
                url_list.append(href)
        else:
            print("Table of contents div not found on the website.")
            
    # Ensure uniqueness of URLs in the list
    return unique(url_list)

#---------------- From Table of Contents as URL, Extract pages URL for each required page of the textbook ----------------#

def extract_url(link, pageList, maxNmber, alphabet_char=[]):
    """
    Extracts URLs for specific pages of an online textbook.

    Args:
        link (str): Base URL of the textbook pages.
        pageList (list): List of landing pages for specific chapters.
        maxNmber (int): Maximum number of index numbers of the table of content.
        alphabet_char (list, optional): List of alphabet characters or string indices. Default is an empty list.

    Returns:
        list: A list of unique URLs representing specified pages.
    """
    # Generate a combined list of numeric and alphabet characters
    list_pages = list(range(1, maxNmber + 1))
    list_pages.extend(alphabet_char)

    url = []
    
    # Iterate through the provided pageList
    for item in pageList:
        for value in list_pages:
            # Check if the item starts with the current value (number or alphabet)
            if item.startswith(str(value)):
                url.append(link + item)

    # Ensure uniqueness of URLs in the list
    return unique(url)



#-------------------------------- Extract contents with url -------------------------------#

def extract_url_content(url):
    """
    Extracts content from a URL's HTML structure, organized into sections, irrelevant_content, paragraphs, lists, figures, and tables.

    Args:
        url (str): The URL of the webpage to extract content from.

    Returns:
        list: A list containing two dictionaries: irrelevant_content (chapter title and non-section paragraphs) 
              and content_list (structured sections, headings, paragraphs, lists, figures, and tables).
    """
    
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main content section
    main_content = soup.find("div")

    if main_content is None:
        print("Unable to find the main content section")
        return

    # List to store the content
    content_list = []
    
    # Extract chapter title and non-section paragraphs
    irrelevant_content = {}
    head = soup.find('head')
    Titles = head.find_all('title')
    for title in Titles:
        if title:
            name = title.text.strip()
            irrelevant_content["Title"] = name

    body = soup.find('body')
    paras = []
    pp = body.find_all('p')
    for p in pp:
        paras.append(p.text.strip())

    # Find all the sections in the main content
    sections = main_content.find_all("section")

    # Set to store unique section identifiers
    section_identifiers = set()

    # Iterate over each section
    sec = []  # To generate a subset of paragraph data
    for section in sections:
        section_data = {}

        # Extract section identifier
        section_id = section.get("id")
        section_class = section.get("class")
        section_uuid_key = section.get("data-uuid-key")
        section_data_type = section.get("data-type")
        section_class_tuple = tuple(section_class) if section_class is not None else ()
        section_identifier = (section_id, section_class_tuple, section_uuid_key, section_data_type)

        # Skip if section identifier is already encountered
        if section_identifier in section_identifiers:
            continue

        # Add section identifier to the set
        section_identifiers.add(section_identifier)

        # Extract section title
        # ------------------------
        subtitle = soup.find(['h3', 'h4', 'h2', 'h1'])
        title = section.find(["h1", "h2", "h3", "h4", "h5"])
        if title:
            section_data["title"] = title.text.strip()
        else:
             section_data["title"] = subtitle.text.strip()

        # Extract section paragraphs
        paragraphs = section.find_all(["p", "span"])
        section_data["Section"] = []
        
        for paragraph in paragraphs:
            paragraph_text = paragraph.text.strip()
            if paragraph_text:
                section_data["Section"].append(paragraph_text)
                sec.append(paragraph_text)

        # Extract list items
        lists = section.find_all("ul")
        section_data["lists"] = []
        for ul in lists:
            list_items = ul.find_all("li")
            section_data["lists"].append([li.text.strip() for li in list_items])

        # Extract figures and image links
        figures = section.find_all("div", {"class": "os-figure"})
        section_data["figures"] = []
        for figure in figures:
            figure_data = {}
            img = figure.find("img")
           
            if img and "src" in img.attrs:
                image_url = urljoin(url, img["src"])
                figure_data["image"] = image_url

            caption = figure.find("figcaption")
            if caption:
                figure_data["caption"] = caption.text
            
            section_data["figures"].append(figure_data)

        # Extract tables
        tables = section.find_all("table")
        section_data["tables"] = []
        for table in tables:
            table_data = []
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                table_data.append([cell.text.strip() for cell in cells])
            section_data["tables"].append(table_data)

        content_list.append(section_data)

  # Extract only paragraphs that are not in the sections structure
    irrelevant_content["Paragraphs_Not_in_Sections"] = remove_items(paras, sec)

    return [irrelevant_content, content_list]  


#----- Iterate and extract different pages, by URL, in the textbook and save as one file --------------#



def extract_textbook(url_list, textbook_name):
    """
    Extracts and structures content from a list of URLs into a JSON file.

    Args:
        url_list (list): List of URLs containing the textbook content.
        textbook_name (str): Name of the textbook for JSON file naming.

    Returns:
        content_list: A list of dictionaries, containing structured content data.
    """
    content_list = []  # List to store the structured content
    page_data = {}  # Dictionary to store content per page
    pages = 0  # Page counter
    
    # Iterate through the list of URLs
    for url in url_list:
        # Extract content from the URL using a helper function (extract_url_content)
        page_content = extract_url_content(url)
        
        # The page_content is a list with two items:
        # 1. irrelevant_content (not used in this context)
        # 2. content_list (well-structured sections needed)
        # We access content_list using indexing [1] to remove paragraphs not in sections since it is not needed for the training dataset.
        
        page_data['Page ' + str(pages)] = page_content[1]
        pages += 1
    
    content_list.append(page_data)  # Append structured content to the list
    
    # Get the current working directory and create the file path for JSON
    script_dir = os.getcwd()
    json_path = os.path.join(script_dir, f"{textbook_name}.json")
    
    # Save the structured content as JSON
    with open(json_path, "w") as file:
        json.dump(content_list, file, indent=4)
    
    return content_list

