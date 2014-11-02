#queries about the ministers attendance variables

def q22():
    #pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par secteurs et par annee
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par année"
    print question
    res={}
    total_year={}
    statuses={}
    statuses["M"]=0
    statuses["CS"]=1
    statuses["CS_PR"]=1
    for status in statuses:
        res[statuses[status]]={}
        for year in years_list:
            res[statuses[status]][year]=0
    for year in years_list:
        total_year[year]=0
  
    for act in MinAttend.objects.filter(act__validated=2):
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        if status not in ["NA", "AB"]:
            year=str(act.act.releve_annee)
            total_year[year]+=1
            res[statuses[status]][year]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for index in range(2):
        if index==0:
            row=["M"]
        else:
            row=["RP"]
        for year in years_list:
            if res[index][year]==0:
                res_year=0
            else:
                res_year=round(float(res[index][year])*100/total_year[year],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""

    

def q38():
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) selon le pays et l'année (premier chiffre : pourcentage de M  par rapport au pays et à l'année ; deuxième chiffre : pourcentage de CS ou CS_PR par rapport au pays et à l'année)"
    print question

    statuses={}
    statuses["M"]=0
    statuses["CS"]=1
    statuses["CS_PR"]=1
    res={}
    total_cell={}
    for country in countries:
        res[country]={}
        total_cell[country]={}
        for year in years_list:
            total_cell[country][year]=0
            res[country][year]=[0,0]

    for act in MinAttend.objects.filter(act__validated_attendance=True).exclude(act__releve_annee=2013):
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        country=act.country.country_code
        if status not in ["NA", "AB"]:
            year=str(act.act.releve_annee)
            total_cell[country][year]+=1
            res[country][year][statuses[status]]+=1
    print "res", res
    print "total_cell", total_cell

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for country in countries:
        row=[country]
        for year in years_list:
            res_year=""
            for index in range(2):
                if res[country][year][index]==0:
                    temp=0
                else:
                    temp=round(float(res[country][year][index])*100/total_cell[country][year],3)
                res_year+=str(temp)+ " / "
            row.append(res_year[:-3])
        writer.writerow(row)
    writer.writerow("")
    print ""


def q76():
    question="Pourcentage moyen de représentants permanents par acte"
    queries_periodes(question, MinAttend, query="repr_perm")
    
