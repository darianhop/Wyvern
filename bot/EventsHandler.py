from pickle import FALSE, TRUE
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone
from .Oauth import retrieve_credentials
# from .MemberHandler import REMINDER_CHANNEL_ID
from discord.ext import tasks
import discord
import asyncio

INTERNAL_CALENDAR_ID = 'mdt0cqfvv99lgtlo567jhv7tfk@group.calendar.google.com'
LAB_CALENDAR_ID = '19aahr89ga4qhhrj15vskbcfhk@group.calendar.google.com'

REMINDER_CHANNEL_ID = 947286490973634640
# REMINDER_CHANNEL_ID = 962178983078797390 # ERPL
class GoogleCalendar(discord.Client):
    """
    Represents a small custom interface to the Google Calendar API
    """
        
    async def CalendarInstance(guilds, upcoming = FALSE, created = TRUE):
        """
        Creates a new GoogleCalendar instance with the supplied credentials
        """

        try:
            # Creates a new Google API request service
            creds = retrieve_credentials()
            service = build('calendar', 'v3', credentials=creds)         

            async def EventsListener(guilds, service, calendar_id):
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
                events_result = service.events().list(calendarId=calendar_id, 
                                                    timeMin=startTime,
                                                    timeMax = endTime,
                                                    maxResults=10, singleEvents=True,
                                                    orderBy='startTime').execute()
                upcoming_Events = events_result.get('items', [])

                
                # Retrieving Upcoming Events, if there are any
                try:
                    if not upcoming_Events:
                        return

                    # Gather data on all of the events returned from the calendar search
                    for upcoming in upcoming_Events:
                        upcoming_start = upcoming['start'].get('dateTime', upcoming['start'].get('date'))
                        upcoming_end = upcoming['end'].get('dateTime', upcoming['end'].get('date'))
                        upcoming_author = upcoming['creator'].get('creator', upcoming['creator'].get('email'))
                        upcoming_calendar_name = upcoming['organizer'].get('displayName')
                        try:
                            upcoming_location = upcoming['location'].get('location')
                        except:
                            upcoming_location = 'undefined'
                        upcoming_event_url = upcoming['htmlLink']

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
                        if upcoming_start >= timeZoneStart and upcoming_start <= timeZoneEnd:
                            
                            print(upcoming_start, upcoming['summary'])
                            upcoming_embed = discord.Embed(
                                name=upcoming['summary'],
                                title="Upcoming Event: "+upcoming['summary'],
                                url=upcoming_event_url,
                                color=discord.Colour(0x255c6),
                            )
                            upcoming_embed.set_author(name= upcoming_calendar_name)
                            upcoming_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Google_Calendar_icon_%282015-2020%29.svg/246px-Google_Calendar_icon_%282015-2020%29.svg.png")

                            # Converts the Event time to a readable format
                            event_start_time = datetime.strptime(upcoming_start,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")
                            event_end_time = datetime.strptime(upcoming_end,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")

                            upcoming_embed.add_field(name="Starts:", value= event_start_time, inline=True)
                            upcoming_embed.add_field(name="Ends:", value= event_end_time, inline=True)
                            upcoming_embed.add_field(name="Location:", value= upcoming_location, inline=True)
                            upcoming_embed.add_field(name="Author", value= upcoming_author, inline=True)
                            await guilds.get_channel(channel_id=REMINDER_CHANNEL_ID).send(embed = upcoming_embed)

                    # Checks for events created in the last 5 minutes

                    now = datetime.now(timezone.utc).astimezone()
                    last = timedelta(minutes = 5)
                    lastUpdate = (now-last).astimezone().isoformat()
                    new_events_results = service.events().list(calendarId=calendar_id,
                                                        updatedMin = lastUpdate,
                                                        maxResults=10, singleEvents=True,
                                                        orderBy='startTime').execute()
                    created_Events = new_events_results.get('items', [])

                    try:
                        if not created_Events:
                            return # Break and donot continue if none exist

                        for created in created_Events:
                            created_start = created['start'].get('dateTime', created['start'].get('date'))
                            created_end = created['end'].get('dateTime', created['end'].get('date'))
                            created_author = created['creator'].get('creator', created['creator'].get('email'))
                            created_calendar_name = created['organizer'].get('displayName')
                            try:
                                created_location = created['location'].get('location')
                            except:
                                created_location = 'undefined'
                            created_event_url = created['htmlLink']

                            print(created_start, created['summary'])
                            created_embed = discord.Embed(
                                name=created['summary'],
                                title="New Event: "+created['summary'],
                                url=created_event_url,
                                color=discord.Colour(0x255c6),
                            )
                            created_embed.set_author(name= created_calendar_name)
                            created_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Google_Calendar_icon_%282015-2020%29.svg/246px-Google_Calendar_icon_%282015-2020%29.svg.png")

                            # Converts the Event time to a readable format
                            event_start_time = datetime.strptime(created_start,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")
                            event_end_time = datetime.strptime(created_end,"%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y, %H:%M:%S")

                            created_embed.add_field(name="Starts:", value= event_start_time, inline=True)
                            created_embed.add_field(name="Ends:", value= event_end_time, inline=True)
                            created_embed.add_field(name="Location:", value= created_location, inline=True)
                            created_embed.add_field(name="Author", value= created_author, inline=True)
                            await guilds.get_channel(channel_id=REMINDER_CHANNEL_ID).send(embed = created_embed)

                    except HttpError as error:
                        print('An error occurred sending a created project embed: %s' % error)

                
                except HttpError as error:
                    print('An error occurred sending a reminder embed: %s' % error)

                    
            await asyncio.gather(
                EventsListener(guilds, service, INTERNAL_CALENDAR_ID),
                EventsListener(guilds, service, LAB_CALENDAR_ID)
            )

        except HttpError as error:
            # The API encountered a problem.
            print(error)
    


    # Initializes the Calendar
    def init(guilds):
        GoogleCalendar.initializeCalendar.start(guilds)

    def unload(self):
        self.initializeCalendar.cancel()

    # Starts the Calendar Instance
    @tasks.loop(seconds = 30) #This time is the loop time
    async def initializeCalendar(guilds):
        try:
            await GoogleCalendar.CalendarInstance(guilds)
        
        except HttpError as e:
            print(f"An error has occured while running calendar coroutines,: \n{e}")
