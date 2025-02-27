import datetime
from datetime import date, timedelta, timezone
import os
import os.path
import json
from ics import Calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def authenticate():
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
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)
    return service


def search_events_by_date(service, cal_id, date_str):
  """Searches for events on a given date.

  Args:
    service: The Google Calendar API service object.
    cal_id: The Google Calendar ID string
    date_str: The date to search for in 'YYYY-MM-DD' format.

  Returns:
    A list of events for the given date, or an empty list if no events are found.
  """
  date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
  start_of_day = datetime.datetime.combine(date_obj, datetime.time.min).isoformat() + 'Z'
  end_of_day = datetime.datetime.combine(date_obj, datetime.time.max).isoformat() + 'Z'

  events_result = service.events().list(calendarId=cal_id, timeMin=start_of_day,
                                        timeMax=end_of_day, singleEvents=True,
                                        orderBy='startTime').execute()
  events = events_result.get('items', [])
  return events


def iterate_cal(service, cal_id, filename, verbose):
    with open(filename,  encoding="utf-8") as file:
        content = file.read()
        # Process the content
        calendar = Calendar(content)
        for event in calendar.events:
            date_to_search = event.begin.strftime("%Y-%m-%d")
            # check for existing events on the date we are considering
            events_on_date = search_events_by_date(service, cal_id, date_to_search)
            if not events_on_date:
                if verbose:
                    print(f"No events found on {date_to_search}")
                new_event = {
                    'summary': event.name,
                    'description': event.description,
                    'start': {'date': date_to_search},
                    'end': {'date': event.end.strftime("%Y-%m-%d")}
                }
                # Uncomment these when we are ready to push to the cals
                new_event = service.events().insert(calendarId=cal_id, body=new_event).execute()
                if verbose:
                    print('Event created: %s' % (new_event.get('htmlLink')))
            else:
                if verbose:
                    print(f"Events on {date_to_search}:")
                    for event in events_on_date:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(f"{start} - {event['summary']}")

def test_date(service, cal_id, verbose):
    date_to_search = '2025-04-01'  # Replace with the desired date in 'YYYY-MM-DD' format
    enddate_to_search = '2025-04-02'  # Replace with the desired date in 'YYYY-MM-DD' format

    events_on_date = search_events_by_date(service, cal_id, date_to_search)

    if not events_on_date:
        if verbose:
            print(f"No events found on {date_to_search}")
        new_event = {
            'summary': "New Event!",
            'description': "New Event!",
            'start': {'date': date_to_search},
            'end': {'date': enddate_to_search},
        }
        if verbose:
            print(new_event)
        # Push to the cals
        new_event = service.events().insert(calendarId=cal_id, body=new_event).execute()
        if verbose:
            print('Event created: %s' % (new_event.get('htmlLink')))
    else:
        if verbose:
            print(f"Events on {date_to_search}:")
            for event in events_on_date:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"{start} - {event['summary']}")


if __name__ == '__main__':
    service = get_calendar_service()
    #cal_id = menu_ids[file_info.filename]
    #iterate_cal(service, 'english_elementary_lunch.ics', 'primary', True)
    test_date(service, 'primary', True)
