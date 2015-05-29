#-*- coding: utf-8 -*-

#queries about the pers variables (RespPropos or Rapporteur)


def q91():
    initial_question="Liste des RespPropos 1-3, PartyFamily et Nationalite"
    #~ -> par secteur
    question=initial_question+", par secteur"
    print question
    res=init_cs(empty_dic=True)
    res=get_list_pers_cs(res, "resp", 3)
    write_list_pers(question, cs_list, "CS", res, "resp")
#~ 
    #~ #-> par année
    question=initial_question+", par année"
    print question
    res=init_year(empty_dic=True)
    res=get_list_pers_year(res, "resp", 3)
    write_list_pers(question, years_list, "YEAR", res, "resp")

    #~ #-> par secteur et par année
    question=initial_question+", par secteur et par année"
    print question
    res=init_cs_year(empty_dic=True)
    res=get_list_pers_cs(res, "resp", 3, year_var=True)
    write_list_pers_cs_year(question, res, "resp")
    #~ 


def q92():
    initial_question="Liste des RapporteursPE 1-5 et Groupe, pour les actes NoUniqueType=COD"

    #a)NoUniqueType=COD et NbLectures=1
    #b)NoUniqueType=COD et NbLectures=2 ou 3
    nb_lec_list=((" et NbLectures=1", "act__nb_lectures"),(" et NbLectures=2 ou 3", "act__nb_lectures__gt"))
    
    for nb_lec in nb_lec_list:
        #-> par secteur
        question=initial_question+nb_lec[0]+", par secteur"
        print question
        res=init_cs(empty_dic=True)
        res=get_list_pers_cs(res, "rapp", 5, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_list_pers(question, cs_list, "CS", res, "rapp")
    
        #~ #-> par année
        question=initial_question+nb_lec[0]+", par année"
        print question
        res=init_year(empty_dic=True)
        res=get_list_pers_year(res, "rapp", 5, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_list_pers(question, years_list, "YEAR", res, "rapp")
    
        #~ #-> par secteur et par année
        question=initial_question+nb_lec[0]+", par secteur et par année"
        print question
        res=init_cs_year(empty_dic=True)
        res=get_list_pers_cs(res, "rapp", 5, year_var=True, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_list_pers_cs_year(question, res, "rapp")
