#queries about the vote_public variable


def q17():
    #votes par année
    question="votes par année"
    print question
    res={}
    for year in years_list:
        res[year]= 0

    for act in Act.objects.filter(validated=2, vote_public=True):
        year=str(act.releve_annee)
        res[year]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        row.append(res[year])
    writer.writerow(row)
    writer.writerow("")
    print ""


def q33():
    #votes par année
    question="votes par secteur, en fonction de l'année"
    print question
    res=init_cs_year()

    for act in Act.objects.filter(validated=2, vote_public=True):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][year]+=1
    print "res", res

    write_cs_year(question, res)
