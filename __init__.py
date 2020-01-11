from aqt.utils import showInfo, getOnlyText
# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *

from .util.change import change_decks
from .util.add_cards import add_by_tag

# add menu item to menu   
change = QAction("Change subs2srs cards", mw)
change.triggered.connect(change_decks)
change.setShortcut('c')
mw.form.menuTools.addAction(change)

add = QAction("Add Cards to Tag", mw)
add.triggered.connect(add_by_tag)
add.setShortcut('Shift+A')
mw.form.menuTools.addAction(add)