# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

config = mw.addonManager.getConfig(__name__)

def change_decks():
    change_tag = config['tags']['change']
    test = mw.col.findNotes('note:subs2srs tag:%s' % change_tag) #saves a list of note IDs
    showInfo("found %s cards tagged '%s'" % (len(test), change_tag))

# add menu item to menu   
action = QAction("Change Decks", mw)
action.triggered.connect(change_decks)
mw.form.menuTools.addAction(action)