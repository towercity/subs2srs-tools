# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *

from .util.change import change_decks

# add menu item to menu   
action = QAction("Change Decks", mw)
action.triggered.connect(change_decks)
mw.form.menuTools.addAction(action)
