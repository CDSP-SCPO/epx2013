# -*- coding: utf-8 -*-
"""
get the information from opal
"""
from actsInformationRetrieval.models import NPModel


def getOpalVariables(noCelex):
	"""
	FUNCTION
	get opal variables npCaseNumber, np, npActivityType and npActivityDate
	PARAMETERS
	noCelex: noCelex of the act
	RETURN
	dictionary of opal variables
	"""
	try:
		#does the noCelex exist in NPModel?
		instances=NPModel.objects.filter(noCelex=noCelex)
		#there is at least one match -> we retrieve it/them
		npCaseNumberList=npList=npActivityTypeList=npActivityDateList=[]
		columnsList=["npCaseNumber", "np", "npActivityType", "npActivityDate"]
		opalDic={"opalNPCaseNumber":"", "opalNP":"", "opalNPActivityType":"", "opalNPActivityDate":""}
		#for each row concerning the act being retrieved
		for instance in instances:
			#for each column
			for varNameOpal in columnsList:
				varNameActsInfo="opal"+varNameOpal[:2].upper()+varNameOpal[2:]
				varList=eval(varNameOpal+"List")
				varValue=str(getattr(instance, varNameOpal))
				#if it's not already present in the variable list of different values
				if varValue not in varList:
					varList.append(varValue)
					#concatene different values in the dictionary to be returned
					opalDic[varNameActsInfo]+=varValue+"; "
		#delete last "; "
		for item in opalDic:
			opalDic[item]=opalDic[item][:-2]
		return opalDic
	except Exception, e:
		print "exception", e

	return None


def getOpalInfo(noCelex):
	"""
	FUNCTION
	gets all the information from opal (NPModel)
	PARAMETERS
	noCelex: noCelex of the act
	RETURN
	dictionary of retrieved data from opal
	"""
	dataDic={}

	#get npCaseNumber, np, npActivityType and npActivityDate
	try:
		dataDic.update(getOpalVariables(noCelex))
	except:
		print "no opal match"
	for key, value in dataDic.iteritems():
		print key, value

	return dataDic
