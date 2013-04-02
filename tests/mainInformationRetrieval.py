idsDataDic={}
dataDic={}
print ""

#CHO0SE SOURCE (COMMENT OTHER SOURCES)
src="eurlex"
#~ src="oeil"
#~ src="prelex"


if src=="eurlex":
	#MODIFY AT WILL!!
	url="eurlexContent.html"

	import getEurlexIdsFunctions as eurlexIds
	import getEurlexInformationFunctions as eurlexInfo
	html=eurlexIds.getEurlexUrlContent(url)
	print "INFORMATION RETRIEVAL"
	dataDic=eurlexInfo.getEurlexInformation(html)

elif src=="oeil":
	#MODIFY AT WILL!!
	url="oeilContent.html"
	idsDataDic['suite2eLecturePE']=1

	import getOeilIdsFunctions as oeilIds
	import getOeilInformationFunctions as oeilInfo
	html=oeilIds.getOeilUrlContent(url)
	print "IDS RETRIEVAL"
	idsDataDic.update(oeilIds.getAllOeilIds(html))
	print ""
	print "INFORMATION RETRIEVAL"
	dataDic=oeilInfo.getOeilInformation(html, idsDataDic)

elif src=="prelex":
	#MODIFY AT WILL!!
	url="prelexContent.html"
	idsDataDic['proposSplittee']=0
	idsDataDic['suite2eLecturePE']=1

	import getPrelexIdsFunctions as prelexIds
	import getPrelexInformationFunctions as prelexInfo
	html=prelexIds.getPrelexUrlContent(url)
	print "IDS RETRIEVAL"
	idsDataDic.update(prelexIds.getAllPrelexIds(html))
	print ""
	print "INFORMATION RETRIEVAL"
	dataDic=prelexInfo.getPrelexInformation(html, idsDataDic)

print ""
