#-*- coding: utf-8 -*-
import csv
from django.db.models.loading import get_model
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.template import RequestContext
#data to export coming from the two main models ActIds and Act
from act_ids.models import ActIds
from act.models import *
#for the export
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import mimetypes
#change variable names (first row of the csv file)
import act_ids.var_name_ids  as var_name_ids
import act.var_name_data  as var_name_data
#redirect to login page if not logged or does not belong to authorized group
from django.contrib.auth.decorators import login_required, user_passes_test
from common.db import is_member

#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse
#display processing time
import time


def get_headers(excl_fields_act_ids, excl_fields_act):
    """
    FUNCTION
    get the headers of the fields to export (csv file)
    PARAMETERS
    excl_fields_act_ids: fields not to be exported (ActIds) [list of strings]
    excl_fields_act:  fields not to be exported (Act) [list of strings]
    RETURNS
    headers: name of the fields to be saved in the csv file [list of strings]
    """
    headers=[]
    #ActIds
    for field in ActIds()._meta.fields:
        if field.name not in excl_fields_act_ids:
            headers.append(var_name_ids.var_name[field.name])

    #Act
    for field in Act()._meta.fields:
        if field.name not in excl_fields_act:
            headers.append(var_name_data.var_name[field.name])
            #CodeSect and related
            if "code_sect_" in field.name:
                index=field.name[-1]
                headers.append(var_name_data.var_name["code_agenda_"+index])
            #Rapporteurs (Person) and related (oeil)
            elif "rapp_" in field.name:
                index=field.name[-1]
                headers.append(var_name_data.var_name["rapp_country_"+index])
                headers.append(var_name_data.var_name["rapp_party_"+index])
            #Responsibles (Person) and related (prelex)
            elif "resp_" in field.name:
                index=field.name[-1]
                headers.append(var_name_data.var_name["resp_country_"+index])
                headers.append(var_name_data.var_name["resp_party_"+index])
                headers.append(var_name_data.var_name["resp_party_family_"+index])
            #DG and related
            elif "dg_" in field.name:
                index=field.name[-1]
                headers.append(var_name_data.var_name["dg_sigle_"+index])

    #Act many to many fields
    for field in Act()._meta.many_to_many:
        if field.name not in excl_fields_act:
            #GvtCompo: country, party and party_family variable
            if "gvt_compo"==field.name:
                headers.append(var_name_data.var_name[field.name+"_country"])
                headers.append(var_name_data.var_name[field.name+"_party"])
                headers.append(var_name_data.var_name[field.name+"_party_family"])
            else:
                #AdoptPC and AdoptCS variables
                headers.append(var_name_data.var_name[field.name])

    #NP (opal)
    for field in NP()._meta.fields:
        if field.name!="act":
            headers.append(var_name_data.var_name[field.name])

    #Ministers' attendance fields
    headers.append(var_name_data.var_name["country_min_attend"])
    headers.append(var_name_data.var_name["verbatim_min_attend"])
    headers.append(var_name_data.var_name["status_min_attend"])

    return headers


