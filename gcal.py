'''
This script interacts with the Google Calendar API to upload events from ICS files.
It supports both processing individual ICS files in a directory and processing ICS files within a ZIP archive.
Functions:
- authenticate(): Authenticates the user with Google OAuth2 and returns the credentials.
- get_calendar_service(): Returns the Google Calendar API service object.
- search_events_by_date(service, cal_id, date_str): Searches for events on a given date in a specified calendar.
- load_resources(): Loads the necessary resources such as calendar IDs and initializes the Google Calendar service.
- process_zip(menu_ids, service, zip_filepath): Processes ICS files within a ZIP archive and uploads events to Google Calendar.
- process_dir(menu_ids, service): Processes ICS files in the current directory and uploads events to Google Calendar.
Usage:
- Ensure you have 'credentials.json' for Google OAuth2 and 'menu_ids.json' for mapping filenames to calendar IDs.
- Run the script. It will either process a ZIP file named 'calendars.zip' or process individual ICS files in the current directory.
'''
import datetime
from datetime import date, timedelta, timezone
import zipfile
import os
import os.path
import json
import pytz

from ics import Calendar

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def authenticate():
    """
    Authenticates the user with Google API and returns the credentials.

    This function handles the OAuth2 authentication flow for accessing Google APIs.
    It checks for existing credentials in the 'token.json' file. If valid credentials
    are found, they are used. If the credentials are expired, they are refreshed.
    If no valid credentials are found, the user is prompted to log in via a local
    server.

    Returns:
        google.oauth2.credentials.Credentials: The authenticated user's credentials.

    Raises:
        google.auth.exceptions.GoogleAuthError: If there is an error during the authentication process.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when authorization flow completes
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(
                host='localhost',
                port=8088,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_calendar_service():
    """
    Authenticates and returns a Google Calendar service object.

    This function uses the `authenticate` function to obtain the necessary
    credentials and then builds a Google Calendar service object using the
    Google API client library.

    Returns:
        googleapiclient.discovery.Resource: A Google Calendar service object
        that can be used to interact with the Google Calendar API.
    """
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)
    return service


def search_events_by_date(service, cal_id, date_str):
    """
    Searches for events on a given date.

    Args:
        service: The Google Calendar API service object.
        cal_id: The Google Calendar ID string
        date_str: The date to search for in 'YYYY-MM-DD' format.

    Returns:
        A list of events for the given date, or an empty list if no events are found.
    """
    tz_UTC = pytz.timezone('UTC')
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    start_of_day = (datetime.datetime(date_obj.year, date_obj.month, date_obj.day, 00, 00, 00)
        ).astimezone(tz_UTC).isoformat().removesuffix("+00:00")+'Z'
    end_of_day = (datetime.datetime(date_obj.year, date_obj.month, date_obj.day, 23, 59, 59)
        ).astimezone(tz_UTC).isoformat().removesuffix("+00:00")+'Z'

    events_result = service.events().list(calendarId=cal_id, timeMin=start_of_day,
                                            timeMax=end_of_day, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def load_resources():
    """
    Load resources required for the application.
    This function performs the following tasks:
    1. Checks if the "menu_ids.json" file exists and loads it.
    2. Initializes the Google Calendar service.
    3. Checks if the "cal_list.json" file exists and loads it. If not, it fetches the list of calendar names and IDs from the Google Calendar API, filters them by those containing "DPS" in their summary, and saves the list to "cal_list.json".
    Returns:
        tuple: A tuple containing the loaded menu IDs and the Google Calendar service object if "menu_ids.json" exists.
        None: If "menu_ids.json" does not exist.
    """
    # We need a list of filenames and calendar IDs, load them.
    if os.path.exists("menu_ids.json"):
        with open("menu_ids.json") as f:
            menu_ids = json.load(f)

        service = get_calendar_service()

        # If we already saved the list of calendar IDs, load them.
        # cal_list isn't useful now, but might be helpful when I create
        # the next 12 calendars...
        if os.path.exists("cal_list.json"):
            # Open the JSON file
            with open("cal_list.json") as f:
                cal_list = json.load(f)
        else:
            # Call the Calendar API to get the list of calendar names and IDs
            page_token = None
            cal_list = {}
            while True:
                calendar_list = service.calendarList().list(pageToken=page_token).execute()
                for calendar_list_entry in calendar_list['items']:
                    print(f"{calendar_list_entry['id']} {calendar_list_entry['summary']}")
                    # Add to dictionary if contains "DPS"
                    if "DPS" in calendar_list_entry['summary']:
                        cal_list[calendar_list_entry['summary']] = calendar_list_entry['id']
                    page_token = calendar_list.get('nextPageToken')
                if not page_token:
                    break
            # Convert and write JSON object to file
            with open("cal_list.json", "w") as outfile:
                json.dump(cal_list, outfile)
        return (menu_ids, service)
    else:
        return None


def process_content(menu_ids, service, filename, content):
    """
    Processes the content of a calendar file and adds events to a Google Calendar.

    Args:
      menu_ids (dict): A dictionary mapping filenames to Google Calendar IDs.
      service (googleapiclient.discovery.Resource): The Google Calendar API service object.
      filename (str): The name of the file being processed.
      content (str): The content of the calendar file in iCalendar format.

    Returns:
      None
    """
    calendar = Calendar(content)
    for event in calendar.events:
        date_to_search = event.begin.strftime("%Y-%m-%d")
        # check for existing events on the date we are considering
        events_on_date = search_events_by_date(service, menu_ids[filename], date_to_search)
        new_event = {
            'summary': event.name,
            'description': event.description,
            'start': {'date': event.begin.strftime("%Y-%m-%d")},
            'end': {'date': event.end.strftime("%Y-%m-%d")}
        }
        if not events_on_date:
            # print(new_event)
            # Uncomment these when we are ready to push to the cals
            new_event = service.events().insert(calendarId=menu_ids[filename], body=new_event).execute()
            print('Event created: %s' % (new_event.get('htmlLink')))


def process_zip(menu_ids, service, zip_filepath):
    """
    Opens a downloaded ZIP file and processes ICS files within.
    Args:
        menu_ids (dict): A dictionary mapping filenames to calendar IDs.
        service (googleapiclient.discovery.Resource): The Google Calendar API service instance.
        zip_filepath (str): The file path to the ZIP file containing ICS files.
    Raises:
        zipfile.BadZipFile: If the ZIP file is corrupt or not a ZIP file.
        UnicodeDecodeError: If the ICS file content cannot be decoded as UTF-8.
    """
    # For each file in the ZIP, iterate through the events and add them to the
    # calendar with the ID that matches from the menu_id.json lookup file
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            filename = file_info.filename
            if filename in menu_ids and menu_ids[filename] != '':
                with zip_ref.open(file_info) as file:
                    content = file.read().decode('utf-8') # Decode assuming UTF-8
                    process_content(menu_ids, service, filename, content)


def process_dir(menu_ids, service):
    """
    Reads contents of the current directory and processes ICS files within.
    This function filters finds all files in the current directory that have a '.ics' extension.
    For each ICS file, it reads the file contents and calls a function to process the content.
    Args:
        menu_ids (dict): A dictionary where keys are filenames and values are Google Calendar IDs.
                Only files with non-empty calendar IDs are processed.
        service (googleapiclient.discovery.Resource): The Google Calendar API service instance used to interact with the calendar.
    Returns:
        None
    """
    dirlist = list(filter(lambda x: x.endswith('.ics'), os.listdir()))
    for filename in dirlist:
        if filename in menu_ids and menu_ids[filename] != '':
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                process_content(menu_ids, service, filename, content)


if __name__ == "__main__":
    (menu_ids, service) = load_resources()
    zip_filepath = "calendars.zip"
    if os.path.exists(zip_filepath):
        process_zip(menu_ids, service, zip_filepath)
    else:
        process_dir(menu_ids, service)
