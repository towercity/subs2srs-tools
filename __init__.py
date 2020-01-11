# Anki imports
from aqt.utils import showInfo, getOnlyText
from aqt import mw
from aqt.qt import *

# local functions import
from .util.change import change_decks
from .util.add_cards import add_by_tag

# add change function to menus   
change = QAction("Change subs2srs cards", mw)
change.triggered.connect(change_decks)
change.setShortcut('c')
mw.form.menuTools.addAction(change)

# add add function to menus
add = QAction("Add to tag", mw)
add.triggered.connect(add_by_tag)
add.setShortcut('Shift+A')
mw.form.menuTools.addAction(add)