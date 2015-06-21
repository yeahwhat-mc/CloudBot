from cloudbot import hook
import re

NICK_RE = re.compile(r"^\[[^\]]+\](\w+):.*")
COLOR_RE = re.compile(r"\x03\d\d|\x02|\x0F|\x16|\x1F")

@hook.sieve
def minecraftnick(bot, event, plugin):
    if event.nick == "YEAHCHAT":
        nocolor = COLOR_RE.sub("", event.content)
        match = NICK_RE.search(nocolor)
        if match is not None:
            realnick = match.group(1)
            event.nick = realnick
    return event
