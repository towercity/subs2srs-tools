from aqt.utils import showInfo, getOnlyText
# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *

from .util.change import change_decks

# add menu item to menu   
change = QAction("Change Decks", mw)
change.triggered.connect(change_decks)
mw.form.menuTools.addAction(change)

def test_ask():
    vari = getOnlyText('enter text')
    showInfo(vari)

add = QAction("test", mw)
add.triggered.connect(test_ask)
mw.form.menuTools.addAction(add)
