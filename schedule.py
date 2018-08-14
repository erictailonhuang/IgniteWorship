from pymongo import MongoClient
from datetime import date, timedelta, datetime
import calendar

import set as s

client = MongoClient("localhost", 27017)
db = client["IgniteWorship"]

def getAllProfiles():
	profilesMongo = db.members.find()
	profiles = dict()
	if profilesMongo == None:
		print "UNABLE TO RETRIEVE PROFILES FROM DATABASE"
		return None
		#handle this somehow on the UI
	else:
		for i in profilesMongo:
			profiles[i["googleID"]] = i
	return profiles

def allSundays(year):
	d = date(year, 1, 1)                    # January 1st
	d += timedelta(days = 6 - d.weekday())  # First Sunday
	while d.year == year:
		yield d
		d += timedelta(days = 7)

def getAllSundaysInQuarter(year, quarter):
	sundays_pre = list()
	sundays = list()
	for d in allSundays(year):
		sundays_pre.append(d)

	#prune list of sundays to just quarter of interest
	monthEnd = quarter * 3
	monthStart = monthEnd - 3
	
	for s in sundays_pre:
		if s.month >= monthStart and s.month <= monthEnd:
			sundays.append(s)
	return sundays


def schedule(year, quarter, profiles):
	#get profiles
	# profiles = getAllProfiles()

	#setup quarter
	sundays = getAllSundaysInQuarter(year, quarter)

	sets = list()

	for sun in sundays: #DATE FORMAT IS YEAR-MONTH-DAY
		dayBefore = sun - timedelta(days=1)
		#set datetime
		dateTime_Sunday = getDateTimeObject(str(sun.year) + "-" + str(sun.month) + "-" + str(sun.day))
		dateTime_Sunday = dateTime_Sunday.replace(hour=11, minute=45)
		#rehearsal datetime
		dateTime_Rehearsal = getDateTimeObject(str(dayBefore.year) + "-" + str(dayBefore.month) + "-" + str(dayBefore.day))
		dateTime_Rehearsal = dateTime_Rehearsal.replace(hour=10, minute=00)

		temp = s.Set(dateTime_Sunday)
		temp.updateRehearsalDate(dateTime_Rehearsal)

		sets.append(temp)

	worshipperIDs = profiles.keys() #cycle through when picking people

	#populate worshippers into sets
	for i in sets:
		#find a leader REQUIRED
			# update profile['lastSet']

			

		#find a rhythm instrumentalist REQUIRED
			# update profile['lastSet']


		#find drummer

		#find bassist



		#check set object functions to make sure critical components have been populated
			# def validateLeader(self):

			# def validateVocalist(self):

			# def validateRhythmInstrument(self):

			# def getMembers(self):

			# def getBandSize(self):
		continue


	return sets

def getNextPersonToFillRole(roleName, sundayDateTimeObject, profiles):
	#algo to pick avaialble person who served least recently

		# leader
		# vocalist
		# acousticGuitarist
		# electricLeadGuitarist
		# electricRhythmGuitarist
		# bassist
		# keyboarist
		# drummer
		# percussionist
		# violinist
		# other

		# def p1(args):
		#     whatever

		# def p2(more args):
		#     whatever

		# myDict = {
		#     "P1": p1,
		#     "P2": p2,
		#     ...
		#     "Pn": pn
		# }

		# def myMain(name):
		#     myDict[name]()

	return

def worshiperIsAvailable(profile, sundayDateTimeObject):

	# if profile['lastSet'] != (sundayDateTimeObject - timedelta(weeks = 1)):
	# 	continue
	# profile['unavailableSundays']
	# profile['serveMore']

	return

def processProfiles(profiles):
	'''
	reduce to:
		'googleID': {
						'lastSet': dateTimeObject, 
						'secondaryInstruments': list(str), 
						'unavailableSundays': list(dateTimeObject), 
						'leader': Bool, 
						'primaryInstrument': str, 
						'serveMore': int, (0 = no, 1 = yes, 2 = only if needed) 
						'vocalist': Bool
					}
	'''

	for i in profiles.keys():
		temp = dict()
		temp['leader'] = profiles[i]['leader']
		temp['vocalist'] = profiles[i]['vocalist']
		temp['primaryInstrument'] = profiles[i]['primaryInstrument'] #can be None
		temp['secondaryInstruments'] = str(profiles[i]['secondaryInstrument']).replace(" ", "").split(",")
		temp['unavailableSundays'] = processDateList(profiles[i]['unavailableSundays']) #UPDATE WITH NEW GUI
		if (profiles[i]['serveMore'] == 'No'):
			temp['serveMore'] = 0
		elif (profiles[i]['serveMore'] == 'Yes'):
			temp['serveMore'] = 1
		else:
			temp['serveMore'] = 2 #only if needed
		temp['lastSet'] = None ##UPDATE WITH DB LOOKUP, getDateTimeObject()
		
		profiles[i] = temp
	
	return profiles

def processDateList(dateList):
	if dateList == None:
		return None
	#converts a list of dates in format u'Sep 30 to 2018-09-30 to datetime object
	#guess year to be the next occurence of the date 
	formattedDates = list()
	monthAbbreviationLookup = dict((v,k) for k,v in enumerate(calendar.month_abbr))
	for i in dateList:
		month = int(monthAbbreviationLookup[str(i.strip().split(" ")[0])])
		day = int(i.strip().split(" ")[1])
		year = None

		#guess the year (user isnt required to specify year YET)
		dt = datetime.now()
		for dayBias in range(0, 365):
			dt += timedelta(days = dayBias)
			if dt.month >= month:
				year = dt.year
				break

		formattedDates.append(getDateTimeObject(str(str(year) + "-" + str(month) + "-" + str(day))))
	return formattedDates

def getDateTimeObject(dateString): #YEAR-MONTH-DAY
	return datetime.strptime(dateString, '%Y-%m-%d')

if __name__ == "__main__":
	#get profiles
	profiles =  getAllProfiles()

	if profiles != None:
		#prune and process profile data
		profiles = processProfiles(profiles)

		#schedule
		setSchedule = schedule(2018, 4, profiles)

		#commit to DB
	else:
		print "FAIL"