#SLOW
def get_validated_acts(excl_fields_act_ids, excl_fields_act):
    """
    FUNCTION
    return all the validated acts of the model
    PARAMETERS
    excl_fields_act_ids: fields not to be exported (ActIds) [list of strings]
    excl_fields_act: fields not to be exported (Act) [list of strings]
    RETURNS
    acts: validated acts and relative data [list of Act model instances]
    """
    tic=time.time()
    
    #querysets
    qs_act=Act.objects.defer("id",  'date_doc', "url_prelex", "validated", "validated_attendance").filter(validated=2).prefetch_related("gvt_compo", "adopt_cs_contre", "adopt_cs_abs", "adopt_pc_contre", "adopt_pc_abs").prefetch_related("gvt_compo__party")
    qs_actids=ActIds.objects.defer("id", 'src', "url_exists", 'act').filter(src="index")
    qs_cs=CodeSect.objects.all().prefetch_related("code_agenda", "config_cons")
    qs_pers=Person.objects.all()
    qs_party=Party.objects.all()
    qs_pf=PartyFamily.objects.all()
    qs_dg=DG.objects.all().prefetch_related("dg_sigle")
    qs_np=NP.objects.all()
    qs_minattend=MinAttend.objects.all()
    qs_verb=Verbatim.objects.all()
    qs_status=Status.objects.all()

    #fields names
    names_actids=[field.name for field in ActIds()._meta.fields if field.name not in excl_fields_act_ids]
    names_act=[field.name for field in Act()._meta.fields if field.name not in excl_fields_act]
    names_act_m2m=[field.name for field in Act()._meta.many_to_many]
    
    #list of acts
    acts=[]
    nb=0

    for act in qs_act:
        #~ print "act", act
        nb+=1
        print "nb", nb
        #~ print ""
        #list of fields for one act
        fields=[]
        act_ids=qs_actids.get(act=act)

        #ActIds
        for field in names_actids:
            fields.append(getattr(act_ids, field))
        
        #Act
        for field in names_act:
            #CodeSect and related
            if "code_sect_" in field:
                cs_id=getattr(act, field+"_id")
                if cs_id!=None:
                    cs=qs_cs.get(pk=cs_id)
                    fields.append(cs.code_sect)
                    fields.append(cs.code_agenda.code_agenda)
                else:
                    fields.extend([None, None])
            #Rapporteurs (Person) and related (oeil) or Responsibles (Person) and related (prelex)
            elif "rapp_" in field or "resp_" in field:
                pers_id=getattr(act, field+"_id")
                if pers_id!=None:
                    pers=qs_pers.get(pk=pers_id)
                    party=qs_party.get(pk=pers.party_id)
                    fields.append(pers.name)
                    fields.append(pers.country_id)
                    fields.append(party.party)
                    if "resp_" in field:
                        #party_family
                        fields.append(qs_pf.get(party=party, country_id=pers.country_id).party_family)
                else:
                    if "resp_" in field:
                        temp=[None]*4
                    else:
                        temp=[None]*3
                    fields.extend(temp)
            #DG and related
            elif "dg_" in field:
                dg_id=getattr(act, field+"_id")
                if dg_id!=None:
                    dg=qs_dg.get(pk=dg_id)
                    fields.append(dg.dg)
                    fields.append(dg.dg_sigle.dg_sigle)
                else:
                    fields.extend([None, None])
            else:
                #for all the other non fk fields, get its value
                fields.append(getattr(act, field))
#~ 
        #Act many to many fields
        for field in names_act_m2m:
            #GvtCompo
            if "gvt_compo"==field:
                gvt_compos_country=gvt_compos_party=gvt_compos_party_family=""
                #~ #for each country
                for gvt_compo in act.gvt_compo.all():
                    #for each party, add a "row" for each variable (country, party, party family)
                    for party in gvt_compo.party.all():
                        gvt_compos_country+=gvt_compo.country_id+"; "
                        gvt_compos_party+=party.party+"; "
                        gvt_compos_party_family+=qs_pf.get(party=party, country_id=gvt_compo.country_id).party_family+"; "
                #delete last "; "
                fields.append(gvt_compos_country[:-2])
                fields.append(gvt_compos_party[:-2])
                fields.append(gvt_compos_party_family[:-2])
            #~ #adopt_cs_contre, adopt_cs_abs, adopt_pc_contre, adopt_pc_abs
            else:
                countries=""
                for country in getattr(act, field).all():
                    countries+=country.country_code+"; "
                fields.append(countries[:-2])
#~ 
        #Opal
        np_instances=qs_np.filter(act=act)
        np_vars={"case_nb":"", "np":"", "act_type":"", "act_date":""}
        for np_instance in np_instances:
            for np_var in np_vars:
                if np_var=="np":
                    inst=np_instance.np_id
                else:
                    inst=getattr(np_instance, np_var)
                np_vars[np_var]+=str(inst)+"; "
        for np_var in np_vars:
            fields.append(np_vars[np_var][:-2])
