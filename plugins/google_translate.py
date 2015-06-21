from cloudbot import hook
import re

try:
    import goslate
    gs = goslate.Goslate()
except:
    goslate = None
    
cmdre = re.compile("(?:(?:from\s*(\w+)\s+)|(?:(?:in)?to?\s*(\w+)\s+)){0,2}(.*)")

def parselang(langstr):
    langstr = langstr.lower()
    for pair in gs.get_languages().iteritems():
        if langstr in (pair[0], pair[1], pair[1].lower()):
            return pair[0]
    return None

@hook.command
def translate(text):
    """translate [from <source language>] [into <target language>] <sentence> 
    -- translates <sentence> from source language (default autodetect) to target
    language (default English) using Google Translate"""
    if goslate is None:
        return "You need to install the goslate api to use this feature"

    inpmatch = cmdre.match(text)
    text = inpmatch.group(3)
    if inpmatch.group(1):
        slang = parselang(inpmatch.group(1))
    else:
        slang = gs.detect(text)
    if inpmatch.group(2):
        tlang = parselang(inpmatch.group(2))
    else:
        tlang = "en"

    try:
        result = gs.translate(text, tlang, slang)
        return u"{} means {} in {}".format(text, result, gs.get_languages()[slang])
    except goslate.Error as e:
        return "Error: " + str(e)
