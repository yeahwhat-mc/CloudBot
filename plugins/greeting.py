from cloudbot import hook
import random
import re

GREETING_RE = re.compile(r"(\w+) joined the game\.")
GREETINGS = ["Hallo", "Hello", "Hai", "Whoop", "Herro", "Yoyoyo", "WB", "Welcome back", "Hi", "Hellow", "Hey"]

@hook.regex(GREETING_RE)
def greet(inp):
    """Responds on greetings with a 3:1 chance"""
    if random.randint(0, 3) == 0:
        player = inp.group(1)
        return "{greeting} {player}!".format(greeting=random.choice(greetings), player=player)
