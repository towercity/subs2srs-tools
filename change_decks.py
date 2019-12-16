# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def change_decks():
    card = mw.col.sched.getCard()
    note = card.note()
    string_list = ['due item:']
    for (name, value) in note.items():
        string_list.append("%s: %s" % (name, value))
    showInfo("\n".join(string_list))

# create a new menu item, "test"
action = QAction("Change Decks", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(change_decks)
# and add it to the tools menu
mw.form.menuTools.addAction(action)