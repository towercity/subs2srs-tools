# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
import urllib.request as request
import json

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="

config = mw.addonManager.getConfig(__name__)

def search_jisho(word): 
    url = "%s%s" % (JISHO_API, word)
    return json.loads(request.urlopen(url).read())

def change_decks():
    change_tag = config['tags']['change']
    change_notes = mw.col.findNotes('note:subs2srs tag:%s' % change_tag) #saves a list of note IDs
    showInfo("found %s cards tagged '%s'" % (len(change_notes), change_tag))
    test = search_jisho('red')
    showInfo(str(test['meta']['status']))


# add menu item to menu   
action = QAction("Change Decks", mw)
action.triggered.connect(change_decks)
mw.form.menuTools.addAction(action)