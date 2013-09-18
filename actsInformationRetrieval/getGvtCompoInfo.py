# -*- coding: utf-8 -*-
"""
get the information from gvtCompo
"""
from actsInformationRetrieval.models import GvtCompoModel


def getAssocVariables(act):
	"""
	FUNCTION
	get all the nationGvtPoliticalComposition from an act object
	PARAMETERS
	act: instance of an act (ActsInformationModel)
	RETURN
	prelexNationGvtPoliticalComposition (ActsInformationModel)
	"""
	gvt_compo_list=[]
	for gvtCompo in act.prelexNationGvtPoliticalComposition.all():
		split=gvtCompo.nationGvtPoliticalComposition.split(':', 1)
		gvt_compo_list.append((split[0], split[1]))
	return gvt_compo_list


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
	if act.prelexAdoptionConseil!=None:
		date=act.prelexAdoptionConseil
	else:
		#if no prelexAdoptionConseil, take oeilSignPECS
		date=act.oeilSignPECS

	gvtCompos=GvtCompoModel.objects.filter(startDate__lte=date, endDate__gte=date)
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
	gvtCompo data
	"""
	#TEST ONLY -> TO REMOVE
	#~ act.prelexAdoptionConseil="2012-02-21"

	gvt_compo=getGvtCompo(act)
	print "prelexNationGvtPoliticalComposition", gvt_compo

	return gvt_compo
