import datetime
from datetime import date, timedelta
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next event from each calendar
  of a user in which "DPS" appears in the calendar name.
  """
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

  try:
    service = build("calendar", "v3", credentials=creds)

    # If we already saved the list of calendar IDs, load them.
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

    # Print the data (it will be stored as a Python dictionary)
    # iterating both key and values
    for key, value in cal_list.items():
      print(f"{key}: {value}")

      # replace this with the proper date from menu
      today = date.today()
      tomorrow = today + timedelta(days=1)
      tomorroww_format = tomorrow.strftime("%Y-%m-%d")

      new_event = {
        'summary': 'Test',
        'description': 'Delete me.',
        'start': {
          'date': tomorroww_format,
        },
        'end': {
          'date': tomorroww_format,
        },
      }
      new_event = service.events().insert(calendarId=value, body=new_event).execute()
      print('Event created: %s' % (new_event.get('htmlLink')))

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()