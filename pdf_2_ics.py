# -*- coding: utf-8 -*-
import re
from datetime import datetime, timezone
from io import BytesIO
from urllib.parse import urljoin
from urllib.request import urlopen

import emoji
import ics
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from pypdf import PdfReader


def get_all_pdfs(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    response.raise_for_status()
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all anchor tags and extract the href attribute
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    pdf_files = list(
        set([urljoin(url, file) for file in links if file.endswith(".pdf")])
    )
    return pdf_files


def url_to_text(pdf_url):
    remote_file = urlopen(pdf_url).read()
    memory_file = BytesIO(remote_file)
    reader = PdfReader(memory_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def is_valid_date(date_string, language):
    """
    Checks if the input string is a valid date in the format "Month Day"
    where the month is a word (e.g., January, February) and the day is a number.
    """
    return parse_date_string(date_string, language) is not None


def parse_date_string(date_string, language):
    """Parses a date string into year, month, day."""
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


def text_to_ics(text, event_title, language):
    # Create WordNetLemmatizer object
    wnl = WordNetLemmatizer()

    calendar = ics.Calendar()
    lines = text.split("\n")
    # print(lines)
    i = 0
    while i < len(lines):
        line = lines[i]
        if not is_valid_date(line.strip(), language):
            i += 1
            continue
        date_parts = parse_date_string(line.strip(), language)
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
            and not is_valid_date(lines[i + 1].strip(), language)
            and "Prices" not in lines[i + 1]
            and "Precios" not in lines[i + 1]
            and "ambios" not in lines[i + 1]
            and "change" not in lines[i + 1]
        ):
            next_line = lines[i + 1].strip()
            line = add_emojis(next_line, language, wnl)
            # print(line)
            event.description += line + "\n"
            i += 1
        calendar.events.add(event)
    return calendar


def to_file(ics_string, filename):
    # Save to file:
    if ics_string:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            f.write(ics_string)


def generate_ics(pdf_filename, level, language, meal):
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
    link = pdf_filename.replace(" ", "%20")
    # print(link)
    text = url_to_text(link)
    # print(text)
    cal = text_to_ics(text, event_title, language)
    ics_string = cal.serialize()
    # print(ics_string)
    to_file(ics_string, outfile)
    return True


def parse_filename(filename):
    if "Carb" in filename:
        return False
    if "Achievement" in filename:
        return False

    if "K12" in filename:
        level = "k12"
    elif "ES" in filename:
        level = "elementary"
    elif "MS" in filename:
        level = "middle"
    elif "HS" in filename:
        level = "high"
    elif "BIC" in filename:
        level = "bic"
    elif "PreK" in filename:
        level = "prek"
    else:
        return False

    if "Spanish" in filename:
        language = "es"
    else:
        language = "en"

    if "Breakfast" in filename:
        meal = "breakfast"
    elif "Lunch" in filename:
        meal = "lunch"
    elif "ASSP" in filename:
        meal = "afterschoolsnack"
    elif "Snack" in filename:
        meal = "snack"
    else:
        return False
    return (level, language, meal)


pdf_files = get_all_pdfs("https://www.dpsnc.net/Page/7089")
for filename in pdf_files:
    params = parse_filename(filename)
    if params:
        (level, language, meal) = params
        generate_ics(filename, level, language, meal)
