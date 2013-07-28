#manipulates dates
from datetime import date

def splitFrenchDate(dateString):
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


def splitDateToIso(year, month, day):
	"""
	FUNCTION
	transform a split date to the iso format ('YYYY-MM-DD')
	PARAMETERS
	year, month, day: year, month and day of the date to transform
	RETURN
	date in the iso format
	"""
	return date(int(year), int(month), int(day)).isoformat()


def stringToIsoDate(string):
	"""
	FUNCTION
	transform a string date to the iso format ('YYYY-MM-DD')
	PARAMETERS
	string: string date to convert
	RETURN
	date in the iso format
	"""
	#if year is first
	if string[2].isdigit():
		year, month, day=string[:4], string[5:7], string[8:]
	#if year is last
	else:
		#the year must be coded on 4 digits
		year, month, day=string[6:], string[3:5], string[:2]
	return splitDateToIso(year, month, day)


def listReverseEnum(L):
	"""
	FUNCTION
	reverse a list or string and return it along with the original position of each element
	PARAMETERS
	L: list or string
	RETURN
	reverse list+ index
	"""
	for index in reversed(xrange(len(L))):
	  yield index, L[index]


def show(varName):
	"""
	FUNCTION
	"improves" built-in print function
	PARAMETERS
	varName: name of the variable to display
	RETURN
	nice display of the variable
	"""
	return varName+": "+eval(varName)
