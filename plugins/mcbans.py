from cloudbot import hook
from cloudbot.util import http
import re

BANSURL = "http://www.mcbans.com/player/{}/"
INFORE = re.compile("Showing (\d+) to (\d+) of (\d+) entries")
COLINDEX = ["type", "banid", "server", "mod", "reason", "date"]
    
def getbans(player):
    bs = http.get_soup(BANSURL.format(player))

    reputation = bs.find("label", attrs={"class":"one-third"}, text="Reputation").parent.div.get_text(strip=True)
    totalbans = bs.find("label", attrs={"class":"one-third"}, text="Bans").parent.div.get_text(strip=True)
    table = bs.find("td", text="Ban ID").parent.parent.parent
    rows = table.tbody.find_all("tr")
    banlist = []
    for row in rows:
        rowvals = {}
        columns = row.find_all("td")
        for i, column in enumerate(columns):
            val = column.get_text(strip=True)
            if val:
                rowvals[COLINDEX[i]] = val
        banlist.append(rowvals)
    return totalbans, reputation, banlist

@hook.command()
def mcbans(text, reply):
    """mcbans <user> -- Gets information on <user>s minecraft bans from mcbans"""
    user = text.strip()

    try:
        totalbans, reputation, banlist = getbans(user)
    except (http.HTTPError, http.URLError) as e:
        return "Could not fetch ban data from MCBans: {}".format(str(e))

    user_url = BANSURL.format(user)
    
    reply("The user \x02{user}\x02 has \x02{bans}\x02 ban(s) and a reputation of "\
        "\x02{rep}\x02. See detailed info at {url}".format(
        user=user, bans=totalbans, rep=reputation, url=user_url))
    for ban in banlist:
        reply("Ban ID: {banid}, Reason: {reason}, Server: {server}, "\
            "Date: {date}".format(banid=ban["banid"], reason=ban["reason"], 
                server=ban["server"], date=ban["date"]))
