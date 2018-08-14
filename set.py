from pymongo import MongoClient
import datetime

class Set:
	def __init__(self, sundayDate):
		self.sundayDate = sundayDate #datetime object
		self.rehearsalDate = None #datetime object

		self.leaders = list()
		self.vocalists = list()
		self.acousticGuitarists = list()
		self.electricLeadGuitarists = list()
		self.electricRhythmGuitarists = list()
		self.bassists = list()
		self.keyboarists = list()
		self.drummers = list()
		self.percussionists = list()
		self.violinists = list()
		self.other = list()

	def getSundayDate(self):
		return self.sundayDate

	def getRehearsalDate(self):
		return self.rehearsalDate

	def addLeader(self, googleID, instrument):
		self.leaders.append(googleID)
		self.vocalists.append(googleID) #leader needs to sing
		return googleID in self.leaders

	def addVocalist(self, googleID):
		self.vocalists.append(googleID)
		return googleID in self.vocalists

	def addAcousticGuitarist(self, googleID):
		self.acousticGuitarists.append(googleID)
		return googleID in self.acousticGuitarists

	def addElectricLeadGuitarist(self, googleID):
		self.electricLeadGuitarists.append(googleID)
		return googleID in self.electricLeadGuitarists

	def addElectricRhythmGuitarist(self, googleID):
		self.electricRhythmGuitarists.append(googleID)
		return googleID in self.electricRhythmGuitarists
		
	def addBassist(self, googleID):
		self.bassists.append(googleID)
		return googleID in self.bassists

	def addKeyboardist(self, googleID):
		self.keyboarists.append(googleID)
		return googleID in self.keyboarists
		
	def addDrummer(self, googleID):
		self.drummers.append(googleID)
		return googleID in self.drummers
		
	def addPercussionist(self, googleID):
		self.percussionists.append(googleID)
		return googleID in self.percussionists
		
	def addViolinist(self, googleID):
		self.violinists.append(googleID)
		return googleID in self.violinists
		
	def addOther(self, googleID):
		self.other.append(googleID)
		return googleID in self.other





	def removeLeader(self, googleID):
		self.leaders.remove(googleID)
		return googleID not in self.leaders

	def removeVocalist(self, googleID):
		self.vocalists.remove(googleID)
		return googleID not in self.vocalists

	def removeAcousticGuitarist(self, googleID):
		self.acousticGuitarists.remove(googleID)
		return googleID not in self.acousticGuitarists

	def removeElectricLeadGuitarist(self, googleID):
		self.electricLeadGuitarists.remove(googleID)
		return googleID not in self.electricLeadGuitarists

	def removeElectricRhythmGuitarist(self, googleID):
		self.electricRhythmGuitarists.remove(googleID)
		return googleID not in self.electricRhythmGuitarists
		
	def removeBassist(self, googleID):
		self.bassists.remove(googleID)
		return googleID not in self.bassists

	def removeKeyboardist(self, googleID):
		self.keyboarists.remove(googleID)
		return googleID not in self.keyboarists
		
	def removeDrummer(self, googleID):
		self.drummers.remove(googleID)
		return googleID not in self.drummers
		
	def removePercussionist(self, googleID):
		self.percussionists.remove(googleID)
		return googleID not in self.percussionists
		
	def removeViolinist(self, googleID):
		self.violinists.remove(googleID)
		return googleID not in self.violinists
		
	def removeOther(self, googleID):
		self.other.remove(googleID)
		return googleID not in self.other




	def getLeader(self):
		return self.leaders

	def getVocalists(self):
		return self.vocalists

	def getAcousticGuitarist(self):
		return self.acousticGuitarists

	def getElectricLeadGuitarist(self):
		return self.electricLeadGuitarists

	def getElectricRhythmGuitarist(self):
		return self.electricRhythmGuitarists
		
	def getBassist(self):
		return self.bassists

	def getKeyboardist(self):
		return self.keyboarists
		
	def getDrummer(self):
		return self.drummers
		
	def getPercussionist(self):
		return self.percussionists
		
	def getViolinist(self):
		return self.violinists
		
	def getOther(self):
		return self.other

	'''
	requirements:
		- at least one leader
		- at least one vocalist
		- at least one rhythmic instrument (acoustic guitar, keyboard, rhythm electric guitar)
	'''
	def validateLeader(self):
		return len(self.leaders) >= 1

	def validateVocalist(self):
		return len(self.vocalists) >= 1

	def validateRhythmInstrument(self):
		return (len(self.electricRhythmGuitarists) >= 1 or len(self.acousticGuitarists) >= 1 or len(self.keyboarists) >= 1)


	def getMembers(self):
		members = set()
		allLists = self.leaders + self.vocalists + self.acousticGuitarists + \
		           self.electricRhythmGuitarists + self.electricLeadGuitarists + self.bassists + \
		           self.keyboarists + self.drummers + self.percussionists + self.violinists + self.other

		for i in allLists:
			members.add(i)
		return members

	def getBandSize(self):
		return len(getMembers())

	def updateRehearsalDate(self, rehearsalDate):
		self.rehearsalDate = rehearsalDate
























