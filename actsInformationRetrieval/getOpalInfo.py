# -*- coding: utf-8 -*-
"""
get the information from opal
"""
from actsInformationRetrieval.models import NPModel
import variablesNameForInformation as vnInfo


def getOpalVariables(noCelex):
	"""
	FUNCTION
	get opal variables npCaseNumber, np, npActivityType and npActivityDate
	PARAMETERS
	noCelex: noCelex of the act
	RETURN
	dictionary of opal variables
	"""
	opal_dic={}
	try:
		#does the noCelex exist in NPModel?
		instances=NPModel.objects.filter(noCelex=noCelex)
		for instance in instances:
			npActivityType=(vnInfo.variablesNameDic["opalNPActivityType"] , instance.npActivityType)
			npActivityDate=(vnInfo.variablesNameDic["opalNPActivityDate"] , instance.npActivityDate)
			npCaseNumber=(vnInfo.variablesNameDic["opalNPCaseNumber"] , instance.npCaseNumber)
			opal_dic[instance.np]=(npActivityType, npActivityDate, npCaseNumber)
	except Exception, e:
		print "getOpalVariables exception", e

	return opal_dic


def getOpalInfo(noCelex):
	"""
	FUNCTION
	gets all the information from opal (NPModel)
	PARAMETERS
	noCelex: noCelex of the act
	RETURN
	dictionary of retrieved data from opal
	"""


	#get npCaseNumber, np, npActivityType and npActivityDate
	opal=getOpalVariables(noCelex)
	print "opal", opal
	return opal
