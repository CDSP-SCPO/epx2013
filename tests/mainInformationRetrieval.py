import getEurlexIdsFunctions as eurlexIds
import getEurlexInformationFunctions as eurlexInfo
import getOeilIdsFunctions as oeilIds
import getOeilInformationFunctions as oeilInfo
import getPrelexIdsFunctions as prelexIds
import getPrelexInformationFunctions as prelexInfo

idsDataDic={}
dataDic={}
print ""
print "INFORMATION RETRIEVAL"
print ""

#CHO0SE SOURCE (COMMENT OTHER SOURCES)
src="eurlex"
src="oeil"
#~ src="prelex"


if src=="eurlex":
	#MODIFY AT WILL!!
	url="eurlexContent.html"

	html=eurlexIds.getEurlexUrlContent(url)
	dataDic=eurlexInfo.getEurlexInformation(html)

elif src=="oeil":
	#MODIFY AT WILL!!
	url="oeilContent.html"
	html=oeilIds.getOeilUrlContent(url)
	dataDic=oeilInfo.getOeilInformation(html)

elif src=="prelex":
	#MODIFY AT WILL!!
	url="prelexContent.html"
	idsDataDic['proposSplittee']=0
	idsDataDic['suite2eLecturePE']=1

	html=prelexIds.getPrelexUrlContent(url)
	idsDataDic.update(prelexIds.getAllPrelexIds(html))
	dataDic=prelexInfo.getPrelexInformation(html, idsDataDic)
