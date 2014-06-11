#-*- coding: utf-8 -*-
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from forms import CSVUploadForm
from models import CSVUpload
#models
from act_ids.models import ActIds
from act.models import Act, ConfigCons, CodeSect, CodeAgenda, GvtCompo, Person, Country, Party, PartyFamily, DG, DGSigle, DGNb, NP, MinAttend
from import_app.models import ImportAdoptPC, ImportDosId, ImportNP, ImportMinAttend
from common.db import save_get_object
#manipulate csv files, path of the file to import, copy a list and use regex
import csv, os, copy, re
#cross validation functions and get data from eurlex, oeil, prelex
import get_ids
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
#model as parameter
from django.db.models.loading import get_model
#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from common.db import save_get_field_and_fk
import re


def detect_delim(header):
    """
    FUNCTION
    detect the delimiter of a csv file and return it
    PARAMETERS
    header: first line of a csv file [string]
    RETURN
    delimiter character [char]
    """
    if header.find(";")!=-1:
        #~ print "delimiter=';'"
        return ";"
    if header.find(",")!=-1:
        #~ print "delimiter=','"
        return ","
    #default delimiter (MS Office export)
    return ";"


def none_or_var(var, var_type):
    """
    FUNCTION
    return the variable or None if it contains no value
    PARAMETERS
    var: variable to test [int or string]
    var_type: type of the variable (string, int) [string]
    RETURN
    var_new: variable or None if it contains no value [int or string]
    """
    var_new=None
    if var_type=="str":
        if var.strip()!="NULL" and var.strip()!="":
            var_new=var
    elif var_type=="int":
        try:
            int(var)
            var_new=var
        except:
            pass

    return var_new


def save_2_tables(row, fields, fields_fk, party_family=""):
    """
    FUNCTION
    open a csv file and save its variables variables in 2 joined tables:
    code_sect_rep/config_cons
    code_sect_rep/code_agenda
    name/country
    name/party
    dg/dg_sigle
    PARAMETERS
    row: row to be processed (from the csv file) [list]
    fields: model name, field name and position in file (num colomn) [list]
    fields_fk: model name, field name and position in file (num colomn) for each foreign key [list of lists]
    party_family: model name, field name and position in file (num colomn) for the party_family variable
    RETURN
    msg: row main variable, used to display a success or error [string]
    exist: True if the instance already exists, False otherwise [boolean]
    """
    #~ field=["Person", "name", <position>]
    #~ fields_fk=[["Country", "country", <position>], ["Party", "party", <position>]]
    src=""
    #original lists are modified a few lines after in the program and should not be (the position is updated with the value of the field) -> use a copy of the list instead with deepcopy
    field=copy.deepcopy(fields)
    field_fk=copy.deepcopy(fields_fk)
    #the position becomes the value (in order to call the save_get_field_and_fk function)
    field[2]=row[field[2]].strip()
    #if import of responsibles (prelex) -> change name format of person: "LASTNAME, Firstname" -> "LASTNAME Firstname"
    if field[1]=="name":
        field[2]=field[2].replace(",","")
        src="resp"
    #delete the last dot for the code_sect if any
    elif field[1]=="code_sect":
        field[2]=field[2].rstrip(".")

    msg=var_name_data.var_name[field[1]]+"="+field[2]
    #for each foreign key
    for fk in field_fk:
        fk[2]=row[fk[2]].strip()
        msg+=", "+fk[1]+"="+fk[2]

    #save the field and its foreign keys
    instance, exist=save_get_field_and_fk(field, field_fk, src)

    #if dg import: we have to save dg_nb too
    if field[1]=="dg":
        dg_nb=row[2].strip()
        #if the dg has an associate number
        if dg_nb!="":
            #save or get (if already exists) the dg_nb instance
            dg_nb_instance=save_get_object(DGNb, {"dg_nb": dg_nb})
            #link it to the current dg
            instance.dg_nb.add(dg_nb_instance)
    #import party_family
    elif party_family!="":
        party_family=row[party_family[2]].strip()
        #save the party family
        try:
            PartyFamily.objects.create(party=instance.party, country=instance.country, party_family=party_family)
        except Exception, e:
            print "party_family already exists for this party and country"
        msg+=", party_family="+party_family

    return msg, exist


