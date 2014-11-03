#-*- coding: utf-8 -*-

#queries about the nb_mots variable


def q54():
    question="Nombre de mots moyen des textes des actes, par année"
    print question
    res=init_year()
    res=get_by_year(res, variable="nb_mots")
    write_year(question, res)
    

def q55():
    question="Nombre de mots moyen des textes des actes, par secteur"
    print question
    res=init_cs()
    res=get_by_cs(res, variable="nb_mots")
    write_cs(question, res)
   

def q56():
    question="Nombre de mots moyen des textes des actes, par secteur et par année"
    print question
    res=init_cs_year()
    res=get_by_cs_year(res, variable="nb_mots")
    write_cs_year(question, res)


def nb_mots_type_acte(type_acte):
    question="Nombre de mots moyen pour les actes de type "+type_acte+", par année" 
    print question 
    res=init_year()
    res=get_by_year_variable(Act, res, {"validated": 2, "type_acte": type_acte}, "nb_mots")
    write_year(question, res)


def q63():
    type_actes=["CS DEC", "CS DVE", "CS REG", "DEC", "DVE", "REG", "CS DEC W/O ADD"]
    for type_acte in type_actes:
        nb_mots_type_acte(type_acte)
        
    
def nb_mots_type_acte_bis(type_actes):
    str_list=str(type_actes)
    question="Total nombre de mots * nombre d'actes de type "+str_list
    print question 
    nb=0
    res=0
    for act in Act.objects.filter(validated=2, type_acte__in=type_actes, nb_mots__isnull=False):
        nb+=1
        res+=act.nb_mots
    res=res*nb
    write_res(question, res)
    
    question="Total nombre de mots * nombre d'actes de type "+str_list+", par année" 
    print question 
    res=init_year()
    res=get_by_year_variable(Act, res, {"validated": 2, "type_acte__in": type_actes, "nb_mots__isnull": False}, "nb_mots")
    write_year(question, res, query="nb_mots")
    
        
def q63_bis():
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "CS DEC W/O ADD"], ["CS REG", "REG"]]
    for type_acte in type_actes:
        nb_mots_type_acte_bis(type_acte)


def nb_mots_no_unique_type(no_unique_type):
    question="Nombre de mots moyen pour les actes de NoUniqueType "+no_unique_type+", par année" 
    print question 
    res=init_year()
    res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index", "no_unique_type": no_unique_type}, "nb_mots")
    write_year(question, res)


def q64():
    no_unique_types=["COD", "CNS", "SYN", "CS"]
    for no_unique_type in no_unique_types:
        nb_mots_no_unique_type(no_unique_type)


def nb_mots_no_unique_type_bis(key, no_unique_types):
    str_list=str(no_unique_types)
    nb=0
    res=0
    if key=="include":
        txt=" = "
        nb_actes=ActIds.objects.filter(act__validated=2, src="index", no_unique_type__in=no_unique_types, act__nb_mots__isnull=False)
        for act in ActIds.objects.filter(act__validated=2, src="index", no_unique_type__in=no_unique_types, act__nb_mots__isnull=False):
            nb+=1
            res+=act.act.nb_mots
    else:
        txt=" <> "
        nb_actes=ActIds.objects.filter(act__validated=2, src="index", act__nb_mots__isnull=False).exclude(no_unique_type__in=no_unique_types)
        for act in ActIds.objects.filter(act__validated=2, src="index", act__nb_mots__isnull=False).exclude(no_unique_type__in=no_unique_types):
            nb+=1
            res+=act.act.nb_mots
    
    question="Total nombre de mots * nombre d'actes de NoUniqueType"+txt+str_list
    print question 
    
    
    res=res*nb
    write_res(question, res)
    
    res=init_year()
    question="Total nombre de mots * nombre d'actes de NoUniqueType"+txt+str_list+", par année" 
    print question 
    if key=="include":
        txt=" = "
        res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index", "no_unique_type__in": no_unique_types}, "nb_mots")
    else:
        txt=" <> "
        res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index"}, "nb_mots", exclude_vars={"no_unique_type__in": no_unique_types})
        
    write_year(question, res, query="nb_mots")
    
    
def q64_bis():
    no_unique_types={"include": ["COD"], "exclude": ["COD"]}
    for key, no_unique_type in no_unique_types.iteritems():
        nb_mots_no_unique_type_bis(key, no_unique_type)


def q83():
    #Nb de mots x Nb d’actes par année, pour les secteurs
    question="Total nombre de mots * nombre d'actes par code sectoriel et par année"
    print question 
    res=init_cs_year()
    res=get_by_cs_year(res, variable="nb_mots", filter_variables={"nb_mots__gt": 0})
    write_cs_year(question, res, query="nb_mots")

    
def nb_mots_2009(filter_variables={}, q=""):
    #Nb de mots x Nb d’actes par année, pour les secteurs
    question="Total nombre de mots * nombre d'actes de 2009, "+q+"par mois"
    print question 
    res=init_month()
    res=get_by_month(res, "nb_mots", filter_variables=filter_variables)
    write_month(question, res, query="nb_mots")
    
    
def q90_mois():
    nb_mots_2009(filter_variables={"act__releve_annee": 2009})


def q90_mois_nut():
    nb_mots_2009(filter_variables={"act__releve_annee": 2009, "no_unique_type": "COD"}, q="pour les actes de NoUniqueType=COD, ")
