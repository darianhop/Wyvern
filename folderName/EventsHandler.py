from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from folderName.Oauth import Google_CALENDAR_ID, retrieve_credentials
# from folderName.MemberHandler import REMINDER_CHANNEL_ID
from discord.ext import tasks
import discord
import asyncio
REMINDER_CHANNEL_ID = 947286490973634640
# REMINDER_CHANNEL_ID = 962178983078797390 # ERPL Temp
class GoogleCalendar(discord.Client):
    """
    Represents a small custom interface to the Google Calendar API
    """
    

    def init(guilds):
        GoogleCalendar.initializeCalendar.start(guilds)

    def unload(self):
        self.initializeCalendar.cancel()

    @tasks.loop(seconds = 20)
    async def initializeCalendar(guilds):
        await GoogleCalendar.CalendarInstance(guilds)
        
    async def CalendarInstance(guilds):
        """
        Creates a new GoogleCalendar instance with the supplied credentials
        """
        while True:
            # Creates a new Google API request service
            try:
                creds = retrieve_credentials()
                service = build('calendar', 'v3', credentials=creds)
            
                async def EventsListener(guilds):
                    """
                    Listening for events 1 hour to 1hr 5min from now, every 5 minutes.  Google Calendar searching works only with UTC Time Zone
                    """

                    # Setting up time ranges for the calendar search with respect to UTC time zone.
                    now = datetime.utcnow()
                    deltaStartTime = timedelta(hours=1)
                    deltaEndTime = timedelta(hours=1,minutes=5)
                    startTime = (now+deltaStartTime).isoformat() + 'Z' # Z is UTC format
                    endTime = (now+deltaEndTime).isoformat() + 'Z' # Z is UTC format
                    now = now.isoformat() + 'Z' # Z is UTC format
                    
                    # Call the Calendar API (Searching Times need to be in UTC time, values for logic are defined later)
                    events_result = service.events().list(calendarId=Google_CALENDAR_ID, 
                                                        timeMin=startTime,
                                                        timeMax = endTime,
                                                        maxResults=10, singleEvents=True,
                                                        orderBy='startTime').execute()
                    events = events_result.get('items', [])
                    
                    
                    # Retrieving Events, if there are any
                    try:
                        if not events:
                            return

                        # Gather data on all of the events returned from the calendar search
                        for event in events:
                            start = event['start'].get('dateTime', event['start'].get('date'))
                            end = event['end'].get('dateTime', event['end'].get('date'))
                            author = event['creator'].get('creator', event['creator'].get('email'))
                            calendar_name = event['organizer'].get('displayName')
                            try:
                                location = event['location'].get('location')
                            except:
                                location = 'undefined'
                            event_url = event['htmlLink']

                            """
                            These definitions below are:
                                 The Current Time in this time zone
                                 The Start of the Search Range in this time zone
                                 The End of the Search Range in this time zone
                            If the values used for the events results above are used it searches with respect to UTC time zone.
                            """
                            # Defining the Current Time and Search Range with respect to this time zone
                            timeZoneNowMath = datetime.now()
                            timeZoneStart = (timeZoneNowMath + deltaStartTime).isoformat()
                            timeZoneEnd = (timeZoneNowMath + deltaEndTime).isoformat()
                            
                            # Determining if any of the events returned are starting within the search range in this time zone
                            if start >= timeZoneStart and start <= timeZoneEnd:
                               
                                print(start, event['summary'])
                                embed = discord.Embed(
                                    name=event['summary'],
                                    title="Upcoming Event: "+event['summary'],
                                    url=event_url,
                                    color=discord.Colour(0x255c6),
                                )
                                embed.set_author(name= calendar_name)
                                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Google_Calendar_icon_%282015-2020%29.svg/246px-Google_Calendar_icon_%282015-2020%29.svg.png")

                                # Converts the Event time to a readable format
                                event_start_time = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")
                                event_end_time = datetime.strptime(end,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")

                                embed.add_field(name="Starts:", value= event_start_time, inline=True)
                                embed.add_field(name="Ends:", value= event_end_time, inline=True)
                                embed.add_field(name="Location:", value= location, inline=True)
                                embed.add_field(name="Author", value= author, inline=True)
                                await guilds.get_channel(channel_id=REMINDER_CHANNEL_ID).send(embed = embed)

                        else:
                            return
                        
                        # If any events have been created, fetch them and create notification. 
                        # """
                        # (Currently Returns exception HttpError 400)
                        # """
                        # new_events_result = service.events().watch(calendarId=Google_CALENDAR_ID, 
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
        
            # Waits 5 minutes and creates a task
            # print('Events Call at timestamp')
            # print(datetime.utcnow())
            await asyncio.sleep(300)
            asyncio.create_task(EventsListener(guilds))
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