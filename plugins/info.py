from cloudbot import hook
import re

NICK_RE = re.compile(r"^\[[^\]]+\]\[[^\]]+\](\w+):.*")
COLOR_RE = re.compile(r"\x03\d\d|\x02|\x0F|\x16|\x1F")

ADMINTEXT = "\x0311Hey {user}! Don't take me for an idiot, you know exactly "\
    "who i am..."
INFOTEXT = "\x0311Hey {user}! I'm {owner}'s bot. Take a look at {url} for a "\
    "list of commands."
PLOTTEXT = "\x038{}Search a free plot and talk to a \x0312staffmember\x038! "\
    "They will set it up for you! :)"
RULESTEXT = "\x038{}Type '/rules' and read thoroughly to get the "\
    "Builder-rank. Please note there are several pages!"
STAFFTEXT = "\x038{}If you decide to join our staffteam, read this: "\
    "http://wiki.yeahwh.at/Apply_for_Staff"
TRUSTEDTEXT = "\x038{}Be patient! Staff will promote you, when they think "\
    "its appropriate to do so. Protip: Asking just ruins chances!"
UNBANTEXT = "\x038{}To get unbanned the banned person must make an appeal in "\
    "the forums. Reading this might be helpful: \x0312http://s.frd.mn/VtPShK"

OWNER = "Yepoleb"
ADMINS = ["Yepoleb", "frdmn"]
HELPURL = "http://wiki.yeahwh.at/R2D2"


@hook.command('r2d2', 'bot', 'info', autohelp=False)
def info(text, reply, nick):
    """info - Posts information about the bot"""
    if nick in ADMINS:
        reply(ADMINTEXT.format(user=nick))
    else:
        reply(INFOTEXT.format(user=nick, owner=OWNER, url=HELPURL))

@hook.command('plot', 'plots', autohelp=False)
def plots(text, reply):
    """plot [playername] - Let new players know how to claim plots"""
    if text == "":
        player = ""
    else:
        player = "@" + text + ": "
    txt = PLOTTEXT.format(player)
    for line in txt.splitlines():
        reply(line)

@hook.command('rule', 'rules', autohelp=False)
def rules(text, reply):
    """rules [playername] - Let guests read the /rules"""
    if text == "":
        player = "@Guests: "
    else:
        player = "@" + text + ": "
    txt = RULESTEXT.format(player)
    for line in txt.splitlines():
        reply(line)

@hook.command('application', 'guard', 'mod', 'staffapp', autohelp=False)
def staffapp(text, reply):
    """staffapp [playername] - Use this command when someone want to apply as staff"""
    if text == "":
        player = ""
    else:
        player = "@" + text + ": "
    txt = STAFFTEXT.format(player)
    for line in txt.splitlines():
        reply(line)

@hook.command('trust', 'trusted', autohelp=False)
def trusted(text, reply):
    """trusted [playername] - When players ask for Trusted rank"""
    if text == "":
        player = ""
    else:
        player = "@" + text + ": "
    txt = TRUSTEDTEXT.format(player)
    for line in txt.splitlines():
        reply(line)

@hook.command('banappeal', 'appeal', 'unban', autohelp=False)
def unban(text, reply):
    """unban [playername] - This command shows how to get unbanned"""
    if text == "":
        player = ""
    else:
        player = "@" + text + ": "
    txt = UNBANTEXT.format(player)
    for line in txt.splitlines():
        reply(line)

@hook.command('help', autohelp=False)
def help(text):
    """help - Return a link to the bot's wiki page"""
    return "http://wiki.yeahwh.at/R2D2"
