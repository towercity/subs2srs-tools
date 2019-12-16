test = mw.col.findNotes('note:subs2srs tag:00change')
for note in test:
	noteInfo = mw.col.getNote(note)
	for (name, value) in noteInfo.items():
		print("%s: %s" % (name, value))
	print("\n------\n")