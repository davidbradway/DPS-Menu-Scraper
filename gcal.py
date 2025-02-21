import datetime
from datetime import date, timedelta, timezone
import zipfile
import os
import os.path
import json

from ics import Calendar

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def process_zip(zip_filepath):
  # We need a list of filenames and calendar IDs, load them.
  if os.path.exists("menu_ids.json"):
    with open("menu_ids.json") as f:
      menu_ids = json.load(f)

    """Opens a downloaded ZIP file and processes ICS files within."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build("calendar", "v3", credentials=creds)

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

    # For each file in the ZIP, iterate through the events and add them to the
    # calendar with the ID that matches from the menu_id.json lookup file
    with zipfile.ZipFile('calendars.zip', 'r') as zip_ref:
      for file_info in zip_ref.infolist():
        if file_info.filename in menu_ids and menu_ids[file_info.filename] != '':
          with zip_ref.open(file_info) as file:
            content = file.read().decode('utf-8') # Decode assuming UTF-8
            calendar = Calendar(content)
            for event in calendar.events:
              new_event = {
                'summary': event.name,
                'description': event.description,
                'start': {'date': event.begin.strftime("%Y-%m-%d")},
                'end': {'date': event.end.strftime("%Y-%m-%d")}
              }
              print(new_event)
              # Uncomment these when we are ready to push to the cals
              #new_event = service.events().insert(calendarId=menu_ids[file_info.filename], body=new_event).execute()
              #print('Event created: %s' % (new_event.get('htmlLink')))

if __name__ == "__main__":
  process_zip("calendars.zip")