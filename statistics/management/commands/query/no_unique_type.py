#-*- coding: utf-8 -*-

#queries about the no_unique_type variable

#import general steps common to each query
from  ..init import *
from  ..get import *
from  ..write import *

    
def q62(cs, name):
    question="Pourcentages d'actes NoUniqueType=COD adoptés en 1ère lecture en fonction du nombre de base juridiques et du code sectoriel"
    print question
    #first line: 1 BJ; second line: many BJ
    #first column: only one cs (13); second column: all cs
    #first zero: nb acts; second_zero: total
    res=[[[0,0],[0,0]], [[0,0],[0,0]]]
    #~ count=0     

    for act_ids in ActIds.objects.filter(act__validated=2, src="index"):
        act=act_ids.act
        if act.base_j.strip()!="":
            nb_bj=act.base_j.count(';')
            #if more than one BJ, assignate to "many BJ" catageory
            if nb_bj>0:
                nb_bj=1
            
            if act.releve_annee==2004 and act.releve_mois==3 and act.no_ordre==36:
                print "nb_bj", nb_bj
       
            #for specific cs in parameter
            nb_cs=1
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None and get_cs(code_sect.code_sect)==cs:
                    nb_cs=0
                    break
                    
            #count total
            res[nb_bj][nb_cs][1]+=1
            if nb_cs==0:
                #if the act has a code sectoriel="13", it has to be counted for the "all cs" column too
                res[nb_bj][1][1]+=1
            
            #count number of acts
            if act_ids.no_unique_type=="COD" and act.nb_lectures==1:
                res[nb_bj][nb_cs][0]+=1
                if nb_cs==0:
                    #if the act has a code sectoriel="13", it has to be counted for the "all cs" column too
                    res[nb_bj][1][0]+=1
                
    print "res", res
    #~ print "count", count
    
    writer.writerow([question])
    writer.writerow(["", "CS="+name, "Tous les CS"])
    for nb_bj in range(2):
        if nb_bj==0:
            row=["Une BJ"]
        else:
            row=["Plusieurs BJ"]
        for nb_cs in range(2):
            if res[nb_bj][nb_cs][0]==0:
                temp=0
            else:
                temp=round(float(res[nb_bj][nb_cs][0])*100/res[nb_bj][nb_cs][1], 3)
            row.append(temp)
        writer.writerow(row)
    writer.writerow("")
    print ""


def q98():
    #Pourcentage d’actes adoptés avec NoUniqueType=COD 1/et NbLectures=1, 2/et NbLectures=2, par année, par secteur, par année et par secteur
    variables={1: "1ère lecture", 2: "2ème lecture"}
    filter_vars={"act__nb_lectures__isnull": False}
    check_vars_act_ids={"no_unique_type": "COD"}
    
    for key, value in variables.iteritems():
        check_vars_act={"nb_lectures": key}
        
        question="Pourcentage d'actes NoUniqueType=COD adoptés en "+value+" par secteur"
        print question
        res=init_cs()
        res=get_by_cs(res, Model=ActIds, filter_vars=filter_vars, check_vars_act=check_vars_act, check_vars_act_ids=check_vars_act_ids)
        write_cs(question, res)

        question="Pourcentage d'actes NoUniqueType=COD adoptés en "+value+" par année"
        print question
        res=init_year()
        res=get_by_year(res, Model=ActIds, filter_vars=filter_vars, check_vars_act=check_vars_act, check_vars_act_ids=check_vars_act_ids)
        write_year(question, res)

        question="Pourcentage d'actes NoUniqueType=COD adoptés en "+value+" par année et par secteur"
        print question
        res=init_cs_year()
        res=get_by_cs_year(res, Model=ActIds, filter_vars=filter_vars, check_vars_act=check_vars_act, check_vars_act_ids=check_vars_act_ids)
        write_cs_year(question, res)
