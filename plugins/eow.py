from cloudbot import hook
import datetime
import json
import pytz
import os

TIMEFORMAT = "%H:%M:%S"
TRAVELTIME = datetime.timedelta(hours=1)
TIMEZONE = pytz.timezone("Europe/Berlin")
NAME = "frdmn"

NOWORK = "\x033{} doesn't have to work today"
NOTSTARTED = "\x033{} hasn't started work. Probably sleeping!"
WILLSTOP = "\x033{} will stop working in {}"
TRAVELINGHOME = "\x033{} is on his way home"
TRAVELINGWORK = "\x033{} is on his way to work"
ATHOME = "\x033{} should already be at home"

parsedtimes = {}

@hook.on_start()
def load_times(bot):
    with open(os.path.join(bot.data_dir, "eow.json"), "r") as timef:
        timedata = json.load(timef)

    for day, times in timedata.items():
        daytimes = []
        for time in times:
            start, end = time.split("-")
            starttime = datetime.datetime.strptime(start, TIMEFORMAT).time()
            endtime = datetime.datetime.strptime(end, TIMEFORMAT).time()
            daytimes.append((starttime, endtime))
        parsedtimes[int(day)] = daytimes

def formattime(seconds):
    if seconds < 1:
        return "0 seconds"
    hours = seconds//3600
    minutes = seconds%3600//60
    seconds = seconds%60
    timelist = []
    if hours == 1:
        timelist.append("{} hour".format(hours))
    elif hours > 1:
        timelist.append("{} hours".format(hours))
    if minutes == 1:
        timelist.append("{} minute".format(minutes))
    elif minutes > 1:
        timelist.append("{} minutes".format(minutes))
    if seconds == 1:
        timelist.append("{} second".format(seconds))
    elif seconds > 1:
        timelist.append("{} seconds".format(seconds))
    
    return " ".join(timelist[:2]) # Drop the seconds if we have hours

@hook.command('eow', 'remaining', 'endofwork', 'beeroclock', 
    'remainingtimewhilefrdmnhastowork', 'meow', autohelp=False)
def endofwork(text):
    curdate = datetime.datetime.now(tz=pytz.utc).astimezone(TIMEZONE).replace(tzinfo=None)
    weekday = curdate.weekday()

    daytimes = parsedtimes[weekday]
    if not daytimes:
        return NOWORK.format(NAME)

    for timerange in daytimes:
        starttime = datetime.datetime.combine(curdate.date(), timerange[0])
        endtime = datetime.datetime.combine(curdate.date(), timerange[1])
        if starttime <= curdate < endtime:
            remaining = endtime - curdate
            return WILLSTOP.format(NAME, formattime(remaining.seconds))
        elif starttime - TRAVELTIME <= curdate < starttime:
            return TRAVELINGWORK.format(NAME)
        elif endtime + TRAVELTIME > curdate >= endtime:
            return TRAVELINGHOME.format(NAME)

    if all((curdate + TRAVELTIME).time() < timerange[0] for timerange in daytimes):
        return NOTSTARTED.format(NAME)
    else:
        return ATHOME.format(NAME)
