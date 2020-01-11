# subs2srs Vocab Tools

Download here: https://ankiweb.net/shared/info/390779156

A simple Anki 2.1+ addon that eases the process of making Japanese vocab study cards from subs2srs cards. It has two major functions:

## 1. Change subs2srs cards

Keyboard shortcut: `c`

Transforms subs2srs cards into Japanese vocab study cards. To use: 

1. Copy the new term you'd like to make a card for into the Note field of your subs2srs card
2. tag the card with the change tag you've set in your the addon config (defaults to 00change)
3. Select `Change subs2srs cards` in the tools menu, or simply press 'c' on the main screen.

## 2. Add to tag

Adds new vocabulary study cards to a specified tag.

The main function of this addon. Lets you search jisho for the meanings of Japanese terms and add them to your Anki database.

In essence, this is an all-in-one reading practice app, stripped to its barest bits. You select a tag you'd like to add cards to -- I use the name of whatever game/book/article I'm reading here, for easy filtered decks later -- then this addon will continually prompt you for new words to search the meanings of, until you tell it to quit, that is. It will display the word you've searched with its definition, then prompt if you'd like to add the card to your Anki database or not.

If a note already exists, it will add the tag you've selected to the note than continue the loop. If the card doesn't exist, it will then search your subs2srs cards for any notes that uses the term (with some very basic conjugation allowances), add the tag you've selected to the card, convert the card to a standard Vocabulary card, then continue the loop. Finally, if none of these methods find any notes, the script will create a new card for the term with the tag you've chosen. 

To quit searching, either enter cancel the next new term prompt, or enter `q` in the input blank.
