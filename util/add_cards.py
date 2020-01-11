#anko imports
from aqt import mw
from aqt.utils import showInfo, getOnlyText, askUser

# local utilities
from .jisho import JishoHandler
from .change import change_decks

# load config files
config = mw.addonManager.getConfig(__name__)

# init jisho handler
jisho = JishoHandler()

# given a term and its part of speech, reduces the term to its root for simple unconjugated searching
def find_root(term, pos):
    term = list(term) # make a list for easy manipulations

    if pos == 'adjective' and term[len(term) - 1] == 'い': # method to find い adjectives
        term = term[:-1] # remove the last character of the word
    elif pos == 'verb':
        term = term[:-1]
        
    return ''.join(term)

# given a jisho response at a tag to add, puts the user-specified term into the database in one of three ways
def add_term(jisho_resp, tag):
    term = jisho.get_japanese_term(jisho_resp)

    # check if not already exists; if so, add and leave
    note_exists = mw.col.findNotes(f"Vocabulary:{term}")
    if note_exists:
        mw.col.tags.bulkAdd(note_exists, tag, True) #the actual adding logic for anki 
        return True

    # find root term then search for it
    term_root = find_root(term, jisho.get_pos(jisho_resp))
    subs2srs_notes = mw.col.findNotes(f"note:{config['models']['subs2srs']} {term_root}")

    if subs2srs_notes: #if it's found something....
        edit_notes = subs2srs_notes[0:1]
        note = mw.col.getNote(subs2srs_notes[0]) #only edit the first found note
        note.fields[5] = term #saves the term to the correct field in the model
        mw.col.tags.bulkAdd(edit_notes, config["tags"]["change"], True) #mark it to change 
        mw.col.tags.bulkAdd(edit_notes, tag, True) #add the new tag
        note.flush()
    else:
        # Set the model
        modelBasic = mw.col.models.byName(config["models"]["japanese"])
        mw.col.decks.current()['mid'] = modelBasic['id']

        # Get the deck
        deck = mw.col.decks.byName(config["decks"]["main"])

        # Instantiate the new note
        note = mw.col.newNote()
        note.model()['did'] = deck['id']

        # Add the fields
        note.fields[0] = term
        note.fields[1] = jisho.get_reading(jisho_resp)
        note.fields[3] = jisho.get_definition(jisho_resp) 

        # Set the tags (and add the new ones to the deck configuration
        note.tags = mw.col.tags.canonify(mw.col.tags.split(tag))
        m = note.model()
        m['tags'] = note.tags
        mw.col.models.save(m)

        # Add the note
        mw.col.addNote(note)

def add_cards(tag, new_terms=[]):
    vocab_archive = [] #keeps record of added cards

    if new_terms: # dated code; kept in for future bulk-add extention 
        (f"adding {len(new_terms)} new cards to {tag}")
        # add a call to the card add function to the new_terms here
        for term in new_terms:
            jisho_resp = jisho.get_term_one(term)
            if not jisho_resp:
                pass
            else: 
                add_term(jisho_resp, tag)
                vocab_archive.append(term)

    # loops to add new notes until user quits
    searching = True
    while searching:
        term = getOnlyText(f"Tag: {tag}\nEnter term: ") #asks for term via anki

        # exit condition --> if user hits cancel or enters q
        if term == 'q' or term == '':
            searching = False
            break

        # pull data from jisho        
        jisho_resp = jisho.get_term_one(term)
        if not jisho_resp:
            showInfo('No term found. Rerunning search')
        else:
            term = jisho.get_japanese_term(jisho_resp)

            add_note = askUser(f"Selected Term: {jisho.get_reading(jisho_resp)}\nPart of Speech: {jisho.get_pos(jisho_resp)}\nDefinition: {jisho.get_definition(jisho_resp)}\n\nAdd term?")

            if add_note == True:
                add_term(jisho_resp, tag) #the logic to add the cardo
                vocab_archive.append(term)            

    showInfo("Added %s notes:\n * %s" % (len(vocab_archive), '\n * '.join(vocab_archive)))
    change_decks()

    mw.col.save()

# wrapper function. prompts the user for tag then calls add function with it
def add_by_tag():
    tag = getOnlyText("Enter tag")
    add_cards(tag)