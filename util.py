import traceback

lyricWidth = 70 #line width
chordWidth = 80 #line width

#pad out new lyrics and chords to a determined text width (using spaces)
def lyricFormatToStore(lyrics):
	#if too long, mka new line
	lyricContent = list() #list lines of lyrics, max lyricWidth chars per line
	curLyrics = ""

	lyrics = lyrics.rstrip();

	countChordRow = 0

	blankRowCount = 0 #regulate new lines

	for curLine in lyrics.split('\n'): #for every line
		if (len(curLine.strip()) == 0): #regulate extra newline creation
			blankRowCount += 1
		else:	
			blankRowCount = 0

		countChordRow += 1
		if ("..." not in curLine) and blankRowCount < 2: #discard truncated lines and extra new lines
			if len(curLine) > lyricWidth: #if line length is greater than lyricWidth
				tempLine = ""
				splitLine = curLine.split(' ')
				for word in splitLine: #for every word in this line
					if(len(word) >= lyricWidth): #if word is too long for its own line, truncate
						if (len(tempLine.strip()) != 0):
							lyricContent.append(pad(tempLine, lyricWidth)) #append what is already pending if nonzero length
							tempLine = "" #clear buffer
						tempTooLong = word[0] + word[1] + word[2] + "...[[LINE TRUNCATED - WILL BE DISCARDED AFTER NEXT EDIT]]"
						lyricContent.append(pad(tempTooLong, lyricWidth))
						break

					if ((len(tempLine) + len(word)) < lyricWidth): #if adding the next word still keeps the line length under lyricWidth, then add the next word to this line
						tempLine += word + " "
					else: #if adding the next word makes the line over lyricWidth chars long
						lyricContent.append(pad(tempLine, lyricWidth))
						tempLine = "" #clear buffer
						tempLine += word + " " #add to next line
						
				lyricContent.append(pad(tempLine, lyricWidth)) #add last word then add the line
				tempLine = "" #clear buffer	

			else: #if line length isnt greater than lyricWidth
				lyricContent.append(pad(curLine, lyricWidth, False))

	return("\n".join(lyricContent))

#pad all lines out to lyricWidth/chordWidth(for chords) chars to allow chord insertions where lyrics are not present
def pad(line, padLen, trimLeft = True):
	# if (len(line.strip()) == 0): #if its just whitespace
	# 	return("")
	if (len(line.strip()) == padLen):
		return(line.strip())
	if (trimLeft):
		line = line.strip()
	else: 
		line = line.rstrip()
	pad = padLen - len(line)
	line = (line + " " * pad)
	return(line)

#assemble lyrics from db data
def getPrettified_Lyrics(lyricContent):
	printSong = ""
	for line in lyricContent.split("\n"):
		printSong += pad(line, lyricWidth, False) + "\n"

	return printSong

#assemble chords from db data
def getPrettified_Chords(chordContent, linesCount, originalKey, desiredKey):
	try:
		# chords stored as list of data (below)
		# chordData = [position, key, chord] 

		# generate blank chord lines
		printChords = ((pad(" ", chordWidth, False) + "\n") * (linesCount+2)).split('\n') #one extra line to pad

		if chordContent == None or len(chordContent) == 0:
			return (pad(" ", chordWidth, False))

		expandedChordData = list() #stored as [row, col, chord]
		
		# first pass - decompress row/col from position
		for key, value in chordContent.iteritems():
			decompressedPos = decompressPosition(int(key))
			expandedChordData.append([decompressedPos[0], decompressedPos[1], value])

		# second pass to insert chords
		for chordDatum in expandedChordData:
			row = chordDatum[0]
			col = chordDatum[1]
			if (row < linesCount + 2):
				try:
					chord = str(getChordInKey(chordDatum[2], originalKey, desiredKey))
				except Exception, d:
					traceback.print_exc()
					chord = "invld0"

				#get line of interest
				cLine = printChords[row]
				
				#insert chord
				startIndex = getValidChordWindow(cLine, col, len(chord))
				if startIndex != -1:
					prepLine = cLine[:startIndex] + chord + cLine[(startIndex + len(chord)):]
					cLine = pad(prepLine, chordWidth, False) #make sure its padded
				else: #if invalid
					cLine = cLine[0:62] + "XX" #truncate and mark

				#reinsert line
				printChords[row] = cLine
		return '\n'.join(printChords)

  	except Exception, e:
		traceback.print_exc()
        return (pad(" ", chordWidth, False) * linesCount)

