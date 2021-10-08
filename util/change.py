# Anki imports
from aqt.utils import showInfo
from aqt.qt import *
from aqt import mw

# local dependencies
from .jisho import JishoHandler

# load config files
config = mw.addonManager.getConfig(__name__)

# jisho handler instance
jisho = JishoHandler()


# removes a tag from a list (function made for semantic purposes)
def strip_tags(tags, rem_tag):
    tags.remove(rem_tag)
    return tags


# creates a new note
# currently based on biased model
# TODO: make the model user-specified
def create_new_note(note, model, deck, tags):
    term = note.fields[5]  # pulls in the vocab term from the 'Note' field

    try:
        jisho_resp = jisho.get_term_one(term)  # pulls info from Jisho
    except:
        return

    new_note = {
        "deckName": deck,
        "modelName": model,
        "fields": {
            "Vocabulary": term,
            "Vocabulary-Reading": jisho.get_reading(jisho_resp),
            "Meaning": jisho.get_definition(jisho_resp),
            "Sentence-1": note.fields[0],
            "Sentence-1-Audio": note.fields[1],
            "Sentence-1-Image": note.fields[2],
            "Sentence-1-English": note.fields[3],
            "Sentence-1-Reading": note.fields[4],
        },
        "tags": strip_tags(note.tags, tags['change'])
    }

    return new_note


def send_to_anki(new_note):
    # Set the model
    try:
        modelBasic = mw.col.models.byName(new_note['modelName'])
    except:
        return
        
    mw.col.decks.current()['mid'] = modelBasic['id']

    # Get the deck
    deck = mw.col.decks.byName(new_note['deckName'])

    # Instantiate the new note
    note = mw.col.newNote()
    note.model()['did'] = deck['id']

    # Add the fields
    new_field = new_note['fields']
    note.fields[0] = new_field['Vocabulary']
    note.fields[1] = new_field['Vocabulary-Reading']
    note.fields[3] = new_field['Meaning']
    note.fields[7] = new_field['Sentence-1']
    note.fields[8] = new_field['Sentence-1-Reading']
    note.fields[10] = new_field['Sentence-1-English']
    note.fields[11] = new_field['Sentence-1-Audio']
    note.fields[12] = new_field['Sentence-1-Image']

    # Set the tags (and add the new ones to the deck configuration
    tags = " ".join(new_note["tags"])
    note.tags = mw.col.tags.canonify(mw.col.tags.split(tags))
    m = note.model()
    m['tags'] = note.tags
    mw.col.models.save(m)

    # Add the note
    mw.col.addNote(note)


def change_decks():
    # short names for config dictionaries
    tags = config['tags']
    models = config['models']
    decks = config['decks']

    # search the database for subs cards tagged to change
    noteIds = mw.col.findNotes("tag:%s" % tags['change'])

    # check for blank notes array; if empty, return False
    if not len(noteIds):
        return False

    new_notes = []  # blank array to hold new notes made below
    changed_notes = [] # blank array to track changed notes
    # create the notes
    for noteId in noteIds:
        note = mw.col.getNote(noteId)
        try:
            new_notes.append(
                create_new_note(note,
                                model=models['japanese'],
                                deck=decks['main'],
                                tags=tags))
        except:
            showInfo("skipped")
        else:
            changed_notes.append(noteId)

    for new_note in new_notes:
        send_to_anki(new_note)
        # pass

    mw.col.remNotes(changed_notes)

    mw.col.save()

    showInfo(f"{len(noteIds)} notes changed!")
