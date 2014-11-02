#write the result of the query in a csv file


def write_res(question, res):
    writer.writerow([question])
    writer.writerow([res])
    writer.writerow("")
    print res
    print ""


def write_cs(question, res, nb_vars=2, percent=100):
    writer.writerow([question])
    writer.writerow(cs_list)
    row=[]
    for cs in cs_list:
        if nb_vars==2:    
            if res[cs][0]==0:
                temp=0
            else:
                temp=round(float(res[cs][0])*percent/res[cs][1], 3)
        else:
            temp=res[cs]
        row.append(temp)
    writer.writerow(row)
    writer.writerow("")
    print ""
    

def write_year(question, res, nb_vars=2, percent=100, bj=False, query=""):
    writer.writerow([question])
    row=[]
    if not bj:
        writer.writerow(years_list)
        for year in years_list: 
            #compute avg or percentage (two variables: total and number)
            if nb_vars==2: 
                if res[year][0]==0:
                    temp=0
                else:
                    #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                    if query=="nb_mots":
                        res[year][1]=float(1)/res[year][1]
                    temp=round(float(res[year][0])*percent/res[year][1], 3) 
            else:
                #no avg to compute
                temp=res[year]
            row.append(temp)
        writer.writerow(row)
    else:
        #nb=2, display two lines with two variables
        writer.writerow(years_list_zero)
        for nb in range(nb_var):
            if nb==0:
                row=["Une BJ"]
            else:
                row=["Plusieurs BJ"]
            
            for year in years_list:
                if res[year][nb]==0:
                    temp=0
                else:
                    total=res[year][0]+res[year][1]
                    temp=round(float(res[year][nb])*100/total, 3) 
                row.append(temp)
            writer.writerow(row)
        
    writer.writerow("")
    print ""


def write_month(question, res, percent=1, nb_vars=1, query=""):
    #nb=2: counter of nb acts concerned
    writer.writerow([question])
    writer.writerow(months_list)
    row=[]
    for month in months_list:
        if nb_vars==1:
            res_month=res[month]
        elif nb_vars==2:
            if res[month][0]==0:
                res_month=0
            else:
                #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                if query=="nb_mots":
                    res[month][1]=float(1)/res[month][1]
                res_month=round(float(res[month][0])*percent/res[month][1],3)
        row.append(res_month)
        
    writer.writerow(row)
    writer.writerow("")
    print ""


def write_cs_year(question, res, nb_vars=2, percent=100, total_year=False, amdt=False, query=""):
    #nb=2: counter of nb acts concerned
    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            if total_year:
                if amdt:
                    #display sum of each year for amdt
                    res_year=res[cs][year][0]
                else:
                    if res[cs][year]==0:
                        res_year=0
                    else:
                        res_year=round(float(res[cs][year])*percent/total_year[year],3)
            else:
                if nb_vars==1:
                    res_year=res[cs][year]
                elif nb_vars==2:
                    if res[cs][year][0]==0:
                        res_year=0
                    else:
                        #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                        if query=="nb_mots":
                            res[cs][year][1]=float(1)/res[cs][year][1]
                        res_year=round(float(res[cs][year][0])*percent/res[cs][year][1],3)
            row.append(res_year)
        writer.writerow(row)
    #write sum each column
    if amdt:
        row=["Total"]
        for year in years_list:
            row.append(total_year[year])
        writer.writerow(row)
    writer.writerow("")
    print ""



def write_list_pers(question, the_list, element, res, pers_type):
    #crosses cs OR year
    #element: cs OR year
    writer.writerow([question])
    for value in the_list:
        writer.writerow("")
        writer.writerow([element+" "+value])
        if pers_type=="resp":
            writer.writerow(["RespPropos", "PartyFamily", "NationRespPropos", "nb"])
            for resp in res[value]:
                try:
                    country=resp.country
                    pf=PartyFamily.objects.get(country=country, party=resp.party).party_family.encode("utf-8")
                    name=resp.name.encode("utf-8")
                    writer.writerow([name, pf, country.country_code, res[value][resp]])
                except Exception, e:
                    print "pb encoding resp", e
        else:
            writer.writerow(["RapporteursPE", "GroupRapporteurPE", "nb"])
            for rapp in res[value]:
                try:
                    name=rapp.name.encode("utf-8")
                    party=rapp.party.party.encode("utf-8")
                    writer.writerow([name, party, res[value][rapp]])
                except Exception, e:
                    print "pb encoding rapp", e
    writer.writerow("")
    print ""


def write_list_pers_cs_year(question, res, pers_type):
    writer.writerow([question])
    for cs in cs_list:
        writer.writerow("")
        writer.writerow(["CS "+cs])
        for year in years_list:
            writer.writerow(["YEAR "+year])
            if pers_type=="resp":
                writer.writerow(["RespPropos", "PartyFamily", "NationRespPropos", "nb"])
                for resp in res[cs][year]:
                    try:
                        country=resp.country
                        pf=PartyFamily.objects.get(country=country, party=resp.party).party_family.encode("utf-8")
                        name=resp.name.encode("utf-8")
                        writer.writerow([name, pf, country.country_code, res[cs][year][resp]])
                    except Exception, e:
                        print "pb encoding resp", e
            else:
                writer.writerow(["RapporteursPE", "GroupRapporteurPE", "nb"])
                for rapp in res[cs][year]:
                    try:
                        name=rapp.name.encode("utf-8")
                        party=rapp.party.party.encode("utf-8")
                        writer.writerow([name, party, res[cs][year][rapp]])
                    except Exception, e:
                        print "pb encoding rapp", e
        writer.writerow("")
    writer.writerow("")
    print ""


def write_percent_pf(question, the_list, element, res, pers_type):
    #crosses cs OR year
    #element: cs OR year
    writer.writerow([question])
    for value in the_list:
        writer.writerow("")
        writer.writerow([element+" "+value])
        writer.writerow(["PartyFamily "+pers_type, "percentage"])
        for pf in res[value]:
            if pf!="total":
                if res[value][pf]==0:
                    res_pf=0
                else:
                    res_pf=round(float(res[value][pf])*100/res[value]["total"],3)
                writer.writerow([pf, res_pf])
    writer.writerow("")
    print ""

     


def write_percent_pf_cs_year(question, res, pers_type):
    writer.writerow([question])
    for cs in cs_list:
        writer.writerow("")
        writer.writerow(["CS "+cs])
        for year in years_list:
            writer.writerow(["YEAR "+year])
            writer.writerow(["PartyFamily "+pers_type, "percentage"])
            for pf in res[cs][year]:
                if pf!="total":
                    if res[cs][year][pf]==0:
                        res_pf=0
                    else:
                        res_pf=round(float(res[cs][year][pf])*100/res[cs][year]["total"],3)
                    writer.writerow([pf, res_pf])
          
        writer.writerow("")
    writer.writerow("")
    print ""
