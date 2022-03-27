# from Core import creds
from calendar import calendar
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

class GoogleCalendar:
    """
    Represents a small custom interface to the Google Calendar API
    """

    def CalendarInstance():
        """
        Creates a new GoogleCalendar instance with the supplied credentials
        """

        # Creates a new Google API request service
        try:
            creds = retrieve_credentials()
            service = build('calendar', 'v3', credentials=creds)

            """Request Debug
            # calendarRequest = service.calendars().get(calendarId=Google_CALENDAR_ID).execute()
            # try:
            #     print(calendarRequest)
            # except HttpError as e:
            #     print(e)
            """

            
            # print(datetime.now())
            
             # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId=Google_CALENDAR_ID, timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            

            try:
                if not events:
                    print('No upcoming events found.')
                    return

                # Prints the start and name of the next 10 events
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(start, event['summary'])
            except HttpError as error:
                print('An error occurred: %s' % error)

        except HttpError as error:
            # The API encountered a problem.
            print(error)
        
    try:
        CalendarInstance()
    except HttpError as error:
        print('GoogleCalendar Class: Exception Thrown, could not complete CalendarInstance\n')
        print(error)