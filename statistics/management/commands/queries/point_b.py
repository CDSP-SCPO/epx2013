#queries about the nb_point_b variable



def q60():
    question="Nombre de discussions en point b"
    nb_bj_cs("13", "Marché intérieur", "nb_point_b", "int", question)

      

def q65():
    question="Nombre total de points B par année" 
    print question 
    res=init_year(nb_vars=1)
    res=get_by_year(res, "nb_point_b", excluded_values=[None, 0], nb_vars=1)
    write_year(question, res, nb_vars=1)
    
    
def q66():
    question="Nombre total de points B par secteur" 
    print question 
    res=init_cs(nb_vars=1)
    res=get_by_cs(res, "nb_point_b", excluded_values=[None, 0], nb_vars=1)
    write_cs(question, res, nb_vars=1)
    
    
def q67():
    question="Nombre total de points B par année et par secteur" 
    print question 
    res=init_cs_year()
    res=get_by_cs_year(res, variable="nb_point_b", excluded_values=[None, 0], nb_vars=1)
    write_cs_year(question, res)
    
    
def q68():
    question="Nombre total de points B pour les actes avec un vote public, par année"
    print question 
    res=init_year(nb_vars=1)
    res=get_by_year(res, "nb_point_b", excluded_values=[None, 0], nb_vars=1, filter_variables={"vote_public": True})
    write_year(question, res, nb_vars=1)
  
    
    
def q69():
    question="Nombre total de points B pour les actes avec un vote public, par secteur"
    print question 
    res=init_cs(nb_vars=1)
    res=get_by_cs(res, "nb_point_b", excluded_values=[None, 0], nb_vars=1, filter_variables={"vote_public": True})
    write_cs(question, res, nb_vars=1)



def q70():
    question="Nombre total de points B pour les actes avec un vote public, par année et par secteur"
    print question 
    res=init_cs_year()
    res=get_by_cs_year(res, variable="nb_point_b", excluded_values=[None, 0], nb_vars=1, filter_variables={"vote_public": True})
    write_cs_year(question, res)


def q73():
    question="Nombre moyen de points B"
    filter_variables={"nb_point_b__gte": 1}
    queries_periodes(question, Act, filter_variables=filter_variables, filter_total=filter_variables, avg_variable="nb_point_b", percent=1)