def import_2_tables(csv_file, fields, fields_fk, party_family=""):
    """
    FUNCTION
    open a csv file and save its variables variables in 2 joined tables:
    code_sect_rep/config_cons
    code_sect_rep/code_agenda
    name/country
    name/party
    dg/dg_sigle
    PARAMETERS
    csv_file: file to handle
    fields: model name, field name and position in file (num colomn) for each mother table [list of lists]
    fields_fk: model name, field name and position in file (num colomn) for each foreign key for each child table [list of lists of lists]
    party_family: model name, field name and position in file (num colomn) for the party_family variable
    RETURN
    rows_saved: saved rows (success) [list of strings]
    rows_not_saved: rows not saved (error) [list of strings]
    """
    #~ field=[["Party", "party", <position>], ["Person", "name", <position>]]
    #~ fields_fk=[["PartyFamily", "party_family", <position>], [["Country", "country", <position>], ["Party", "party", <position>]]]
    rows_saved=[]
    rows_not_saved=[]
    with open(csv_file, 'r') as csv_file_temp:
        #detect delimiter and skip header
        delimiter=detect_delim(csv_file_temp.readline())
        reader=csv.reader(csv_file_temp, delimiter=delimiter)

        for row in reader:
            #for each mother and child(ren) tables
            for index in xrange(len(fields)):
                msg, exist=save_2_tables(row, fields[index], fields_fk[index], party_family)

            #errors management
            if exist:
                msg_error="The row "+msg+" already exists!!"
                rows_not_saved.append(msg_error)
            else:
                rows_saved.append(msg)

    return rows_saved, rows_not_saved


def save_adopt_cs_pc(instance, field, values):
    """
    FUNCTION
    save the coutries for adopt_cs_contre, adopt_cs_abs, adopt_pc_contre or adopt_pc_abs
    PARAMETERS
    instance: instance of the act [Act model instance]
    field: name  of the field (adopt_cs_contre, adopt_cs_abs, adopt_pc_contre or adopt_pc_abs) [string]
    values: countries [list of strings]
    RETURN
    None
    """
    #countries separated by a comma or a semi-column
    values=re.split(';|,',values)
    #the instance must have an id to add many to many fields
    #~ instance.save()
    for value in values:
        if value!="":
            field_instance=getattr(instance, field)
            try:
                field_instance.add(Country.objects.get(pk=value.strip()))
            except Exception, e:
                print field+" already exists!"


def get_error_msg(ids_row):
    """
    FUNCTION
    return the text of the error msg (if the row already exists when importing a file)
    PARAMETERS
    ids_row: fields that identify the row [dictionary]
    RETURN
    msg: id of the row, used to display an error message [string]
    """
    msg=""
    for field in ids_row:
        try:
            name=var_name_data.var_name[field]
        except Exception, e:
            name=var_name_ids.var_name[field]
        msg+=name+"="+str(ids_row[field])+", "
    return msg[:-2]


