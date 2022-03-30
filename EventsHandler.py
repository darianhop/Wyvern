# from Core import creds
from calendar import Calendar, calendar
from multiprocessing import Event
from discord.ext import tasks, commands
from cv2 import detail_MatchesInfo
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import asyncio

class GoogleCalendar():
    """
    Represents a small custom interface to the Google Calendar API
    """

        
    # def init(self):
        
    #     self.initializeCalendar.start()

    # def unload(self):
    #     self.initializeCalendar.cancel()

    # @tasks.loop(minutes=5.0)
    # async def initializeCalendar(self):
    #     await self.CalendarInstance()
        
    async def CalendarInstance():
        """
        Creates a new GoogleCalendar instance with the supplied credentials
        """
        while True:
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
                    deltaStartTime = timedelta(hours=1)
                    deltaEndTime = timedelta(hours=1,minutes=5)
                    startTime = (now+deltaStartTime).isoformat() + 'Z' # Z is UTC format
                    endTime = (now+deltaEndTime).isoformat() + 'Z' # Z is UTC format
                    now = now.isoformat() + 'Z' # Z is UTC format
                    
                    # Call the Calendar API
                    events_result = service.events().list(calendarId=Google_CALENDAR_ID, 
                                                        timeMin=startTime,
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
            print('events') 
            await asyncio.sleep(1)
            asyncio.create_task(EventsListener())