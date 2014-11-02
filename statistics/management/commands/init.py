#initiate dictionary that will contain the result of a query



def init_cs(nb_vars=2, total=False, empty_list=False, empty_dic=False):
    #nb_vars=2 for computation percents
    res={}
    for cs in cs_list:
        if empty_dic:
            #list of persons, key: pers object; value: nb of occurences
            temp=dict({})
        elif empty_list:
            temp=list([[]*nb_vars])
        elif nb_vars==2:
            temp=[0,0]
        else:
            temp=0
        res[cs]=temp
        if empty_dic and total:
            res[cs]["total"]=0
    return res

    
def init_year(nb_vars=2, total=False, empty_list=False, empty_dic=False):
    """
    empty_dic: for list of persons
    """
    res={}
    for year in years_list:
        if empty_dic:
            #list of persons, key: pers object; value: nb of occurences
            temp=dict({})
        elif empty_list:
            temp=list([[]*nb_vars])
        elif nb_vars==2:
            temp=[0,0]
        else:
            temp=0
        res[year]=temp
        if empty_dic and total:
            res[year]["total"]=0
    return res


def init_month(nb_vars=2):
    res={}
    for month in months_list:
        if nb_vars==2:
            temp=[0,0]
        else:
            temp=0
        res[month]=temp
    return res


def init_cs_year(nb_vars=2, total=False, amdt=False, empty_list=False, empty_dic=False):
    #use nb=2 to compute the percentage for each cell
    #use total=True to compute the percentage of each cell compared to the total of the year
    #titles_list: initialize empty list
    res={}
    total_year={}
    for secteur in cs_list:
        res[secteur]={}
        for year in years_list:
            if empty_dic:
                #list of persons, key: pers object; value: nb of occurences
                temp=dict({})
            elif empty_list:
                temp=list([[]*nb_vars])
            elif nb_vars==2:
                temp=[0,0]
            else:
                temp=0
    
            if total:
                if amdt==True:
                    total_year[year]=0
                else:
                    total_year[year]=temp
            res[secteur][year]=temp
            if total and empty_dic:
                res[secteur][year]["total"]=0
            
            #ATTENTION! If nb=2 and total=True, the same list temp=[0,0] is used for total_year and res -> MUST USE A COPY OF THE LIST
    #~ print "res"
    #~ print res
    if total and not empty_dic:
        return res, total_year
    return res


def str_to_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()
