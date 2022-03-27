# from Core import creds
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import datetime


SCOPES


class GoogleCalendar:
    """
    Represents a small custom interface to the Google Calendar API
    """
    print('GoogleCalendar Class: is this thing on?\n')

    def CalendarInstance():
        """
        Creates a new GoogleCalendar instance with the supplied credentials
        """

        print('\tCalendarInstance online\n')

        # Creates a new Google API request service
        try:
            creds = retrieve_credentials()
            refreshToken = creds.refresh_token

            print('\t\tBuilding Service...\n')
            service = build('calendar', 'v3', creds)
            calendar = service.calendars().get(calendarId=Google_CALENDAR_ID)
            
            print('\t\tService Build Completed\n')
            
            # print('\t\t//Getting Values...//\n')
            # # Sets up the API request
            # print('\t\tSetting Up API Request...\n')
            # request = calendar
            # print('\t\tAPI Request Set Up\n')
            # # Executes the API request
            # print('\t\tExecuting API Request...\n')
            # result = request.execute()
            # print('\t\tAPI Request Executed\n')
            # # Extracts the values from the result
            # print('\t\tExtracting Values...\n')
            # values = result.get('values', [])
            # print('\t\tValues Extracted\n')

            # print('\t\t//Values Retrieved//\n')
            try:
                print(calendar['summary'])
            except:
                print('Could Not Retrieve Calendar Metadata')
            

            # print('\t\tCalling the Calendar API\n')
            
            # # Call the Calendar API
            # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            # print('Getting the next event')
            # events_results = service.events().list(calendarId='primary', timeMin=now,
            #                                        maxResults=1, singleEvents=True, orderBy='startTime').execute()

            # events = events_results.get('items', [])

            # print('\t\tAttempting if statement\n')

            # if not events:
            #     print('No upcoming events found.')
            #     return

            # print('\t\tAttempting For loop\n')

            # for event in events:
            #     start = event['start'].get(
            #         'dateTime', event['start'].get('date'))
            #     print(start, event['summary'])

        except HttpError as error:
            # The API encountered a problem.
            # print(error.content)
            print('error')

    try:
        print('\tTrying CalendarInstance...\n')
        CalendarInstance()
    except HttpError as error:
        print('GoogleCalendar Class: Exception Thrown, could not complete CalendarInstance\n')
        print(error.content)
        # self.creds = creds
        # # Creates a new Google API service request
        # service = build('calendar', 'v3', credentials=creds)

        # calendar = service.calendars().get(calendarId=Google_CALENDAR_ID).execute()
        # print(calendar['summary'])
