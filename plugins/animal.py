from cloudbot import hook
import random

ANIMALS = ("kitten", "dog", "cat", "puppy", "squirrel", "cow", "horse", "chiken", "goat", "shark", "whale", "fish", "monkey", "elephant", "frdmn")

@hook.command(autohelp=False)
def animal(text):
	"""Animal script by vladde, pluginified by Yepoleb"""
	animal = random.choice(ANIMALS)
	return "One " + animal + " has been killed thanks to you :D"
