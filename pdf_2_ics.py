# -*- coding: utf-8 -*-
'''
This script retrieves links to PDF and DOCX files from a specified URL, extracts text content from these files, 
and generates ICS (iCalendar) files based on the extracted text. The script is designed to process school menu 
documents and convert them into calendar events.
Functions:
    get_all_links(url):
    get_unique(url, links):
    get_all_pdfs(url, links):
    get_all_docs(url, links):
    url_to_text(url):
    is_valid_date(date_string, language):
        Checks if the input string is a valid date in the format "Month Day".
    parse_date_string(date_string, language):
    add_emojis(next_line, language, wnl):
    text_to_ics(text, event_title, language, day_language):
    to_file(ics_string, filename):
    generate_ics(pdf_filename, level, language, day_language, meal):
    parse_filename(filename):
Main Execution:
    The script retrieves links from a specified URL, processes DOCX and PDF files to extract text content, 
    and generates ICS files based on the extracted text. The generated ICS files contain calendar events 
    for school menus, with event titles and descriptions based on the content of the documents.
'''
import re
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urljoin
from urllib.request import urlopen
import json
import emoji
import ics
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from pypdf import PdfReader
import docx


def get_all_links(url):
    """
    Extracts all links containing "amazonaws.com" from a JSON object embedded 
    within a script tag of type 'application/json' in the HTML content of a given URL.
    Args:
        url (str): The URL of the webpage to scrape for links.
    Returns:
        list: A list of strings containing links that include "amazonaws.com".
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        requests.exceptions.HTTPError: If the HTTP response contains an error status code.
        AttributeError: If the expected script tag or JSON content is not found.
        json.JSONDecodeError: If the JSON content cannot be parsed.
    """
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    response.raise_for_status()
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    # Find script tag with type 'application/json'
    script_tag = soup.find('script', type='application/json')
    # Get script tag content
    json_string = script_tag.string
    # Load JSON data
    data = json.loads(json_string)
    # Extract links from the JSON data list
    links = [a for a in data if type(a) == str and "uploaded_file" in a]
    return links


def get_unique(url, links):
    """
    Generates a list of unique URLs from the given base URL and list of links.
    This function filters the provided list of links to include only those that
    end with ".pdf" or ".docs", then joins each link with the base URL and 
    returns a list of unique URLs.
    Args:
        url (str): The base URL to join with each link.
        links (list): A list of link strings to be filtered and joined with the base URL.
    Returns:
        list: A list of unique URLs that end with ".pdf" or ".docx".
    """
    unique_links = list(
        set([urljoin(url, file) for file in links if (file.endswith(".pdf") or file.endswith(".docx"))])
    )
    return unique_links


def get_all_pdfs(url, links):
    """
    Extracts and returns a list of unique PDF URLs from a list of links.
    Args:
        url (str): The base URL to join with the PDF file links.
        links (list): A list of file links to filter and join with the base URL.
    Returns:
        list: A list of unique PDF URLs.
    """
    pdfs = list(
        set([urljoin(url, file) for file in links if ".pdf" in file])
    )
    return pdfs


def get_all_docs(url, links):
    """
    Retrieves all unique .docx document URLs from a list of links.

    Args:
        url (str): The base URL to join with the document links.
        links (list): A list of links to filter and join with the base URL.

    Returns:
        list: A list of unique .docx document URLs.
    """
    docs = list(
        set([file for file in links if ".docx" in file])
    )
    return docs


