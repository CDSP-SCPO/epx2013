"""
1/ids and errors retrieval
2/get the urls of European institutions from the ids
3/cross validation between the websites
"""

import getEurlexIdsFunctions as eurlex
import getOeilIdsFunctions as oeil
import getPrelexIdsFunctions as prelex


def checkAndGetEurlexIds(noCelex):
	"""
	FUNCTION
	checks and gets all the ids from the eurlex id
	PARAMETERS
	noCelex: noCelex id (Eurlex)
	RETURN
	dictionary of retrieved data from eurlex
	"""
	dataDic={}
	eurlexUrl=eurlex.getEurlexUrl(noCelex)
	print "eurlex url", eurlexUrl
	eurlexUrlContent=eurlex.getEurlexUrlContent(eurlexUrl)
	if eurlexUrlContent!=False:
		#~ #gets information from eurlex
		dataDic['fileEurlexUrlExists']=True
		dataDic.update(eurlex.getAllEurlexIds(eurlexUrlContent))
	else:
		dataDic['fileEurlexUrlExists']=False
		print "eurlex url does not exist!!"
	
	#~ dataDic['eurlexEurlexUrl']=eurlexUrl
	
	return dataDic
	

def checkAndGetOeilIds(noUniqueType, noUniqueAnnee, noUniqueChrono):
	"""
	FUNCTION
	checks and gets all the ids from the oeil ids
	PARAMETERS
	noUniqueAnnee: noUniqueAnnee id
	noUniqueChrono: noUniqueChrono id
	noUniqueType: noUniqueType id
	RETURN
	dictionary of retrieved data from oeil
	"""
	dataDic={}
	oeilUrl=oeil.getOeilUrl(noUniqueType, noUniqueAnnee, noUniqueChrono)
	print "oeil url", oeilUrl
	oeilUrlContent=oeil.getOeilUrlContent(oeilUrl)
	if oeilUrlContent!=False:
		#~ #gets information from oeil
		dataDic['fileOeilUrlExists']=True
		dataDic.update(oeil.getAllOeilIds(oeilUrlContent))
	else:
		print "oeil url does not exist!!"
		dataDic['fileOeilUrlExists']=False
		dataDic['oeilNoCelex']=None
		dataDic['oeilNoUniqueAnnee']=None
		dataDic['oeilNoUniqueType']=None
		dataDic['oeilNoUniqueChrono']=None
		dataDic['oeilProposOrigine']=None
		dataDic['oeilProposAnnee']=None
		dataDic['oeilProposChrono']=None
	
	#~ dataDic['oeilOeilUrl']=oeilUrl
	
	return dataDic
	
def checkAndGetPrelexIds(idsDic):
	"""
	FUNCTION
	checks and gets all the ids from the prelex ids
	PARAMETERS
	idsDic: dosId or proposOrigine proposAnnee proposChrono
	RETURN
	dictionary of retrieved data from prelex
	"""
	dataDic={}
	if "proposOrigine" in idsDic:
		prelexUrl=prelex.getOldPrelexUrl(idsDic['proposOrigine'], idsDic['proposAnnee'], idsDic['proposChrono'])
	elif "noUniqueType" in idsDic:
		prelexUrl=prelex.getOldPrelexUrlWithOeilIds(idsDic['noUniqueType'], idsDic['noUniqueAnnee'], idsDic['noUniqueChrono'])
	elif "dosId" in idsDic:
		prelexUrl=prelex.getPrelexUrl(idsDic['dosId'])
			
	prelexUrlContent=prelex.getPrelexUrlContent(prelexUrl)
	if prelexUrlContent!=False:
		#~ #gets information from prelex
		dataDic['filePrelexUrlExists']=True
		dataDic.update(prelex.getAllPrelexIds(prelexUrlContent))
	else:
		print "prelex url does not exist!!"
		dataDic['filePrelexUrlExists']=False
		dataDic['prelexNosCelex']=None
		dataDic['prelexDosId']=None
		dataDic['prelexNoUniqueAnnee']=None
		dataDic['prelexNoUniqueType']=None
		dataDic['prelexNoUniqueChrono']=None
		dataDic['prelexProposOrigine']=None
		dataDic['prelexProposAnnee']=None
		dataDic['prelexProposChrono']=None
		
	dataDic['filePrelexUrl']=prelexUrl

	return dataDic
