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


def get_save_acts(excl_fields_act_ids, excl_fields_act, writer):
    """
    FUNCTION
    return all the validated acts of the model
    PARAMETERS
    excl_fields_act_ids: fields not to be exported (ActIds) [list of strings]
    excl_fields_act: fields not to be exported (Act) [list of strings]
    RETURNS
    writer: object to write in the csv file [Writer object]
    #~ RETURNS
    #~ None
    #~ """
    tic=time.time()
    
    qs=Act.objects.filter(validated=2)
    nb=0

    for act in qs.iterator():
        #~ print "act", act
        nb+=1
        print "nb", nb
        #~ print ""
        #list of fields for one act
        fields=[]
        act_ids=ActIds.objects.get(act=act, src="index")

        #ActIds
        for field in ActIds()._meta.fields:
            if field.name not in excl_fields_act_ids:
                fields.append(getattr(act_ids, field.name))

        #Act
        for field in Act()._meta.fields:
            if field.name not in excl_fields_act:
                #CodeSect and related
                if "code_sect_" in field.name:
                    temp=getattr(act, field.name)
                    if temp!=None:
                        fields.append(temp.code_sect)
                        fields.append(temp.code_agenda.code_agenda)
                    else:
                        fields.extend([None, None])
                #Rapporteurs (Person) and related (oeil) or Responsibles (Person) and related (prelex)
                elif "rapp_" in field.name or "resp_" in field.name:
                    temp=getattr(act, field.name)
                    if temp!=None:
                        fields.append(temp.name)
                        country=temp.country
                        party=temp.party
                        fields.append(country.country_code)
                        fields.append(party.party)
                        if "resp_" in field.name:
                            #party_family
                            fields.append(PartyFamily.objects.get(party=party, country=country).party_family)
                    else:
                        if "resp_" in field.name:
                            temp=[None]*4
                        else:
                            temp=[None]*3
                        fields.extend(temp)
                #DG and related
                elif "dg_" in field.name:
                    temp=getattr(act, field.name)
                    if temp!=None:
                        fields.append(temp.dg)
                        fields.append(temp.dg_sigle.dg_sigle)
                    else:
                        fields.extend([None, None])
                else:
                    #for all the other non fk fields, get its value
                    fields.append(getattr(act, field.name))

        #Act many to many fields
        for field in Act()._meta.many_to_many:
            #GvtCompo
            if "gvt_compo"==field.name:
                gvt_compos_country=gvt_compos_party=gvt_compos_party_family=""
                #for each country
                for gvt_compo in getattr(act, field.name).all():
                    country=gvt_compo.country
                    #for each party, add a "row" for each variable (country, party, party family)
                    for party in gvt_compo.party.all():
                        gvt_compos_country+=country.country_code+"; "
                        gvt_compos_party+=party.party+"; "
                        gvt_compos_party_family+=PartyFamily.objects.get(country=country, party=party).party_family+"; "
                #delete last "; "
                fields.append(gvt_compos_country[:-2])
                fields.append(gvt_compos_party[:-2])
                fields.append(gvt_compos_party_family[:-2])
            #adopt_cs_contre, adopt_cs_abs, adopt_pc_contre, adopt_pc_abs
            else:
                countries=""
                for country in getattr(act, field.name).all():
                    countries+=country.country_code+"; "
                fields.append(countries[:-2])

        #Opal
        np_instances=NP.objects.filter(act=act)
        np_vars={"case_nb":"", "np":"", "act_type":"", "act_date":""}
        for np_instance in np_instances:
            for np_var in np_vars:
                if np_var=="np":
                    inst=getattr(np_instance, np_var)
                    inst=inst.country_code
                else:
                    inst=getattr(np_instance, np_var)
                np_vars[np_var]+=str(inst)+"; "
        for np_var in np_vars:
            fields.append(np_vars[np_var][:-2])

        #Ministers' attendance fields
        instances=MinAttend.objects.filter(act=act)
        temp_fields={"country": "", "verbatim": "", "status": ""}
        for instance in instances:
            temp_fields["country"]+=instance.country.country_code+"; "
            temp_fields["verbatim"]+=instance.verbatim.verbatim+"; "
            temp_fields["status"]+=Status.objects.get(verbatim=instance.verbatim, country=instance.country).status+"; "

        fields.append(temp_fields["country"][:-2])
        fields.append(temp_fields["verbatim"][:-2])
        fields.append(temp_fields["status"][:-2])
        
        #write act in file
        writer.writerow(fields)
    
    tac=time.time()
    print "time", tac-tic

    #~ return acts



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
        #file to write in
        writer=csv.writer(open(dir_server+file_name, 'w'),  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        #write headers
        writer.writerow(headers)
        #fetch all the acts of the db and save them into the csv file
        get_save_acts(excl_fields_act_ids, excl_fields_act, writer)

        print "csv export"
        return send_file(request, dir_server+file_name, file_name)

    #GET
    else:
        #fill the hidden input field with the number of acts to export
        response["acts_nb"]=Act.objects.filter(validated=2).count()


    #displays the page (GET) or POST if javascript disabled
    return render_to_response('export/index.html', response, context_instance=RequestContext(request))
