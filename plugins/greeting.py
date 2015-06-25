from cloudbot import hook
import random
import re

GREETINGS = ["Hallo", "Hello", "Hai", "Whoop", "Herro", "Yoyoyo", "WB", "Welcome back", "Hi", "Hellow", "Hey"]
JOINED_RE = re.compile(r"(\w+) joined the game\.", re.IGNORECASE)
GREETING_RE = re.compile(r"(?:{}) R2D2".format("|".join(GREETINGS)), re.IGNORECASE)
print(r"^.*(?:{}) R2D2.*$".format("|".join(GREETINGS)))

@hook.regex(JOINED_RE)
def greet_joined(match):
    """Responds on greetings with a 3:1 chance"""
    if random.randint(0, 3) == 0:
        player = match.group(1)
        return "{greeting} {player}!".format(greeting=random.choice(GREETINGS), player=player)

@hook.regex(GREETING_RE)
def greet_response(match, nick):
    return "{greeting} {player}!".format(greeting=random.choice(GREETINGS), player=nick)
