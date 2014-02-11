import get_ids_eurlex as eurlex
import get_ids_oeil as oeil
import get_ids_prelex as prelex

#ids
#eurlex
no_celex="32006R1921"
no_celex="31997D0091"

#oeil
no_unique_annee="2005"
no_unique_chrono="63"
no_unique_type="CNS"
no_unique_annee="2008"
no_unique_chrono="0762"
no_unique_type="COD"

#prelex
dos_id="193517"
dos_id="196066"
propos_annee="2004"
propos_chrono="15130"
propos_origine="CONS"
ids_prelexDic={}
ids_prelexDic['dos_id']=dos_id
ids_prelexDic["propos_annee"]=propos_annee
ids_prelexDic["propos_chrono"]=propos_chrono
ids_prelexDic["propos_origine"]=propos_origine

url_eurlex="eurlex_content.html"
url_oeil="oeil_content.html"
url_prelex="prelex_content.html"


#PARAMETERS TO CHANGE
src="file"
#~ src="www"
choice="eurlex"
choice="oeil"
#~ choice="prelex"
#~ choice="prelexWithOldIds"
#~ choice="prelexWithOeilIds"

print ""

if choice=="eurlex":
    if src=="www":
        html=eurlex.get_url_content_eurlex(eurlex.get_url_eurlex(no_celex))
    else:
        html=eurlex.get_url_content_eurlex(url_eurlex)

    eurlex.get_ids_eurlex(html)

elif choice=="oeil":
    if src=="www":
        html=oeil.get_url_content_oeil(oeil.get_url_oeil(no_unique_type, no_unique_annee, no_unique_chrono))
    else:
        html=oeil.get_url_content_oeil(url_oeil)

    oeil.get_ids_oeil(html)

else:
    if src=="www":
        if choice=="prelexWithOldIds":
            url_prelex=prelex.get_url_prelex_propos(ids_prelexDic['propos_origine'], ids_prelexDic['propos_annee'], ids_prelexDic['propos_chrono'])
        elif choice=="prelexWithOeilIds":
            url_prelex=prelex.get_url_prelex_no_unique(no_unique_type, no_unique_annee, no_unique_chrono)
            print "url_prelex", url_prelex
        else:
            url_prelex=prelex.get_url_prelex(ids_prelexDic['dos_id'])

    html=prelex.get_url_content_prelex(url_prelex)
    prelex.get_ids_prelex(html)


print ""