#~ 
        #Ministers' attendance fields
        instances=qs_minattend.filter(act=act)
        temp_fields={"country": "", "verbatim": "", "status": ""}
        for instance in instances:
            temp_fields["country"]+=instance.country_id+"; "
            temp_fields["verbatim"]+=qs_verb.get(pk=instance.verbatim_id).verbatim+"; "
            temp_fields["status"]+=qs_status.get(verbatim_id=instance.verbatim_id, country_id=instance.country_id).status+"; "

        fields.append(temp_fields["country"][:-2])
        fields.append(temp_fields["verbatim"][:-2])
        fields.append(temp_fields["status"][:-2])
        
        acts.append(fields)
    
    tac=time.time()
    print "time", tac-tic

    return acts


#VERY SLOW!
#~ def get_validated_acts(excl_fields_act_ids, excl_fields_act):
    #~ """
    #~ FUNCTION
    #~ return all the validated acts of the model
    #~ PARAMETERS
    #~ excl_fields_act_ids: fields not to be exported (ActIds) [list of strings]
    #~ excl_fields_act: fields not to be exported (Act) [list of strings]
    #~ RETURNS
    #~ acts: validated acts and relative data [list of Act model instances]
    #~ """
    #~ qs=Act.objects.filter(validated=2)
    #~ #list of acts
    #~ acts=[]
    #~ nb=0
#~ 
    #~ for act in qs.iterator():
        #~ print "act", act
        #~ nb+=1
        #~ print "nb", nb
        #~ print ""
        #~ #list of fields for one act
        #~ fields=[]
        #~ act_ids=ActIds.objects.get(act=act, src="index")
#~ 
        #~ #ActIds
        #~ for field in ActIds()._meta.fields:
            #~ if field.name not in excl_fields_act_ids:
                #~ fields.append(getattr(act_ids, field.name))
#~ 
        #~ #Act
        #~ for field in Act()._meta.fields:
            #~ if field.name not in excl_fields_act:
                #~ #CodeSect and related
                #~ if "code_sect_" in field.name:
                    #~ temp=getattr(act, field.name)
                    #~ if temp!=None:
                        #~ fields.append(temp.code_sect)
                        #~ fields.append(temp.code_agenda.code_agenda)
                    #~ else:
                        #~ fields.extend([None, None])
                #~ #Rapporteurs (Person) and related (oeil) or Responsibles (Person) and related (prelex)
                #~ elif "rapp_" in field.name or "resp_" in field.name:
                    #~ temp=getattr(act, field.name)
                    #~ if temp!=None:
                        #~ fields.append(temp.name)
                        #~ country=temp.country
                        #~ party=temp.party
                        #~ fields.append(country.country_code)
                        #~ fields.append(party.party)
                        #~ if "resp_" in field.name:
                            #~ #party_family
                            #~ fields.append(PartyFamily.objects.get(party=party, country=country).party_family)
                    #~ else:
                        #~ if "resp_" in field.name:
                            #~ temp=[None]*4
                        #~ else:
                            #~ temp=[None]*3
                        #~ fields.extend(temp)
                #~ #DG and related
                #~ elif "dg_" in field.name:
                    #~ temp=getattr(act, field.name)
                    #~ if temp!=None:
                        #~ fields.append(temp.dg)
                        #~ fields.append(temp.dg_sigle.dg_sigle)
                    #~ else:
                        #~ fields.extend([None, None])
                #~ else:
                    #~ #for all the other non fk fields, get its value
                    #~ fields.append(getattr(act, field.name))
#~ 
        #~ #Act many to many fields
        #~ for field in Act()._meta.many_to_many:
            #~ #GvtCompo
            #~ if "gvt_compo"==field.name:
                #~ gvt_compos_country=gvt_compos_party=gvt_compos_party_family=""
                #~ #for each country
                #~ for gvt_compo in getattr(act, field.name).all():
                    #~ country=gvt_compo.country
                    #~ #for each party, add a "row" for each variable (country, party, party family)
                    #~ for party in gvt_compo.party.all():
                        #~ gvt_compos_country+=country.country_code+"; "
                        #~ gvt_compos_party+=party.party+"; "
                        #~ gvt_compos_party_family+=PartyFamily.objects.get(country=country, party=party).party_family+"; "
                #~ #delete last "; "
                #~ fields.append(gvt_compos_country[:-2])
                #~ fields.append(gvt_compos_party[:-2])
                #~ fields.append(gvt_compos_party_family[:-2])
            #~ #adopt_cs_contre, adopt_cs_abs, adopt_pc_contre, adopt_pc_abs
            #~ else:
                #~ countries=""
                #~ for country in getattr(act, field.name).all():
                    #~ countries+=country.country_code+"; "
                #~ fields.append(countries[:-2])
