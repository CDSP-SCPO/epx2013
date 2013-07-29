# -*- coding: utf-8 -*-
"""
get the information from gvtCompo
"""
from actsInformationRetrieval.models import GvtCompoModel


def getAssocVariables(act):
	"""
	FUNCTION
	get nationGvtPoliticalComposition from GvtCompoModel
	PARAMETERS
	act: instance of an act (ActsInformationModel)
	RETURN
	prelexNationGvtPoliticalComposition (ActsInformationModel)
	"""
	mydic={}
	myDic=act.prelexNationGvtPoliticalComposition.all().values_list("nationGvtPoliticalComposition", flat=True)
	return myDic


def linkActInfoToGvtCompo(act):
	"""
	FUNCTION
	fill the assocation table which links an act to its governments composition
	PARAMETERS
	act: instance of an act (ActsInformationModel)
	RETURN
	True if matching data were saved in the association, False otherwise
	"""
	#we retrieve all the rows from GvtCompoModel for which startDate<adoptionConseil<endDate
	gvtCompos=GvtCompoModel.objects.filter(startDate__lte=act.prelexAdoptionConseil, endDate__gte=act.prelexAdoptionConseil)
	#fill the association
	for gvtCompo in gvtCompos:
		act.prelexNationGvtPoliticalComposition.add(gvtCompo)

	if gvtCompos:
		return True
	return False


def getGvtCompo(act):
	"""
	FUNCTION
	get nationGvtPoliticalComposition (GvtCompoModel)
	PARAMETERS
	act: instance of an act (ActsInformationModel)
	RETURN
	prelexNationGvtPoliticalComposition (ActsInformationModel)
	"""

	nationGvtPoliticalComposition=getAssocVariables(act)
	#no match in the db
	if not nationGvtPoliticalComposition:
		#the government compositions for the current act have not been searched and filled yet
		#let's fill the association
		if linkActInfoToGvtCompo(act)==True:
			#if there is at least one matching row
			return getAssocVariables(act)
		else:
			return None
	else:
		return nationGvtPoliticalComposition

	return None



def getGvtCompoInfo(act):
	"""
	FUNCTION
	returns GvtCompoModel data matching the current act
	PARAMETERS
	act: instance of the act
	RETURN
	dataDic: gvtCompo data
	"""
	dataDic={}

	#TEST ONLY -> TO REMOVE
	#~ act.prelexAdoptionConseil="2012-02-21"

	dataDic["prelexNationGvtPoliticalComposition"]=getGvtCompo(act)
	print "prelexNationGvtPoliticalComposition", dataDic["prelexNationGvtPoliticalComposition"]

	return dataDic
