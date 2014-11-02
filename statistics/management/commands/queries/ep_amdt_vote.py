#queries about the amdt variables


def q16():
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt par année"
    print question
    amdts={}
    amdts["EPComAmdtTabled"]="com_amdt_tabled"
    amdts["EPComAmdtAdopt"]="com_amdt_adopt"
    amdts["EPAmdtTabled"]="amdt_tabled"
    amdts["EPAmdtAdopt"]="amdt_adopt"
    res={}
    for amdt in amdts:
        res[amdt]={}
        for year in years_list:
            res[amdt][year]=[0,0]

    for act in Act.objects.filter(validated=2):
        year=str(act.releve_annee)
        for amdt in amdts:
            if getattr(act, amdts[amdt])!=None:
                res[amdt][year][1]+=1
                res[amdt][year][0]+=getattr(act, amdts[amdt])
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for amdt in amdts:
        row=[amdt]
        for year in years_list:
            if res[amdt][year][1]==0:
                res_year=0
            else:
                res_year=round(float(res[amdt][year][0])/res[amdt][year][1],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""




def q32(display_name, variable_name):
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de " +display_name+ " par secteur, en fonction de l'année"
    print question
    res, total_year=init_cs_year(nb=2, total=True, amdt=True)
    res, total_year=get_by_cs_year(res, variable=variable_name, total_year=total_year)
    write_cs_year(question, res, total_year=total_year, nb=2, amdt=True)


    
def q75():
    question="Nombre moyen d’amendements déposés par la commission parlementaire du PE saisie au fond"
    filter_variables={"com_amdt_tabled__isnull": False}
    queries_periodes(question, Act, filter_variables=filter_variables, exclude_variables={"com_amdt_tabled": 0}, filter_total=filter_variables, avg_variable="com_amdt_tabled", percent=1)
    
    question="Nombre moyen d’amendements déposés au PE"
    filter_variables={"amdt_tabled__isnull": False}
    queries_periodes(question, Act, filter_variables=filter_variables, exclude_variables={"amdt_tabled": 0}, filter_total=filter_variables, avg_variable="amdt_tabled", percent=1)


def q99():
    #Nombre d’EPComAmdtAdopt, 2/Nombre d’EPComAmdtTabled, 3/Nombre d’EPAmdtAdopt, 4/Nombre d’EPAmdtTabled, par année, par secteur, par année et par secteur
    variables={"com_amdt_tabled": "EPComAmdtTabled", "com_amdt_adopt": "EPComAmdtAdopt", "amdt_tabled": "EPAmdtTabled", "amdt_adopt": "EPAmdtAdopt"}

    for key, value in variables.iteritems():
        question="Nombre total d'"+value+" par secteur"
        print question
        res=init_cs(nb_vars=1)
        res=get_by_cs(res, nb_vars=1, variable=key, filter_vars={"validated": 2, key+"_isnull": False})
        write_cs(question, res, nb_vars=1)

        question="Nombre total d'"+value+" par année"
        print question
        res=init_year(nb_vars=1)
        res=get_by_year(res, nb_vars=1, variable=key, filter_vars={"validated": 2, key+"_isnull": False})
        write_year(question, res, nb_vars=1)

        question="Nombre total d'"+value+" par année et par secteur"
        print question
        res=init_cs_year(nb_vars=1)
        res=get_by_cs_year(res, nb_vars=1, variable=key, filter_vars={"validated": 2, key+"_isnull": False})
        write_cs_year(question, res, nb_vars=1)


def q100():
    #1/Moyenne EPVotesFor1, 2/Moyenne EPVotesFor2, 3/Moyenne EPVotesAgst1, 4/Moyenne EPVotesAgst2, 5/Moyenne EPVotesAbs1, 6/Moyenne EPVotesAbs2, par année, par secteur, par année et par secteur
    variables={"votes_for_": "EPVotesFor", "votes_agst_": "EPVotesAgst", "votes_abs_": "EPVotesAbs"}
    nb=2

    #TODO
    for key, value in variables.iteritems():
        for index range(1, nb+1):
            i=str(index)
            variable=key+i
            question="Nombre moyen de "+EPVotesFor+i+" par secteur"
            print question
            res=init_cs(nb_vars=1)
            res=get_by_cs(res, variable=variable, filter_vars={"validated": 2, variable+"_isnull": False})
            write_cs(question, res, percent=1)

            question="Pourcentage d'actes NoUniqueType=COD adoptés en "+value+" par année"
            print question
            res=init_year()
            res=get_by_year(res, Model=ActIds, filter_vars={"act__validated": 2, "src": "index", "act__nb_lectures_isnull": False}, check_vars_act={"nb_lectures": key}, check_vars_act_ids={"no_unique_type": "COD"})
            write_year(question, res, percent=1)

            question="Pourcentage d'actes NoUniqueType=COD adoptés en "+value+" par année et par secteur"
            print question
            res=init_cs_year()
            res=get_by_cs_year(res, Model=ActIds, filter_vars={"act__validated": 2, "src": "index", "act__nb_lectures_isnull": False}, check_vars_act={"nb_lectures": key}, check_vars_act_ids={"no_unique_type": "COD"})
            write_cs_year(question, res, percent=1)