#find a valid starting index of window for new chord insert
def getValidChordWindow(line, start, wordSize): #returns starting position int of available window, -1 if cannot fit
	for i in range(start, start + wordSize):
		if validChordWindow(line, i, wordSize):
			return(i)
	return(-1)

#check if space is available in chord line for adding new chord
def validChordWindow(line, start, wordSize):
	for i in range(start, wordSize): #check there is enough space for a chord (whitespace)
		if i > len(line):
			break
		if not (line[i] == ' '): #check if its blank space
			return(False)
	return(True)

# decompress row, col from position value
def decompressPosition(position):
	row = int(position/(lyricWidth+1)) #plus 1 to account for \n character
	col = int(position) % (lyricWidth+1)
	# print "position: " + str(position)
	# print "row: " + str(row)
	# print "col: " + str(col) 
	return([row, col])

######################################################################################
# validate and transpose chords
def getChordInKey(chord, keyOrigin = "NNS", keyTarget = "NNS"):
	#cap first char
	chord = chord[0].upper() + chord[1:]

	# #if origin and target is same, assume already validated and send out
	# if (keyOrigin == keyTarget):
	# 	return str(chord)

	#if target key is NNS, return invld (we only transpose out of NNS, not into)
	if (keyTarget == "NNS"):
		return "invld1"

	chord = str(chord)
	keyOrigin = str(keyOrigin)
	keyTarget = str(keyTarget)

	#SLASH CHORD CASE: recursive call
	if ('/' in chord):
		#disassemble
		chordA = chord.split("/")[0].upper()
		chordB = chord.split("/")[1].upper()
		#recursive call
		result_A = getChordInKey(chordA, keyOrigin, keyTarget)
		result_B = getChordInKey(chordB, keyOrigin, keyTarget)

		if ("invld" not in result_A and "invld" not in result_B):
			#reassemble
			return(result_A + "/" + result_B)
		else:
			return("invld2")

	#make sure first char is valid
	possibleFirstChar = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', '1', '2', '3', '4', '5', '6', '7']
	if (chord[0] not in possibleFirstChar): #if its not a valid first char
		return(invld)

	#not presence of important chord modifiers
	containsSharp = '#' in str(chord)
	containsFlat = "b" in str(chord)[1:].lower()
	#other modifiers
	containsMinor = "m" in str(chord).lower().replace("dim", "") or "min" in str(chord).lower().replace("dim", "")
	# remove maj
	chord = str(chord).replace("maj", "")
	chord = str(chord).replace("MAJ", "")

	#if illegal
	if (containsSharp and containsFlat):
		return("invld3")

	#get leading chord element
	prefix = ""
	if (keyOrigin == "NNS"): #validate that key is NNS when accepting NNS chords
		if (not isInt(chord[0])):
			return("invld4")
		prefix = str(chord[0])
	else: #if not nns
		prefix = str(chord[0]).upper()

	#put things in order
	suffix = chord.replace(prefix, "").replace("b", "").replace("#", "").lower() #remove prefix from suffix
	if containsMinor:
		suffix = suffix.replace("m", "")
		suffix = "m" + suffix #move to front of suffix
	if containsSharp:
		# suffix = "#" + suffix #move to prefix
		prefix = prefix + "#"
	if containsFlat:
		suffix = suffix.replace("b", "")
		# suffix = "b" + suffix #move to prefix
		prefix = prefix + "b"


	#transpose prefix
	prefix = transpose(prefix, keyOrigin, keyTarget)

	if "invld" in prefix:
		return prefix

	#assemble
	fullChord = prefix + suffix.lower()
	if (len(fullChord) > 9):
		return("invld6")

	return(fullChord)