def url_to_text(url):
    """
    Extracts text content from a given URL pointing to a PDF or DOCX file.

    Args:
        url (str): The URL of the file to extract text from. The URL should end with either ".pdf" or ".docx".

    Returns:
        str: The extracted text content from the file. Returns None if the URL does not end with ".pdf" or ".docx".
    """
    if url.endswith(".pdf"):
        remote_file = urlopen(url).read()
        memory_file = BytesIO(remote_file)
        reader = PdfReader(memory_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif url.endswith(".docx"):
        response = requests.get(url)
        doc = docx.Document(BytesIO(response.content))
        text = ''
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + '\n'
        return text
    else:
        return None


def is_valid_date(date_string, language):
    """
    Checks if the input string is a valid date in the format "Month Day"
    where the month is a word (e.g., January, February) and the day is a number.

    Args:
        date_string (str): The date string to validate.
        language (str): The language of the date string.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    return parse_date_string(date_string, language) is not None


def parse_date_string(date_string, language):
    """
    Parses a date string into year, month, and day.
    Args:
        date_string (str): The date string to parse. It should be in the format "Month Day" 
                           where "Month" is the full name of the month and "Day" is the day of the month.
                           Example: "January 15" or "Enero 15".
        language (str): The language of the date string. Supported values are "es" for Spanish and "en" for English.
    Returns:
        tuple: A tuple containing the year (int), month (int), and day (int) if the date string is successfully parsed.
               Returns None if the date string does not match the expected format or if the language is not supported.
    Raises:
        None
    """
    if language == "es":
        pattern = r"^(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+(\d{1,2})$"
    else:
        pattern = r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})$"
    match = re.match(pattern, date_string)
    if not match:
        return None
    month_name = match.group(1)
    day = int(match.group(2))

    year = datetime.now().year
    if language == "es":
        # list of month names
        month_names = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        month = month_names.index(month_name) + 1
    elif language == "en":
        month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        month = month_names.index(month_name) + 1
    else:
        return None
    return year, month, day


def add_emojis(next_line, language, wnl):
    """
    Adds emojis to the given text based on the specified language.

    Args:
        next_line (str): The input string to which emojis will be added.
        language (str): The language code for emoji conversion ('es' for Spanish, 'en' for English).
        wnl (WordNetLemmatizer): An instance of WordNetLemmatizer for lemmatizing words in the input string.

    Returns:
        str: The input string with emojis added, or None if the language is not supported.
    """
    next_line_no_colons: str = re.sub(r":", r"", next_line)
    next_line_no_colons_low = next_line_no_colons.lower()
    lemmatized_string = " ".join(
        [wnl.lemmatize(words) for words in next_line_no_colons_low.split()]
    )
    with_colons: str = re.sub(r"(\w*)", r":\1:", lemmatized_string)
    if language == "es":
        with_emojis: str = emoji.emojize(string=with_colons, language=language)
    elif language == "en":
        with_emojis: str = emoji.emojize(string=with_colons, language="alias")
    else:
        return None
    only_emoji: str = "".join([c for c in with_emojis if c in emoji.EMOJI_DATA])
    return next_line_no_colons + only_emoji


def text_to_ics(text, event_title, language, day_language):
    """
    Converts a given text into an ICS calendar format.
    Args:
        text (str): The input text containing event details.
        event_title (str): The title of the event.
        language (str): The language used for processing text.
        day_language (str): The language used for parsing dates.
    Returns:
        ics.Calendar: A calendar object containing the parsed events.
    Notes:
        - The function splits the input text into lines and processes each line to identify valid dates.
        - For each valid date, an event is created with the specified title and date.
        - The description of the event is built from subsequent lines until another valid date or specific keywords are encountered.
        - The event is marked as an all-day event and additional properties are set.
    """
    # Create WordNetLemmatizer object
    wnl = WordNetLemmatizer()

    calendar = ics.Calendar()
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not is_valid_date(line.strip(), day_language):
            i += 1
            continue
        date_parts = parse_date_string(line.strip(), day_language)
        year, month, day = date_parts
        event = ics.Event()
        event.name = event_title
        event.begin = datetime(year, month, day, tzinfo=timezone.utc)  # set begin time
        event.make_all_day()
        extra_content = ics.utils.ContentLine(name="TRANSP", value="TRANSPARENT")
        event.extra.append(extra_content)
        # build description until you reach next date
        event.description = ""
        while (
            i + 1 < len(lines)
            and not is_valid_date(lines[i + 1].strip(), day_language)
            and "Prices" not in lines[i + 1]
            and "Precios" not in lines[i + 1]
            and "ambios" not in lines[i + 1]
            and "change" not in lines[i + 1]
        ):
            next_line = lines[i + 1].strip()
            line = add_emojis(next_line, language, wnl)
            event.description += line + "\n"
            i += 1
        calendar.events.add(event)
    return calendar


def to_file(ics_string, filename):
    """
    Save the given ICS string to a file with the specified filename.

    Args:
        ics_string (str): The ICS string content to be saved.
        filename (str): The name of the file where the ICS string will be saved.

    Returns:
        None
    """
    if ics_string:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            f.write(ics_string)


def generate_ics(filename, level, language, day_language, meal):
    """
    Generates an ICS (iCalendar) file from a PDF menu.
    Args:
        filename (str): The filename of the file to be converted.
        level (str): The school level (e.g., 'k12', 'elementary', 'middle', 'high', 'bic', 'prek').
        language (str): The language of the menu ('en' for English, 'es' for Spanish).
        day_language (str): The language of the day names in the calendar.
        meal (str): The type of meal (e.g., 'breakfast', 'lunch', 'afterschoolsnack', 'snack').
    Returns:
        bool: True if the ICS file was generated successfully, False otherwise.
    """
    meal_terms_en = {
        "breakfast": "Breakfast",
        "lunch": "Lunch",
        "afterschoolsnack": "Afterschool Snack",
        "snack": "Snack",
    }
    meal_terms_es = {
        "breakfast": "Desayuno",
        "lunch": "Almuerzo",
        "afterschoolsnack": "Meriendas Después de Clases",
        "snack": "Merienda En la Escuela",
    }

    level_terms_en = {
        "k12": "K12",
        "elementary": "Elementary",
        "middle": "Middle",
        "high": "High",
        "bic": "Breakfast in Classroom",
        "prek": "PreK",
    }
    level_terms_es = {
        "k12": "K12",
        "elementary": "Elemental",
        "middle": "Intermedia",
        "high": "Secundaria",
        "bic": "Desayuno en el Aula",
        "prek": "PreK",
    }

    if "en" in language:
        event_title = f"DPS - {level_terms_en[level]} School {meal_terms_en[meal]} Menu"  # All events in the calendar will have this title
        outfile = f"english_{level}_{meal}.ics"
    elif "es" in language:
        event_title = f"DPS - Menú {meal_terms_es[meal]} Escuela {level_terms_es[level]}"  # All events in the calendar will have this title
        outfile = f"spanish_{level}_{meal}.ics"
    else:
        return False
    link = filename.replace(" ", "%20")
    link = link.replace("?disposition=inline", "")
    # print(link)
    text = url_to_text(link)
    # print(text)
    cal = text_to_ics(text, event_title, language, day_language)
    ics_string = cal.serialize()
    # print(ics_string)
    to_file(ics_string, outfile)
    print(outfile)
    return True


def parse_filename(filename):
    """
    Parses the given filename to extract information about the level, language, and meal type.
    Args:
        filename (str): The name of the file to be parsed.
    Returns:
        tuple: A tuple containing three elements:
            - level (str): The educational level, which can be one of the following:
                - "k12"
                - "elementary"
                - "middle"
                - "high"
                - "bic"
                - "prek"
            - language (str): The language of the file, either "es" (Spanish) or "en" (English).
            - meal (str): The type of meal, which can be one of the following:
                - "breakfast"
                - "lunch"
                - "afterschoolsnack"
                - "snack"
    Returns False if the filename does not contain the required information or contains "Carb" or "Achievement".
    """
    if "Carb" in filename:
        return False
    if "Achievement" in filename:
        return False

    if "Spanish" in filename:
        language = "es"
    else:
        language = "en"
    
    if "K12" in filename:
        level = "k12"
    elif "K-12" in filename:
        level = "k12"
    elif "ES" in filename:
        level = "elementary"
    elif "Elementary" in filename:
        level = "elementary"
    elif "MS" in filename:
        level = "middle"
    elif "Middle" in filename:
        level = "middle"
    elif "HS" in filename:
        level = "high"
    elif "High" in filename:
        level = "high"
    elif "BIC" in filename:
        level = "bic"
    elif "Classroom" in filename:
        level = "bic"
    elif "After" in filename:
        level = "k12"
    elif "Aula" in filename:
        level = "bic"
    elif "PreK" in filename:
        level = "prek"
    elif "Pre-K" in filename:
        level = "prek"
    elif "Prek" in filename:
        level = "prek"
    elif "Breakfast" in filename:
        level = "k12"
    else:
        return False

    if "Breakfast" in filename:
        meal = "breakfast"
    elif "Desayunos" in filename:
        meal = "breakfast"
        language = "es"
    elif "Lunch" in filename:
        meal = "lunch"
    elif "Almuerzo" in filename:
        meal = "lunch"
        language = "es"
    elif "ASSP" in filename:
        meal = "afterschoolsnack"
        language = "en"
    elif "After" in filename:
        meal = "afterschoolsnack"
    elif "Despu" in filename:
        meal = "afterschoolsnack"
        language = "es"
    elif "Snack" in filename:
        meal = "snack"
    elif "Meriendas" in filename:
        meal = "snack"
        language = "es"
    else:
        return False

    if "Spanish" in filename:
        language = "es"

    return (level, language, meal)


if __name__ == "__main__":
    # Spanish menus
    url = "https://www.dpsnc.net/documents/departments/school-nutrition-services/menus/men%C3%BAs-2025-2026---spanish/march-2026/25822543"
    links = get_all_links(url)

    # load the old links to avoid processing the same link twice
    with open("old_links.json", "r") as f:
        old_links = json.load(f)

    new_links = [link for link in links if link not in old_links]
    # do not process the same link twice
    if new_links:
        docs = get_all_docs(url, new_links)
        for filename in docs:
            params = parse_filename(filename)
            if params:
                print(filename)
                (level, language, meal) = params
                generate_ics(filename, level, language, language, meal)

        # This code was to fix a menu with a mix of languages
        # Most content was in Spanish, but the days were labeled in English
        '''
        doc_filename = docs[1]
        print(doc_filename)
        (level, language, meal) = parse_filename(doc_filename)
        print(level, language, meal)
        generate_ics(doc_filename, level, language, 'en', meal)
        '''

        pdfs = get_all_pdfs(url, new_links)
        for filename in pdfs:
            params = parse_filename(filename)
            if params:
                print(filename)
                (level, language, meal) = params
                generate_ics(filename, level, language, language, meal)

        old_links.extend(new_links)
        with open("old_links.json", "w") as f:
            json.dump(old_links, f)
    else:
        print('No new links to process')

    # English menus
    url = "https://www.dpsnc.net/documents/departments/school-nutrition-services/menus/2025-2026-menus---english/march-2026/25821405"

    links = get_all_links(url)

    # load the old links to avoid processing the same link twice
    with open("old_links.json", "r") as f:
        old_links = json.load(f)

    new_links = [link for link in links if link not in old_links]
    # do not process the same link twice
    if new_links:
        docs = get_all_docs(url, new_links)
        for filename in docs:
            params = parse_filename(filename)
            if params:
                print(filename)
                (level, language, meal) = params
                generate_ics(filename, level, language, language, meal)

        pdfs = get_all_pdfs(url, new_links)
        for filename in pdfs:
            params = parse_filename(filename)
            if params:
                print(filename)
                (level, language, meal) = params
                generate_ics(filename, level, language, language, meal)

        old_links.extend(new_links)
        with open("old_links.json", "w") as f:
            json.dump(old_links, f)
    else:
        print('No new links to process')
