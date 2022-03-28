# from Core import creds
from calendar import Calendar, calendar
from multiprocessing import Event

from cv2 import detail_MatchesInfo
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import asyncio

class GoogleCalendar:
    """
    Represents a small custom interface to the Google Calendar API
    """

    async def CalendarInstance():
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

           
            async def EventsListener():
                """
                Listening for events 1 hour to 1hr 5min from now, every 5 minutes
                """

                # Setting up time ranges
                now = datetime.utcnow()
                deltaStartTime = timedelta(hours=0)
                deltaEndTime = timedelta(hours=3,minutes=5)
                startTime = (now+deltaStartTime).isoformat() + 'Z'
                endTime = (now+deltaEndTime).isoformat() + 'Z'

                 # Call the Calendar API
                now = now.isoformat() + 'Z' # Z is UTC format
                
                events_result = service.events().list(calendarId=Google_CALENDAR_ID, timeMin=startTime,
                                                    timeMax = endTime,
                                                    maxResults=10, singleEvents=True,
                                                    orderBy='startTime').execute()
                events = events_result.get('items', [])
                
                # Retrieving Events, if there are any
                try:
                    if not events:
                        print('No upcoming events found.')
                        print(now,' Current Time')
                        return
                    # Prints the start and name of up to the next 10 events
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(start, event['summary']) #Commented out to not spam terminal

                except HttpError as error:
                    print('An error occurred: %s' % error)
                
                    
        except HttpError as error:
            # The API encountered a problem.
            print(error)
        # Waits 5 minutes and creates a task 
        await asyncio.sleep(10)
        asyncio.create_task(EventsListener())

    while True:
        try:
            asyncio.run(CalendarInstance())
        except HttpError as error:
            print('GoogleCalendar Class: Exception Thrown, could not complete CalendarInstance Function\n')
            print(error)