def transpose(baseChord, keyOrigin, keyTarget):
	#when using a flat key, use 'b', otherwise use '#' i.e. Fb key, use flats
	flatTargetKey = False
	if ("b" in keyTarget[1:]):
		flatTargetKey = True

	# print baseChord

	if keyOrigin != "NNS": #if source is not NNS
		#get diff
		startIndex = -1
		halfStepDiffCount = 0 #relative, can be negative
		for i in range(len(halfStepMatrix)): #get start
			if keyOrigin in halfStepMatrix[i]:
				startIndex = i
				break
		for i in range(len(halfStepMatrix)): #get end
			if keyTarget in halfStepMatrix[i]:
				halfStepDiffCount = i - startIndex
				break
		if startIndex == -1:
			return("invld7")

		#get chord location
		chordIndex = -1
		for i in range(len(halfStepMatrix)): #get chord origin index
			if baseChord in halfStepMatrix[i]:
				chordIndex = i
				break
		if chordIndex == -1:
			return("invld8")

		possibleTargetChords = halfStepMatrix[(chordIndex + halfStepDiffCount) % len(halfStepMatrix)] #get list of chords (2 max)


	else: #if source is NNS
		rootIndex = -1
		for i in range(len(halfStepMatrix)): #get 1 chord
			if keyTarget in halfStepMatrix[i]:
				rootIndex = i
		if rootIndex == -1:
			return("invld9")

		stepsFromRoot = int(baseChord[0]) #steps in NNSstepsToNext
		halfStepsFromRoot = 0

		for i in range(stepsFromRoot):
			halfStepsFromRoot += NNSstepsToNext[i]
		
		possibleTargetChords = halfStepMatrix[rootIndex + halfStepsFromRoot]

	#flats or sharps?
	if len(possibleTargetChords) == 1:
		return(possibleTargetChords[0])
	else:
		if flatTargetKey:
			try:
				return possibleTargetChords[1]
			except:
				return possibleTargetChords[0]
		else:
			return possibleTargetChords[0]

	#otherwise use halfStepMatrix
	return baseChord

#use for converting from NNS
NNSchordMatrix = { #major
	"C": ["C", "Dm", "Em", "F", "G", "Am", "B"],
	"D": ["D", "Em", "F#m", "G", "A", "Bm", "C#"],
	"Dflat": ["Dflat", "Eflatm", "Fm", "Gflat", "Aflat", "Bflatm", "C"],
	"C#": ["Dflat", "Eflatm", "Fm", "Gflat", "Aflat", "Bflatm", "C"], #same as above
	"E": ["E", "F#m", "G#m", "A", "B", "C#m", "D#"],
	"Eflat": ["Eflat", "Fm", "Gm", "Aflat", "Bflat", "Cm", "D"],
	"D#": ["Eflat", "Fm", "Gm", "Aflat", "Bflat", "Cm", "D"], #same as above
	"F": ["F", "Gm", "Am", "Bflat", "C", "Dm", "E"],
	"F#": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#"],
	"Gflat": ["F#", "G#m", "A#m", "B", "C#", "D#m", "F"], #same as above
	"G": ["G", "Am", "Bm", "C", "D", "Em", "F#"],
	"A": ["A", "Bm", "C#m", "D", "E", "F#m", "G#"],
	"Aflat": ["Aflat", "Bflatm", "Cm", "Dflat", "Eflat", "Fm", "G"],
	"G#": ["Aflat", "Bflatm", "Cm", "Dflat", "Eflat", "Fm", "G"], #same as above
	"B": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#"],
	"Bflat": ["Bflat", "Cm", "Dm", "Eflat", "F", "Gm", "A"],
	"A#": ["Bflat", "Cm", "Dm", "Eflat", "F", "Gm", "A"], #same as above
	"NNS": ["1", "2m", "3m", "4", "5", "6m", "7"],
	"NNS_": ["1", "2", "3", "4", "5", "6", "7"],
	}
NNSstepsToNext = [2, 2, 1, 2, 2, 2, 1] #2 = wholestep, 1 = halfstep

#use for general case, each index is half step
halfStepMatrix = [["A"], ["A#", "Bb"], ["B"], ["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"], ["F"], ["F#", "Gb"], ["G"], ["G#", "Ab"]]
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False













