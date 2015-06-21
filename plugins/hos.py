from cloudbot import hook
from cloudbot.util import http

API_URL = "http://yeahwh.at/test/api/hos.php?user="

NOBANS = "\x037[\x034Hall of Shame\x037] No entries for \x035{}\x037 :)"
HASENTRIES = "\x037[\x034Hall of Shame\x037] {} entries for \x035{}\x037: {}"
ISBANNED = "\x037[\x034Hall of Shame\x037] \x035{}\x037 is currently banned"

@hook.command('shame', 'hallofshame', 'bans', 'hos')
def hos(text, reply):
    """hos <user> - This command will lookup our Hall of Shame"""
    if not text:
        return '\x038You need to pass a username! (example: \"!hos frdmn\")'
    else:
        data = http.get_json(API_URL + text)
        if not data["success"]:
            #~ if data["payload"]["error"] == "PLAYER_NOT_FOUND":
                #~ return NOBANS.format(text)
            #~ else:
                return data["payload"]["message"]
        
        total = data["payload"]["total"]
        shortlink = data["payload"]["shortlink"]
        if not total > 0:
            return NOBANS.format(text)
        else:
            reply(HASENTRIES.format(total, text, shortlink))
            detail = data["payload"]["detail"]
            if detail["bans"]:
                return ISBANNED.format(text)
