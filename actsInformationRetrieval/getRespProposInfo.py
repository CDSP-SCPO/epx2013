# -*- coding: utf-8 -*-
"""
get the related fields of RespPropos  (from NationRespModel, NationalPartyRespModel, EUGroupRespModel)
"""
from actsInformationRetrieval.models import RespProposModel, NationRespModel, NationalPartyRespModel, EUGroupRespModel
from django.db.models.loading import get_model


def getRespProposVariablesFromDB(table1, respPropos):
	"""
	FUNCTION
	gets the prelex respPropos variables (nationResp, nationalPartyResp or euGroupResp)
	PARAMETERS
	table1: list of model name, field name in the csv file for table1
	respProposId: respPropos id
	RETURN
	nationResp, nationalPartyResp or euGroupResp
	"""
	table2=["RespProposModel", "id", respPropos]
	if table2[2]!=None:
		model1 = get_model('actsInformationRetrieval', table1[0])
		model2 = get_model('actsInformationRetrieval', table2[0])
		attrName1=table1[1]
		attrIdName2=table2[1]
		attrIdName1=attrName1+"_id"
		attrId2=table2[2]

		try:
			#get attrId1 from model2
			instance2=model2.objects.get(**{attrIdName2: attrId2})
			attrId1=getattr(instance2, attrIdName1)
			#if it exist, we get attr1 from model1
			instance1=model1.objects.get(id=attrId1)
			return getattr(instance1, attrName1)
		except Exception, e:
			print "exception", e

	return None


def getPrelexNationResp(respProposId):
	"""
	FUNCTION
	get the nationResp variable from respProposId, RespProposModel and NationRespModel
	PARAMETERS
	respProposId: respPropos id
	RETURN
	nationResp associated to  respProposId
	"""
	table1=["NationRespModel", "nationResp"]
	return getRespProposVariablesFromDB(table1, respProposId)


def getPrelexNationalPartyResp(respProposId):
	"""
	FUNCTION
	get the nationalPartyResp variable from respProposId, RespProposModel and NationalPartyRespModel
	PARAMETERS
	respProposId: respPropos id
	RETURN
	nationalPartyResp associated to  respProposId
	"""
	table1=["NationalPartyRespModel", "nationalPartyResp"]
	return getRespProposVariablesFromDB(table1, respProposId)


def getPrelexEUGroupResp(respProposId):
	"""
	FUNCTION
	get the euGroupResp variable from respProposId, RespProposModel and EUGroupRespModel
	PARAMETERS
	respProposId: respPropos id
	RETURN
	euGroupResp associated to  respProposId
	"""
	table1=["EUGroupRespModel", "euGroupResp"]
	return getRespProposVariablesFromDB(table1, respProposId)


def getRespProposInfo(respProposId):
	"""
	FUNCTION
	get the respProposId linked variables from respProposId, RespProposModel, NationRespModel, NationalPartyRespModel, EUGroupRespModel
	PARAMETERS
	respProposId: respPropos id
	RETURN
	respProposId linked variables nationResp, nationalPartyResp and euGroupResp
	"""
	nationResp=getPrelexNationResp(respProposId)
	print "nationResp", nationResp
	nationalPartyResp=getPrelexNationalPartyResp(respProposId)
	print "nationalPartyResp", nationalPartyResp
	euGroupResp=getPrelexEUGroupResp(respProposId)
	print "euGroupResp", euGroupResp

	return nationResp, nationalPartyResp, euGroupResp

