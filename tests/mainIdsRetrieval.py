import getEurlexIdsFunctions as eurlex
import getOeilIdsFunctions as oeil
import getPrelexIdsFunctions as prelex

#ids
#eurlex
noCelex="32006R1921"
noCelex="32009D0829"

#oeil
noUniqueAnnee="2005"
noUniqueChrono="63"
noUniqueType="CNS"
#~ noUniqueAnnee="2008"
#~ noUniqueChrono="77"
#~ noUniqueType="CNS"

#prelex
dosId="193517"
dosId="196066"
proposAnnee="2004"
proposChrono="15130"
proposOrigine="CONS"
prelexIdsDic={}
prelexIdsDic['dosId']=dosId
prelexIdsDic["proposAnnee"]=proposAnnee
prelexIdsDic["proposChrono"]=proposChrono
prelexIdsDic["proposOrigine"]=proposOrigine

eurlexUrl="eurlexContent.html"
oeilUrl="oeilContent.html"
prelexUrl="prelexContent.html"


#PARAMETERS TO CHANGE
ids="yes"
#~ ids="no"
choice="eurlex"
choice="oeil"
choice="prelex"
choice="prelexWithOldIds"
choice="prelexWithOeilIds"

print ""

if choice =="eurlex":
	if ids=="yes":
		html=eurlex.getEurlexUrlContent(eurlex.getEurlexUrl(noCelex))
	else:
		html=eurlex.getEurlexUrlContent(eurlexUrl)

	eurlex.getAllEurlexIds(html)
	
elif choice=="oeil":
	if ids=="yes":
		html=oeil.getOeilUrlContent(oeil.getOeilUrl(noUniqueType, noUniqueAnnee, noUniqueChrono))
	else:
		html=oeil.getOeilUrlContent(oeilUrl)

	oeil.getAllOeilIds(html)

else:
	if ids=="yes":
		if choice=="prelexWithOldIds":
			prelexUrl=prelex.getOldPrelexUrl(prelexIdsDic['proposOrigine'], prelexIdsDic['proposAnnee'], prelexIdsDic['proposChrono'])
		elif choice=="prelexWithOeilIds":
			prelexUrl=prelex.getOldPrelexUrlWithOeilIds(noUniqueType, noUniqueAnnee, noUniqueChrono)
			print "prelexUrl", prelexUrl
		else:
			prelexUrl=prelex.getPrelexUrl(prelexIdsDic['dosId'])
	
	html=prelex.getPrelexUrlContent(prelexUrl)
	prelex.getAllPrelexIds(html)


print ""
