#manipulates dates
from datetime import date

def splitFrenchFormatDate(dateString):
	"""
	FUNCTION
	split a date ('DD-MM-YYYY') into year, month and day
	PARAMETERS
	dateString: date to split
	RETURN
	year, month and day of the date
	"""
	day=dateString[:2]
	month=dateString[3:5]
	try:
		#date coded on 4 digits
		year=dateString[6:]
	except:
		#date coded on 2 digits
		year=dateString[4:]

	return year, month, day


def dateToIso(year, month, day):
	"""
	FUNCTION
	transform a date to the iso format ('YYYY-MM-DD')
	PARAMETERS
	year, month, day: year, month and day of the date to transform
	RETURN
	date in the iso format
	"""
	return date(int(year), int(month), int(day)).isoformat()
