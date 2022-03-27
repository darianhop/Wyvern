# from Core import creds
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError
import datetime





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
            
            print('\t\tBuilding Service...\n')
            service = build('calendar', 'v3', credentials=creds)
            calendarRequest = service.calendars().get(calendarId=Google_CALENDAR_ID).execute()
            print('\t\tRequest Executed\n')
            try:
                print('\t\t\tPrinting Request...\n')
                print(calendarRequest)
                print('\t\t\tRequest Printed\n')
            except HttpError as e:
                print(e)

        except HttpError as error:
            # The API encountered a problem.
            print(error)
            

    try:
        print('\tTrying CalendarInstance...\n')
        CalendarInstance()
    except HttpError as error:
        print('GoogleCalendar Class: Exception Thrown, could not complete CalendarInstance\n')
        print(error.content)