def get_data_dos_id(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of ImportDosId
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [ImportDosId model instance]
    msg: id of the row, used to display an error message [string]
    exist (not created): True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["dos_id"]=int(row[0])
    if row[1].strip()!="":
        ids_row["no_celex"]=row[1].strip()
    else:
        ids_row["no_celex"]=row[2].strip()

    instance, created = ImportDosId.objects.get_or_create(**ids_row)
    msg=get_error_msg(ids_row)

    #exist and created are opposite boolean
    return instance, msg, not created


def get_data_act(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of Act
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [Act model instance]
    msg: id of the row, used to display an error message [string]
    exist: True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["releve_annee"]=int(row[0])
    ids_row["releve_mois"]=int(row[1])
    ids_row["no_ordre"]=int(row[2])
    #check that the no_celex does not already exist
    try:
        act_ids=ActIds.objects.get(no_celex=row[7].strip(), src="index")
        #there is already one act with the same no_celex -> error
        instance=None
        ids=str(ids_row["releve_annee"])+", "+str(ids_row["releve_mois"])+", "+str(ids_row["no_ordre"])
        msg=ids+" cannot be saved because the act has already been imported or "+var_name_ids.var_name["no_celex"]
        exist=True
    except Exception, e:
        print "no_celex does not exist yet", e

        #extra fields to save if the act does not exist yet
        defaults={}
        defaults["titre_rmc"]=row[3].strip()
        defaults["adopt_cs_regle_vote"]=row[4].strip()
        if row[14].strip()=="Y":
            defaults["split_propos"]=True
        if row[15].strip()=="Y":
            defaults["suite_2e_lecture_pe"]=True
        council_path=row[16].strip().strip(".")
        if council_path!="":
            defaults["council_path"]=council_path
        defaults["notes"]=row[17].strip()
        attendance_pdf=row[18].strip().strip(".").lower()
        if attendance_pdf not in ["", "na"]:
            defaults["attendance_pdf"]=attendance_pdf

        #get instance or create instance if does not already exist
        instance, created = Act.objects.get_or_create(defaults=defaults, **ids_row)
        exist=not created

        #if the act didn't exist, save the related models
        if not exist:
            save_adopt_cs_pc(instance, "adopt_cs_abs", row[5])
            save_adopt_cs_pc(instance, "adopt_cs_contre", row[6])

            #act_ids
            act_ids=ActIds()
            act_ids.src="index"
            act_ids.act=instance
            #if no_celex already exists, the ActIds instance will be updated
            act_ids.no_celex=row[7].strip()
            act_ids.propos_annee=none_or_var(row[8], "int")
            act_ids.propos_chrono=none_or_var(row[9].replace(" ", ""), "str")
            act_ids.propos_origine=none_or_var(row[10], "str")
            act_ids.no_unique_annee=none_or_var(row[11], "int")
            act_ids.no_unique_type=none_or_var(row[12], "str")
            act_ids.no_unique_chrono=none_or_var(row[13], "str")

            #save act_ids
            act_ids.save()

            #success (row saved): get the ids of the act to retrieve the ids on eurlex, oeil and prelex
            msg=ids_row
        else:
            #error message
            msg=get_error_msg(ids_row)

    return instance, msg, exist


def get_save_act_ids(acts_ids):
    """
    FUNCTION
    get and save retrieved ids from eurlex, oeil and prelex in the the database (import or update act ids)
    PARAMETERS
    acts_ids: list of act ids to save (monthly summary ids) [list of dictionaries of releve_* variables]
    RETURN
    None
    """
    fields={}
    for releves in acts_ids:
        act=Act.objects.get(**releves)

        act_ids={}
        #get or create the act ids instance for each source
        for src in ["index", "eurlex", "oeil", "prelex"]:
            act_ids[src]=save_get_object(ActIds, {"act": act, "src": src})

        #get ids
        #eurlex
        act_ids["eurlex"].__dict__.update(get_ids.check_get_ids_eurlex(act_ids["index"].no_celex))
        #~ act_ids["eurlex"].__dict__.update(get_ids.check_get_ids_eurlex(act_ids["index"].no_celex))

        #oeil
        act_ids["oeil"].__dict__.update(get_ids.check_get_ids_oeil(act_ids["index"].no_unique_type, str(act_ids["index"].no_unique_annee), act_ids["index"].no_unique_chrono))
        #~ act_ids["oeil"].__dict__.update(get_ids.check_get_ids_oeil(act_ids["index"].no_unique_type, str(act_ids["index"].no_unique_annee), act_ids["index"].no_unique_chrono))

        #prelex
        ids={}
        #url: try with dos_id
        if act_ids["index"].dos_id!=None:
            ids['dos_id']=str(act_ids["index"].dos_id)
        #no propos_chrono? is it a split proposition?
        elif act_ids["index"].propos_chrono==None or "-" in act_ids["index"].propos_chrono:
            #try with the oeil ids
            ids['no_unique_type']=act_ids["index"].no_unique_type
            ids['no_unique_annee']=act_ids["index"].no_unique_annee
            ids['no_unique_chrono']=act_ids["index"].no_unique_chrono
        else:
            #prelex ids
            ids['propos_origine']=act_ids["index"].propos_origine
            ids['propos_annee']=act_ids["index"].propos_annee
            ids['propos_chrono']=act_ids["index"].propos_chrono

        prelex_ids, act.url_prelex=get_ids.check_get_ids_prelex(ids, act_ids["index"].no_celex)
        #save prelex url
        act.save()
        act_ids["prelex"].__dict__.update(prelex_ids)

        #save ids
        for src in act_ids:
            act_ids[src].save()


def get_data_adopt_pc(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of ImportAdoptPC
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [ImportAdoptPC model instance]
    msg: id of the row, used to display an error message [string]
    exist (not created): True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["releve_annee"]=int(row[0])
    ids_row["releve_mois"]=int(row[1])
    ids_row["no_ordre"]=int(row[2])

    #extra fields to save if the act does not exist yet
    defaults={}
    defaults["adopt_pc_abs"]=row[3]
    defaults["adopt_pc_contre"]=row[4]

    instance, created = ImportAdoptPC.objects.get_or_create(defaults=defaults, **ids_row)
    msg=get_error_msg(ids_row)


    #TEMPORARY: update with no_celex
    #~ instance.no_celex=row[5].strip()
    #~ instance.save();


    #exist and created are opposite boolean
    return instance, msg, not created



def get_data_gvt_compo(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of GvtCompo
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [GvtCompo model instance]
    msg: id of the row, used to display an error message [string]
    exist: True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["start_date"]=row[0].strip().replace("/", "-")
    ids_row["end_date"]=row[1].strip().replace("/", "-")

    #extra fields to save if the act does not exist yet
    defaults={}
    gvt_compos=row[2].split(":")
    defaults["country"]=Country.objects.get(country_code=gvt_compos[0].strip())

    #get instance or create instance if does not already exist
    instance, created = GvtCompo.objects.get_or_create(defaults=defaults, **ids_row)
    exist=not created

    #if the row didn't exist, save the related models
    #2009-avril-09  2010-juin-27    CZ: none
    if not exist and gvt_compos[1].strip()!="none":
        #split party and party_family
        partys_temp=gvt_compos[1].split(",")
        partys=[]
        partys_family=[]
        for party in partys_temp:
            string=re.findall("[^()]+", party)
            partys.append(string[0].strip())
            partys_family.append(string[1].strip())

        #save party and party_family
        data={}
        data["country"]=defaults["country"]
        for index in xrange(len(partys)):
            #save party
            data["party"]=save_get_object(Party, {"party": partys[index]})
            instance.party.add(data["party"])

            data["party_family"]=partys_family[index]
            if data["party_family"]=="Conservative/ Christian Democracy":
                data["party_family"]="Conservative/Christian Democracy"
            #save party_family
            save_get_object(PartyFamily, data)
            #~ PartyFamily.objects.get_or_create(defaults={"party_family": party_family}, **data)

    msg=get_error_msg(ids_row)
    return instance, msg, exist



def get_data_np(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of ImportNP
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [ImportNP model instance]
    msg: id of the row, used to display an error message [string]
    exist (not created): True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["case_nb"]=int(row[0])

    #extra fields to save if the act does not exist yet
    defaults={}
    defaults["no_celex"]=row[1].strip()
    defaults["np"]=row[2].strip()
    defaults["act_type"]=row[3].strip()
    act_date=row[4].strip().replace("/", "-")
    if act_date!="NULL":
        defaults["act_date"]=act_date

    #get instance or create instance if does not already exist
    instance, created = ImportNP.objects.get_or_create(defaults=defaults, **ids_row)

    msg=get_error_msg(ids_row)
    return instance, msg, not created



def get_data_min_attend_insert(row):
    """
    FUNCTION
    get a string (row from csv file) and put its content into an instance of ImportMinAttend
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [ImportMinAttend model instance]
    msg: id of the row, used to display an error message [string]
    exist (not created): True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["no_celex"]=row[3].strip()
    ids_row["country"]=row[4].strip()
    ids_row["verbatim"]=row[6].strip()

    #extra fields to save if the act does not exist yet
    defaults={}
    defaults["releve_annee"]=int(row[0])
    defaults["releve_mois"]=int(row[1])
    defaults["no_ordre"]=int(row[2])
    defaults["status"]=row[5].strip()
    defaults["validated"]=True

    #get instance or create instance if does not already exist
    instance, created = ImportMinAttend.objects.get_or_create(defaults=defaults, **ids_row)

    msg=get_error_msg(ids_row)
    return instance, msg, not created


def get_data_min_attend_update(row):
    """
    FUNCTION
    update ImportMinAttend and MinAttend for a specific act
    PARAMETERS
    row: row from the csv file [row object]
    RETURN
    instance: instance of the model with the extracted data [ImportMinAttend model instance]
    msg: id of the row, used to display an error message [string]
    exist (not created): True if the instance already exists, False otherwise [boolean]
    """
    #used to identify the row
    ids_row={}
    ids_row["no_celex"]=row[0].strip()
    country=row[1].strip()
    #we need the country code
    if len(country)>2:
        country=Country.objects.get(country=country).country_code
    ids_row["country"]=country

    #extra fields to save if the act does not exist yet
    defaults={}
    defaults["status"]=row[2].strip()
    defaults["validated"]=True

    try:
        if row[3].strip()=="":
            raise Exception("empty verbatim")
        ids_row["verbatim"]=row[3].strip()
    except Exception, e:
        print "no verbatim has been entered", e
        #AB or NA
        ids_row["verbatim"]=defaults["status"]

    #get the releve_ids
    try:
        act=ActIds.objects.get(src="index", no_celex=ids_row["no_celex"]).act
        defaults["releve_annee"]=act.releve_annee
        defaults["releve_mois"]=act.releve_mois
        defaults["no_ordre"]=act.no_ordre
    except Exception, e:
        print "the act does not exist yet", e


    #get instance or create instance if does not already exist
    instance, created = ImportMinAttend.objects.get_or_create(defaults=defaults, **ids_row)


    msg=get_error_msg(ids_row)
    return instance, msg, not created


def import_table(csv_file, import_type):
    """
    FUNCTION
    open a csv file and save its variables in the database (in one table )
    used for dos_id (ImportDosId) , act (Act), adopt_pc (ImportAdoptPC), gvt_compo (GvtCompo), np (Opal) and min_attend (ImportMinAttend)
    PARAMETERS
    csv_file: file to handle [file object]
    import_type: type of the file to import [string]
    RETURN
    rows_saved: saved rows (success) [list of strings]
    rows_not_saved: rows not saved (error) [list of strings]
    """
    rows_saved=[]
    rows_not_saved=[]
    with open(csv_file, 'r') as csv_file_temp:
        #detect delimiter and skip header
        header=csv_file_temp.readline()
        #skip empty lines at the beginning of the file
        while header.strip()=="":
            header=csv_file_temp.readline()
        delimiter=detect_delim(header)
        reader=csv.reader(csv_file_temp, delimiter=delimiter)

        min_attend_update_set=set()

        for row in reader:
            print "row", row
            #delete previous records
            if import_type=="min_attend_update":
                no_celex=row[0].strip()
                if no_celex not in min_attend_update_set:
                    #list of unique no_celex
                    min_attend_update_set.add(no_celex)
                    try:
                        acts=ImportMinAttend.objects.filter(no_celex=no_celex)

                        act=ActIds.objects.get(src="index", no_celex=no_celex).act
                        #delete previous MinAttend instances
                        for min_attend in MinAttend.objects.filter(act=act):
                            print "MinAttend deletion", min_attend.act
                            min_attend.delete()

                        #delete previous ImportMinAttend instances
                        for act in acts:
                            print "ImportMinAttend deletion", act.no_celex
                            act.delete()

                    except Exception, e:
                        print "the act does not exist yet", e

            #according to the type of import, extract the content of the row and put it in an object
            instance, msg, exist=eval("get_data_"+import_type)(row)
            #if the row has already been imported
            if exist:
                error="The row " + str(msg) + " already exists!!"
                rows_not_saved.append(error)
            else:
                #new record or update
                instance.save()
                rows_saved.append(msg)

    return rows_saved, rows_not_saved


def help_text(request):
    """
    VIEW
    displays the help text for the selected import in the import page (called with ajax only)
    TEMPLATES
    import/help_text.html
    """
    response={}
    form=CSVUploadForm(request.user, request.POST)
    response['form']=form
    response['display_name']=var_name_ids.var_name
    response['display_name'].update(var_name_data.var_name)

    return HttpResponse(render_to_string('import/help_text.html', response, RequestContext(request)))


@login_required
def import_view(request):
    """
    VIEW
    displays and processes the import page
    TEMPLATES
    import/index.html
    """
    response={}
    #template path to the help text div
    response["help_text_template"]='import/help_text.html'
    response['display_name']=var_name_ids.var_name
    response['display_name'].update(var_name_data.var_name)
    if request.method=='POST':
        form=CSVUploadForm(request.user, request.POST, request.FILES)
        #the form is valid and the import can be processed
        if form.is_valid():
            print "csv import"
            file_to_import=form.cleaned_data['file_to_import']
            file_name_new=" ".join(request.FILES['csv_file'].name.split())
            path=settings.MEDIA_ROOT+"/import/"+file_name_new
            #if a file with the same name already exists, we delete it
            if os.path.exists(path):
                os.remove(path)
            csv_file=CSVUpload(csv_file=request.FILES['csv_file'])
            csv_file.save()
            rows_saved=[]
            rows_not_saved=[]

            #importation of dos_id, act, adopt_pc, gvt_compo, np or min_attend file
            if file_to_import in ["dos_id","act","adopt_pc","gvt_compo", "np", "min_attend_insert", "min_attend_update"]:
                rows_saved, rows_not_saved=import_table(path, file_to_import)
                if file_to_import=="act":
                    #save retrieved ids
                    get_save_act_ids(rows_saved)
            #importation of config_cons or code_agenda
            elif file_to_import in["config_cons", "code_agenda"]:
                #model name, field name, position in the csv file
                field=[CodeSect, "code_sect", 0]
                #config_cons->ConfigCons
                if file_to_import=="config_cons":
                    model=ConfigCons
                else:
                    model=CodeAgenda
                fields_fk=[model, str(file_to_import), 1]
                rows_saved, rows_not_saved=import_2_tables(path, [field], [[fields_fk]])
            #importation of dg, dg_sigle, dg_nb
            elif file_to_import=="dg":
                #model name, field name, position in the csv file
                field=[DG, file_to_import, 0]
                fields_fk=[DGSigle, "dg_sigle", 1]
                rows_saved, rows_not_saved=import_2_tables(path, [field], [[fields_fk]])
            #importation of person
            elif file_to_import=="name":
                field=[]
                #person
                field.append([Person, file_to_import, 0])

                #party_family
                party_family=[PartyFamily, "party_family", 2]
                fields_fk=[]
                #country
                fields_fk.append([Country, "country", 3])
                #party
                fields_fk.append([Party, "party", 1])

                rows_saved, rows_not_saved=import_2_tables(path, field, [fields_fk], party_family)

            response['errors']=rows_not_saved
            response['msg']=str(len(rows_saved)) + " raw(s) imported, "+ str(len(rows_not_saved)) +" error(s)!"
            response["msg_class"]="success_msg"

        #validation errors
        else:
            if 'iframe' in request.POST:
                print "form.errors"
                response['form_errors']= dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items()])
            else:
                response['form']=form

        #if ajax
        if 'iframe' in request.POST:
            return HttpResponse(simplejson.dumps(response), mimetype="application/json")

    #unbound forms
    if "form" not in response:
        response['form']=CSVUploadForm(request.user)

    #displays the page (GET) or POST if javascript disabled
    return render_to_response('import/index.html', response, context_instance=RequestContext(request))
