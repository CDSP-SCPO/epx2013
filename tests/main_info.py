idsDataDic={}
fields={}
print ""

#CHO0SE SOURCE (COMMENT OTHER SOURCES)
src="eurlex"
src="oeil"
src="prelex"


if src=="eurlex":
        #MODIFY AT WILL!!
        url="eurlex_content.html"

        import get_ids_eurlex as eurlexIds
        import get_data_eurlex as eurlexInfo
        html=eurlexIds.get_url_content_eurlex(url)
        print "INFORMATION RETRIEVAL"
        fields=eurlexInfo.get_data_eurlex(html)

elif src=="oeil":
        #MODIFY AT WILL!!
        url="oeilContent.html"
        idsDataDic['suite_2e_lecture_pe']=1

        import get_ids_oeil as ids_oeil
        import get_data_oeil as oeilInfo
        html=ids_oeil.get_url_content_oeil(url)
        print "IDS RETRIEVAL"
        idsDataDic.update(ids_oeil.get_ids_oeil(html))
        print ""
        print "INFORMATION RETRIEVAL"
        fields=oeilInfo.get_data_oeil(html, idsDataDic)

elif src=="prelex":
        #MODIFY AT WILL!!
        url="prelexContent.html"
        idsDataDic['split_propos']=0
        idsDataDic['suite_2e_lecture_pe']=1


        #get no_celex
        import get_ids_eurlex as eurlex_ids
        url_eurlex="eurlex_content.html"
        html=eurlex_ids.get_url_content_eurlex(url_eurlex)
        no_celex=eurlex_ids.get_ids_eurlex(html)["no_celex"]

        import get_ids_prelex as ids_prelex
        import get_data_prelex as prelexInfo
        html=ids_prelex.get_url_content_prelex(url)
        print "IDS RETRIEVAL"
        idsDataDic.update(ids_prelex.get_ids_prelex(html, no_celex))
        print ""
        print "INFORMATION RETRIEVAL"
        fields=prelexInfo.get_data_prelex(html, idsDataDic)

print ""