#~ 
        #~ #Opal
        #~ np_instances=NP.objects.filter(act=act)
        #~ np_vars={"case_nb":"", "np":"", "act_type":"", "act_date":""}
        #~ for np_instance in np_instances:
            #~ for np_var in np_vars:
                #~ if np_var=="np":
                    #~ inst=getattr(np_instance, np_var)
                    #~ inst=inst.country_code
                #~ else:
                    #~ inst=getattr(np_instance, np_var)
                #~ np_vars[np_var]+=str(inst)+"; "
        #~ for np_var in np_vars:
            #~ fields.append(np_vars[np_var][:-2])
#~ 
        #~ #Ministers' attendance fields
        #~ instances=MinAttend.objects.filter(act=act)
        #~ temp_fields={"country": "", "verbatim": "", "status": ""}
        #~ for instance in instances:
            #~ temp_fields["country"]+=instance.country.country_code+"; "
            #~ temp_fields["verbatim"]+=instance.verbatim.verbatim+"; "
            #~ temp_fields["status"]+=Status.objects.get(verbatim=instance.verbatim, country=instance.country).status+"; "
#~ 
        #~ fields.append(temp_fields["country"][:-2])
        #~ fields.append(temp_fields["verbatim"][:-2])
        #~ fields.append(temp_fields["status"][:-2])
        #~ 
        #~ acts.append(fields)
#~ 
    #~ return acts



def qs_to_csv_file(headers, acts, outfile_path):
    """
    FUNCTION
    saves a query set in a csv file on the server
    PARAMETERS
    headers: list of headers [list of strings]
    acts: list of acts [list of Act model instances]
    outfile_path: path of the file to save [string]
    RETURNS
    none
    """
    writer=csv.writer(open(outfile_path, 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

    #write headers
    writer.writerow(headers)

    #write every acts in the db
    for act in acts:
        writer.writerow(act)


def send_file(request, file_server, file_client):
    """
    FUNCTION
    downloads a file from the server
    PARAMETERS
    request: html request [HttpRequest object]
    file_server: name of the file on the server side [string]
    file_client: name of the file on the client side [string]
    RETURNS
    response: html response [HttpResponse object]
    SRC
    http://stackoverflow.com/questions/1930983/django-download-csv-file-using-a-link
    """
    wrapper     =FileWrapper(open(file_server))
    content_type=mimetypes.guess_type(file_server)[0]
    response    =HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']     =os.path.getsize(file_server)
    response['Content-Disposition']="attachment; filename=%s"%file_client
    return response



@login_required
@user_passes_test(lambda u: is_member(u, ["admin", "import_export"]))
def export(request):
    """
    VIEW
    displays the export page -> export all the acts in the db regarding the sorting variable
    TEMPLATES
    export/index.html
    """
    response={}
    
    if request.method=='POST':
        dir_server=settings.MEDIA_ROOT+"/export/"
        file_name="acts.txt"
        #if a file with the same name already exists, we delete it
        if os.path.exists(dir_server+file_name):
            os.remove(dir_server+file_name)
        #get the headers
        excl_fields_act_ids=["id", 'src', "url_exists", 'act']
        excl_fields_act=["id",  'date_doc', "url_prelex", "validated", "validated_attendance"]
        headers=get_headers(excl_fields_act_ids, excl_fields_act)
        #fetch every acts in the db
        acts=get_validated_acts(excl_fields_act_ids, excl_fields_act)
        #save into csv file
        qs_to_csv_file(headers, acts, dir_server+file_name)
        print "csv export"
        return send_file(request, dir_server+file_name, file_name)

    #GET
    else:
        #fill the hidden input field with the number of acts to export
        response["acts_nb"]=Act.objects.filter(validated=2).count()


    #displays the page (GET) or POST if javascript disabled
    return render_to_response('export/index.html', response, context_instance=RequestContext(request))
