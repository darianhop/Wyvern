# from Core import creds
from calendar import Calendar, calendar
from multiprocessing import Event
from discord.ext import tasks, commands
import discord
import googlesearch
from MemberHandler import Member_Handler
from Oauth import SCOPES, Google_CALENDAR_ID, retrieve_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date, datetime, timedelta
import asyncio
REMINDER_ID = 947286490973634640
"""
To renable eventshandler, uncomment "GoogleCalendar.init()" around line 24 in core.
"""
class GoogleCalendar:
    """
    Represents a small custom interface to the Google Calendar API
    """

    def init():
        GoogleCalendar.initializeCalendar.start()

    def unload(self):
        self.initializeCalendar.cancel()

    @tasks.loop(seconds = 20)
    async def initializeCalendar():
        await GoogleCalendar.CalendarInstance()
        
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
                    Google Calendar searching works only with UTC Time Zone
                    """

                    # Setting up time ranges for the calendar search with respect to UTC time zone.
                    now = datetime.utcnow()
                    deltaStartTime = timedelta(hours=1)
                    deltaEndTime = timedelta(hours=1,minutes=5)
                    startTime = (now+deltaStartTime).isoformat() + 'Z' # Z is UTC format
                    endTime = (now+deltaEndTime).isoformat() + 'Z' # Z is UTC format
                    now = now.isoformat() + 'Z' # Z is UTC format
                    
                    # Call the Calendar API (Searching Times need to be in UTC time, values for logic are defined later)
                    events_result = service.events().list(calendarId='rcl.talks@gmail.com', 
                                                        timeMin=startTime,
                                                        timeMax = endTime,
                                                        maxResults=10, singleEvents=True,
                                                        orderBy='startTime').execute()
                    events = events_result.get('items', [])
                    
                    
                    # Retrieving Events, if there are any
                    try:
                        if not events:
                            # print('\nNo upcoming events found.')
                            # print(now,' Current Time\n')
                            return
                        # Gather data on all of the events returned from the calendar search
                        for event in events:
                            start = event['start'].get('dateTime', event['start'].get('date'))
                            
                            """
                            These definitions below are:
                                 The Current Time in this time zone
                                 The Start of the Search Range in this time zone
                                 The End of the Search Range in this time zone
                            If the values used for the events results above are used it searches with respect to UTC time zone.
                            """
                            # Defining the Current Time and Search Range with respect to this time zone
                            timeZoneNowMath = datetime.now()
                            timeZoneStartMath = timedelta(hours=1)
                            timeZoneEndMath = timedelta(hours=1,minutes=5)
                            timeZoneStart = (timeZoneNowMath + timeZoneStartMath).isoformat()
                            timeZoneEnd = (timeZoneNowMath + timeZoneEndMath).isoformat()
                            
                        # Determining if any of the events returned are starting within the search range in this time zone
                        if start >= timeZoneStart and start <= timeZoneEnd:
                            print(timeZoneNowMath, 'current time')
                            print(start, event['summary'])
                            embed = discord.Embed(
                                title='*LB-130 Calenar',
                                color=discord.Colour(0x255c6),
                                description="Desc",
                            )
                            await discord.Guild.get_channel(Member_Handler,channel_id=REMINDER_ID).send(embed=embed)
                            """
                            await statement here
                            """
                        else:
                            return
                        
                        # If any events have been created, fetch them and create notification. 
                        # """
                        # (Currently Returns exception HttpError 400)
                        # """
                        # new_events_result = service.events().watch(calendarId='rcl.talks@gmail.com', 
                        #                                 timeMin=now,
                        #                                 # timeMax = endTime,
                        #                                 maxResults=10, singleEvents=True,
                        #                                 orderBy='startTime').execute()
                        # new_events = new_events_result.get('items', [])
                        # for event in new_events:
                        #     new_event_data = new_events['start'].get('dateTime', new_events['start'].get('date'))
                        #     print(new_event_data, new_events['summary'])


                    except HttpError as error:
                        print('An error occurred: %s' % error)
                        
                # async def createdEventsListener():
                #     """
                #     Returns the time and name of a newly created event in the calendar when it is created.                    
                #     """
                #     # Setting up time ranges
                #     now = datetime.utcnow()
                #     now = now.isoformat() + 'Z' # Z is UTC format

                #     # Call the Calendar API
                #     events_result = service.events().watch(calendarId=Google_CALENDAR_ID, 
                #                                         timeMin=now,
                #                                         # timeMax = endTime,
                #                                         maxResults=10, singleEvents=True,
                #                                         orderBy='startTime').execute()
                #     events = events_result.get('items', [])

                #     # Retrieving New Events, if there are any
                #     try:
                #         if not events:
                #             print(now,' Current Time')
                #             return
                #         # Prints the start and name of up to the next 10 events
                #         for event in events:
                #             start = event['start'].get('dateTime', event['start'].get('date'))
                #             print(start, event['summary']) #Commented out to not spam terminal

                #     except HttpError as error:
                #         print('An error occurred: %s' % error)

            except HttpError as error:
                # The API encountered a problem.
                print(error)
        
            # Waits 5 minutes and creates a taskS
            print('Events Call at timestamp')
            print(datetime.utcnow())
            await asyncio.sleep(30)
            asyncio.create_task(EventsListener())
            # asyncio.create_task(createdEventsListener())
    


    # def initEvents():
    #     GoogleCalendar.initializeNewEvents.start()

    # def unload(self):
    #     self.initializeNewEvents.cancel()

    # @tasks.loop(seconds = 20)
    # async def initializeNewEvents():
    #     await GoogleCalendar.newEventsInstance()
    
    # async def newEventsInstance():
    #     print('New Events Instance Function')

    #     while True:
    #         # Creates a new Google API request service
    #         try:
    #             creds = retrieve_credentials()
    #             service = build('calendar', 'v3', credentials=creds)

    #             async def newEventsListener():
    #                 # Setting up time ranges
    #                 now = datetime.utcnow()
    #                 now = now.isoformat() + 'Z' # Z is UTC format

    #                 # Call the Calendar API
    #                 events_result = service.events().watch(calendarId=Google_CALENDAR_ID, 
    #                                                     timeMin=now,
    #                                                     ).execute()
    #                 events = events_result.get('items', [])

    #                 # Retrieving New Events, if there are any
    #                 try:
    #                     if not events:
    #                         print(now,' Current Time')
    #                         return
    #                     # Prints the start and name of up to the next 10 events
    #                     for event in events:
    #                         start = event['start'].get('dateTime', event['start'].get('date'))
    #                         print(start, event['summary']) #Commented out to not spam terminal
    #                         print(now)

    #                 except HttpError as error:
    #                     print('An error occurred: %s' % error)

    #         except HttpError as error:
    #             # The API encountered a problem.
    #             print(error)
            
    #         # Waits 5 minutes and creates a task
    #         print('New Events Call at timestamp')
    #         asyncio.create_task(newEventsListener())
    #         await asyncio.sleep(10)