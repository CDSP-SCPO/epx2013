#-*- coding: utf-8 -*-

#queries about the type_acte variable

def nb_actes_type_acte(question_types, types):
    question="Nombre de "+question_types+", pour certains secteurs, par année"
    print question 
    res=init_cs_year()
    res=get_by_cs_year(res, count=False, filter_variables={"type_acte__in": types})
    write_cs_year(question, res)

        
def q85():
    question_types="CS DVE+DVE"
    types=["CS DVE", "DVE"]
    nb_actes_type_acte(question_types, types)


def q86():
    question_types="CS REG+REG"
    types=["CS REG", "REG"]
    nb_actes_type_acte(question_types, types)
    

    
def q87():
    question_types="CS DEC+DEC+CS DEC W/O ADD"
    types=["CS DEC", "DEC", "CS DEC W/O ADD"]
    nb_actes_type_acte(question_types, types)
