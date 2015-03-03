#-*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
from act_ids.forms import ActIdsForm
from act.forms import ActForm, Add, Modif
from act.models import Act, DG, Person, NP, PartyFamily, Country, CodeSect
from history.models import History
from import_app.models import ImportNP
from common.db import get_act_ids
#get the add_modif check_add_modif_forms
from common.views import check_add_modif_forms, get_ajax_errors
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
from common.config_file import max_cons
#retrieve url contents
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from import_app.get_ids_oeil import get_url_oeil, get_url_content_oeil
#retrieve data
from get_data_eurlex import get_data_eurlex, get_date_diff, save_config_cons
from get_data_oeil import get_data_oeil
from get_data_others import get_data_others
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required
#use json for the ajax request
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
#log file
from django.conf import settings
import sys
import os
import time
import logging
#convert unicode to dict
from ast import literal_eval
from collections import OrderedDict
 
# Get an instance of a logger
logger = logging.getLogger(__name__)



def get_urls(act_ids, dos_id):
    """
    FUNCTION
    get the eurlex and oeil url
    PARAMETERS
    act_ids: ids of the act [ActIds model instance]
    dos_id: validated dos_id of the act or None if does not exist
    RETURN
    urls: urls of eurlex and oeil [dictionary of strings]
    """
    urls={}
    #["data" variables url to retrieve all the variables, "ids" variables url to retrieve the directory code variables (code_sect and rep_en variables)]
    urls["url_eurlex"]=[get_url_eurlex(act_ids.no_celex), get_url_eurlex(act_ids.no_celex, "HIS")]
    urls["url_oeil"]=get_url_oeil(str(act_ids.no_unique_type), str(act_ids.no_unique_annee), str(act_ids.no_unique_chrono))
    return urls


def get_party_family(resps):
    """
    FUNCTION
    get the party family variable for each resp
    PARAMETERS
    resps: dictionary of responsibles [dictionary of Person model instances]
    RETURN
    resps: dictionary of party_family variables for each responsible [dictionary of strings]
    """
    for index in resps:
        if resps[index]!=None:
            #if id and not instance, get the instance instead
            if type(resps[index]) is long:
                resps[index]=Person.objects.get(pk=resps[index])
            # if party None: the responsible does not exist in external responsible file -> we can only display his name (on eurlex and œil, no data about country or party of responsibles)
            if resps[index].party!=None:
                resps[index]=PartyFamily.objects.get(party=resps[index].party, country=resps[index].country).party_family
            else:
                resps[index]=None
        else:
            resps[index]=None
    return resps


def get_data(src, act_ids, url):
    """
    FUNCTION
    get data of an act from a source in parameter
    PARAMETERS
    src: source (eurlex or oeil) [string]
    act_ids: ids of the act for a given source source [ActIds model instance]
    url: link to the act page [string]
    RETURN
    fields:  dictionary which contains retrieved data for a given source [dictionary]
    dg_names: list of dg names [list of strings]
    resp_names: list of resp names [list of strings]
    """
    logger.debug('get_data')
    fields={}
    dg_names=[None]*2
    resp_names=[None]*3
    ok=False
    
    logger.debug("get_url_content_"+src)

    if src=="eurlex":
        url_content=[get_url_content_eurlex(url[0]), get_url_content_eurlex(url[1])]
        if url_content[0] is not False:
            ok=True
    elif src=="oeil":
        #oeil
        url_content=get_url_content_oeil(url)
        if url_content is not False:
            ok=True
        
    #if the url exists and there is a valid content
    if ok:
         setattr(act_ids, "url_exists", True)
         fields, dg_names, resp_names=eval("get_data_"+src)(url_content, act_ids)
    else:
        setattr(act_ids, "url_exists", False)
        logger.debug("error while retrieving "+src+" url")
        print "error while retrieving "+src+" url"


    #actualization url exist attribute
    logger.debug("act_ids to be saved")
    act_ids.save()

    return fields, dg_names, resp_names


def check_multiple_dgs(act):
    """
    FUNCTION
    check if act.dg_1 or act.dg_2 contains one or more dgs (if it's a DG with a number, there can be 2 or 3 possible DGs)
    assignate the first one to the corresponding act field and store all the possibilities in a dictionary (to be displayed in the template)
    PARAMETERS
    act: instance of the data of the act [Act model instance]
    RETURN
    dgs:  dictionary that contains all the possible dgs for each dg [dictionary of (lists of) DG model instances]
    act: updated instance of the data of the act [Act model instance]
    """
    dgs={}
    for index in range(1,3):
        num=str(index)
        name="dg_"+num+"_id"
        instances=getattr(act, name)
        try:
            nb=len(instances)
            if nb>1:
                #store all the possible values to be displayed in the template
                #only dgs with a number can have many values (dg number with only one value: 1999-3-1)
                dgs_temp=[dg.dg for dg in instances]
                dgs[num]=", ".join(dgs_temp)+"."
            #if many possible dgs, keep the first one only (to be displayed in the drop down list)
            setattr(act, name, instances[0])
        except Exception, e:
            print "dg is None", e
            pass
    return dgs, act


def store_dg_resp(act, eurlex_list, oeil_list, field):
    """
    FUNCTION
    get all the dgs and resps on eurlex / œil and save œil dgs / resps in Act model if none was found on eurlex
    PARAMETERS
    act: instance of the data of the act [Act model instance]
    eurlex_list: list of dg or resp names from eurlex [list of strings]
    oeil_list: list of dg or resp names from oeil [list of strings]
    field: name of the field ("dg" or "resp") [string]
    RETURN
    act: instance of the data of the act (with updated dgs or resps if any) [Act model instance]
    eurlex_dic: list of dg or resp names from eurlex [dictionary of strings]
    oeil_dic: list of dg or resp names from oeil [dictionary of strings]
    """
    print "oeil_list", oeil_list
    oeil_dic={}
    for index, field in enumerate(oeil_list):
        index=str(index+1)
        oeil_dic[index]=field
    eurlex_dic={}
    for index, field in enumerate(eurlex_list):
        num=str(index+1)
        eurlex_dic[num]=field
        if field==None and oeil_dic[num]!=None:
            try:
                #update the act instance with the oeil resp
                if field=="resp":
                    setattr(act, "resp_"+num, Person.objects.get(name=oeil_dic[num]))
                else:
                    #update the act instance with the oeil dg
                    setattr(act, "dg_"+num, DG.objects.get(dg=oeil_dic[num]))
            except Exception, e:
                print "except store_dg_resp", e

    return act, eurlex_dic, oeil_dic


def get_adopt_variables(act):
    """
    FUNCTION
    get data for adopt variables (adopt_cs_contre, adopt_pc_contre, adopt_cs_abs, adopt_pc_abs) from the database
    PARAMETERS
    act: instance of the data of the act [Act model instance]
    RETURN
    adopts: adopt variables [dictionary]
    """
    adopts={}
    names=["adopt_cs_contre", "adopt_pc_contre", "adopt_cs_abs", "adopt_pc_abs"]
    #for each variable:
    for name in names:
        countries=getattr(act, name).all()
        #for each of the country drop down lists
        for index in range(len(countries)):
            adopts[name+"_"+str(index+1)]=countries[index]
        
    print "adopts"
    print adopts
    print ""

    return adopts


def check_update(POST):
    """
    FUNCTION
    check if we are updating a field of the act form (code_sect, rapp or resp)
    PARAMETERS
    POST: request.POST object [dictionary]
    RETURN
    True if a field is being updated and False otherwise [Boolean]
    """
    for key in POST:
        if key.startswith('update'):
            return True
    return False


def get_data_all(context, add_modif, act, POST):
    """
    FUNCTION
    get all data of an act (from eurlex and oeil)
    PARAMETERS
    context: variables to be displayed in the html form [dictionary]
    add_modif: "add" if the form is in add mode, "modif" otherwise [string]
    act: instance of the data of the act [Act model instance]
    POST: request.POST object [dictionary]
    RETURN
    context: update of the variables to be displayed in the html form [dictionary]
    """
    logger.debug('get_data_all')
    #retrieve the act ids for each source
    act_ids=get_act_ids(act)

    #"compute" the url of the eurlex and oeil page
    urls=get_urls(act_ids["index"], act_ids["index"].dos_id)
    
    #an act has been selected in the drop down list -> the related data is displayed
    #if state different of modif, save and ongoing and if the act is not being modified
    #not check_update(POST): not updating a code_sect, rapp or resp
    if context["state"]=="display" and add_modif=="add" and not check_update(POST):
        print "data retrieval"
        logger.debug('data retrieval')
        
        #retrieve all the data from all the sources
        #COMMENT FOR TESTS ONLY
        
        logger.debug('oeil to be processed')
        print "oeil to be processed"
        fields, dg_names_oeil, resp_names_oeil=get_data("oeil", act_ids["oeil"], urls["url_oeil"])
        act.__dict__.update(fields)

        #adopt_conseil from eurlex needs nb_lectures from oeil -> eurlex after oeil
        logger.debug('eurlex to be processed')
        print "eurlex to be processed"
        fields, dg_names_eurlex, resp_names_eurlex=get_data("eurlex", act_ids["eurlex"], urls["url_eurlex"])
        act.__dict__.update(fields)
        
        #~ #store dg/resp from eurlex and oeil to be displayed as text in the template
        logger.debug('dg and resp to be processed')
        act, context["dg_names_eurlex"], context["dg_names_oeil"]=store_dg_resp(act, dg_names_eurlex, dg_names_oeil, "dg")
        act, context["resp_names_eurlex"], context["resp_names_oeil"]=store_dg_resp(act, resp_names_eurlex, resp_names_oeil, "resp")
#~
        #~ #check multiple values for dgs with numbers
        context["dg"], act=check_multiple_dgs(act)
    else:
        #on ADD
        #get information about dg and resp when updating a field
        #literal_eval to convert unicode dic to dic
        names={"dg_names_eurlex": "hidden_dg_eurlex_dic", "dg_names_oeil": "hidden_dg_oeil_dic", "resp_names_eurlex": "hidden_resp_eurlex_dic", "resp_names_oeil": "hidden_resp_oeil_dic", "dg": "hidden_dg_dic"}
        for name in names:
            try:
                context[name]=literal_eval(POST[names[name]])
            except Exception, e:
                print "pb literal_eval", names[name], e
                context[name]={}

    #we have selected an act in the drop down list or clicked on the modification button
    if "add_act" in POST or "modif_act" in POST:
        #display adopt variables (countries in the drop down lists)
        adopts=get_adopt_variables(act)

        if "add_act" in POST:
            adopts["releve_mois_init"]=act.releve_mois
            form_data=ActForm(instance=act, initial=adopts)
            #~ context["status"]="add"
        else:
            form_data=ActForm(instance=act, initial=adopts)
            #~ context["status"]="modif"
    else:
        form_data=ActForm(POST, instance=act)

    context["urls"]=urls
    context['act']=act
    #COMMENT FOR TESTS ONLY
    temp=get_data_others(act_ids["index"], act)
    context['opals']=temp["opal"]
    context['gvt_compos']=temp["gvt_compo"]
    context['min_attends']=temp["min_attend"]
    context["party_family"]=get_party_family({"1": act.resp_1_id, "2": act.resp_2_id, "3": act.resp_3_id})
    context["cons_vars_b"]=get_cons_vars("b", act.date_cons_b, act.cons_b)
    context["cons_vars_a"]=get_cons_vars("a", act.date_cons_a, act.cons_a)
    context['act_ids']=act_ids
    context['form_data']=form_data
    
    return context



def get_cons_vars(character, date_cons="", cons=""):
    """
    FUNCTION
    from the character (a or b), date_cons and cons fields in parameter, return a dictionary of all the temp_date_cons and temp_cons values
    PARAMETERS
    character: "a" or "b" [string]
    date_cons: value of the date_cons field [string]
    cons: value of the cons field [string]
    RETURN
    cons_vars: dictionary of all the temp_date_cons and temp_cons values [dictionary]
    """
    cons_vars=OrderedDict({})
    date_conss=date_cons.split(";")
    conss=cons.split(";")
    date_cons_name="date_cons_"
    cons_name="cons_"

    #initialization
    for num in xrange(1, max_cons+1):
        suffix=character+"_"+str(num)
        #initialize date_cons and cons
        cons_vars[date_cons_name+suffix]=None
        cons_vars[cons_name+suffix]=None

    #there is at least one cons variable
    if date_cons!="":
        for num in xrange(1, max_cons+1):
            suffix=character+"_"+str(num)
            try:
                #fill dictionary with vartiable values
                cons_vars[date_cons_name+suffix]=date_conss[num]
                cons_vars[cons_name+suffix]=conss[num]
            except Exception, e:
                #no more cons variable
                break
            

    print "cons_vars", cons_vars

    return cons_vars


def init_context(context):
    """
    FUNCTION
    initialize the context dictionary passed to the template with list of variables and names to display
    PARAMETERS
    context: context dictionary (empty or with a few variables) [dictionary]
    RETURN
    context: first variables of the dictionary containing all the variables to be displayed in th html form [dictionary]
    """
    #display "real" name of variables (names given by europolix team, not the names stored in db)
    context['display_name']=var_name_ids.var_name
    context['display_name'].update(var_name_data.var_name)
    
    #the template contains 4 main tables, each of these tables contains a subset of variables from the Act model -> this allows the template to loop over the corresponding subset of variables only (the one corresponding to the table to be displayed)
    #three tables for eurlex, one for oeil
    context["vars_eurlex_1"]=["titre_en", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "rep_en_1", "rep_en_2", "rep_en_3", "rep_en_4", "type_acte", "base_j", "nb_mots"]    
    context["vars_eurlex_2"]=["adopt_propos_origine", "com_proc", "dg_1", "dg_2", "dg_3", "resp_1", "resp_2", "resp_3", "transm_council", "nb_point_b", "adopt_conseil", "nb_point_a"]
    context["vars_eurlex_3"]=["rejet_conseil", "chgt_base_j", "duree_adopt_trans", "duree_proc_depuis_prop_com", "duree_proc_depuis_trans_cons", "duree_tot_depuis_prop_com", "duree_tot_depuis_trans_cons", "vote_public", "adopt_cs_regle_vote", "adopt_cs_contre", "adopt_cs_abs", "adopt_pc_contre", "adopt_pc_abs", "adopt_ap_contre", "adopt_ap_abs", "dde_em", "split_propos", "proc_ecrite", "suite_2e_lecture_pe", "gvt_compo"]
    
    context["vars_oeil"]=["commission", "com_amdt_tabled", "com_amdt_adopt", "amdt_tabled", "amdt_adopt", "votes_for_1", "votes_agst_1", "votes_abs_1", "votes_for_2", "votes_agst_2", "votes_abs_2", "rapp_1", "rapp_2", "rapp_3", "rapp_4", "rapp_5", "modif_propos", "nb_lectures", "sign_pecs"]
    
    return context



class ActUpdate(UpdateView):
    """
    VIEW
    displays and processes the acts data retrieval page
    TEMPLATES:
    act/index.html: display the act data page which itself calls the template of the act form
    act/form.html: display the act form
    """
    #if omitted error 'ActUpdate' object has no attribute 'object'
    object=None
    model = Act
    form_class=ActForm
    #html page of the form page
    template_name = 'act/index.html'
    #html page of the form object
    form_template = 'act/form.html'
    
    #used for log only
    def dispatch(self, request, *args, **kwargs):
        logger.debug('\n')
        logger.debug('dispatch (log)')
        #~ self.course = get_object_or_404(Class, pk=kwargs['class_id'])
        #save all prints to a log file
        log_file_path=settings.LOG_FILE_PATH
        #COMMENT OUT FOR LOCAL TESTS ONLY
        #~ sys.stdout = open(log_file_path, "a")
        print ""
        print time.strftime("TODAY IS: %d/%m/%Y, CURRENT TIME IS: %H:%M:%S")
        print ""
        
        return super(ActUpdate, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        Pass parameters to the context object for get requests
        """
        logger.debug('get (log)')
        print "get"
        #~ print "static path"
        #~ print settings.STATIC_ROOT
        #if ommited, get error "Generic detail view ActUpdate must be called with either an object pk or a slug."
        return self.render_to_response(self.get_context_data())
    
    
    def get_context_data(self, **kwargs):
        """
        pass generic parameters to the context object so it can be viewed inside the template
        """
        logger.debug('get_context_data (log)')
        print "get_context_data"
        context = super(ActUpdate, self).get_context_data(**kwargs)
        
        #fill the dictionary sent to the template with the list of variables along with the names to display
        context.update(init_context(context))
        if "add" not in context:
            context['add'] = Add()
        if "modif" not in context:
            context['modif'] = Modif()
        if "form_data" not in context:
            context["form_data"]=ActForm()
        context["form_template"]=self.form_template
         #state=display (display the data of an act), saved (the act is being saved) or ongoing (validation errors while saving)
        if "state" not in context:
            context['state']="display"

        context["cons_vars_b"]=get_cons_vars("b")
        context["cons_vars_a"]=get_cons_vars("a")
        
        print "end get_context_data"

        #prints are normally displayed (back to normal)
        #COMMENT OUT FOR LOCAL TESTS ONLY
        #~ sys.stdout = sys.__stdout__
        
        return context



    def post(self, request, *args, **kwargs):
        """
        The form is posted
        """
        logger.debug('post (log)')
        print "post"
        context={}
        #add_modif=None, "add" or "modif"
        #act=act to validate / modify or None if no act is found (modification)
        #context: add add or modif to the forms being displayed / to be displayed
        mode, add_modif, act, context=check_add_modif_forms(request, context, Add, Modif, "act")
        
        print "ACT", act
        print "ACTION",  add_modif
        print "USER", request.user.username
        print ""
        
        logger.debug("act: "+ str(act))
        logger.debug('mode: ' + str(mode))
        logger.debug("add_modif: "+ str(add_modif))
        logger.debug("user: "+ request.user.username)

        #if any of this key is present in the context dictionary -> no act display and return the errors with a json object
        #otherwise display act and return the html form of the act to validate or modif in a string format
        keys=["msg", "add_act_errors", "modif_act_errors"]
    
        #if selection of an act in the drop down list or click on the modif_act button
        if mode !=None:
            #if we are about to add or modif an act (the add or modif form is valid)
            if add_modif!=None:
                post_values = request.POST.copy()
                
                #update durations (JavaScript is deactivated)
                if 'update_durations' in post_values:
                    print "update_durations"
                    post_values.update(update_durations_fct(post_values))

                form_data=ActForm(post_values, instance=act)

                #saves the act
                if 'save_act' in post_values:
                    if form_data.is_valid():
                        context=self.form_valid(form_data, act, context, add_modif)
                    else:
                        context=self.form_invalid(form_data, context)
                
                
                #default state: display the act
                if "state" not in context:
                    context["state"]="display"
                        
                #displays the retrieved data of the act to validate / modify when...
                    #no form error: selection of an act in the add / modif form
                    #form errors: when saving the form if ajax deactivated
                if not any(key in context for key in keys) or not self.request.is_ajax() and context["state"]!="saved":
                    logger.debug("act_to_validate display")
                    print 'act_to_validate display'
                    
                    #get the data of the act
                    context=get_data_all(context, add_modif, act, post_values)


                context['mode']=mode
                context['add_modif']=add_modif
            
            if request.is_ajax():
                #save act (with or without errors) or act display and modif (with errors)
                if any(key in context for key in keys):
                    logger.debug("save act (with or without errors) or act display and modif (with errors)")
                    return HttpResponse(simplejson.dumps(context), mimetype="application/json")
                else:
                    #act display or modif (without errors)
                    logger.debug("act display or modif (without errors)")
                    context=self.get_context_data(**context)
                    return HttpResponse(render_to_string(self.form_template, context, RequestContext(request)))

        if request.is_ajax():
            #no act has been selected-> do nothing
            return HttpResponse(simplejson.dumps(""), mimetype="application/json")

        return self.render_to_response(self.get_context_data(**context))


    def form_valid(self, form_data, act, context, add_modif):
        """
        Called if all forms are valid.
        """
        print "form_valid"
    
        #if use form_data m2m are deleted!
        act.validated=2
        act.notes=self.request.POST['notes']
        act.save()
        
        #save adopt variables
        names=["adopt_cs_contre", "adopt_pc_contre", "adopt_cs_abs", "adopt_pc_abs"]
        for name in names:
            #remove "old" countries of adopt variables for the given act
            field=getattr(act, name)
            field.clear()
            for nb in range(8):
                form_field=form_data.cleaned_data[name+"_"+str(nb+1)]
                if form_field!=None:
                    #save "new" countries of adopt variables
                    field.add(form_field)
                
        context["state"]="saved"
        context["msg"]="The act " + str(act) + " has been validated!"
        context["msg_class"]="success_msg"
        
        #save in history
        History.objects.create(action=add_modif, form="data", act=act, user=self.request.user)

        return context


    def form_invalid(self, form_data, context):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        print "form_data not valid", form_data.errors
        if self.request.is_ajax():
            context['save_act_errors']= get_ajax_errors(form_data)
        else:
            context['form_data']=form_data
        context["msg"]="The form contains errors! Please correct them before submitting again."
        context["msg_class"]="error_msg"
        state="ongoing"

        return context


def reset_form(request):
    """
    VIEW
    reset the act form (except add and modif)
    TEMPLATES
    act/form.html
    """
    context={}
    context=init_context(context)
    context['form_data']=ActForm()
    return render_to_response('act/form.html', context, context_instance=RequestContext(request))


def update_code_sect(request):
    """
    VIEW
    update the code_agenda when a different code_sect is selected from the drop down list
    TEMPLATES
    None (Ajax only)
    """
    context={}
    if request.POST["code_sect_id"]!="":
        instance=CodeSect.objects.get(pk=request.POST["code_sect_id"])
        context["code_agenda"]=instance.code_agenda.code_agenda
    else:
        context["code_agenda"]=None
    return HttpResponse(simplejson.dumps(context), mimetype="application/json")


def update_person(request):
    """
    VIEW
    update the resp (eurlex) or rapp (oeil) variables when a different person is selected from the drop down list
    TEMPLATES
    None (Ajax only)
    """
    context={}
    if request.POST["person_id"]!="":
        instance=Person.objects.get(pk=request.POST["person_id"])
        context["country"]=instance.country.pk
        party=instance.party
        context["party"]=party.party
        try:
            context["party_family"]=PartyFamily.objects.only("party_family").get(party=party, country=context["country"]).party_family
        except Exception, e:
            print "no party family for the party of the rapporteur yet", e
            context["party_family"]=None
    else:
        context["country"]=None
        context["party"]=None
        context["party_family"]=None

    return HttpResponse(simplejson.dumps(context), mimetype="application/json")


def update_dg(request):
    """
    VIEW
    update the dg_sigle when a different dg is selected from the drop down list
    TEMPLATES
    None (Ajax only)
    """
    context={}
    if request.POST["dg_id"]!="":
        print "dg_id", request.POST["dg_id"]
        instance=DG.objects.get(pk=request.POST["dg_id"])
        context["dg_sigle"]=instance.dg_sigle.dg_sigle
        print "dg_sigle", context["dg_sigle"]
    else:
        context["dg_sigle"]=None
    return HttpResponse(simplejson.dumps(context), mimetype="application/json")


def update_durations_fct(post):
    """
    FUNCTION
    update all the durations fields with the dates passed in the post parameter (request.POST)
    PARAMETERS
    post: request.POST object [dictionary]
    RETURN
    context: updated act data [dictionary]
    """
    context={}
    context['duree_adopt_trans']=context['duree_proc_depuis_prop_com']=context['duree_proc_depuis_trans_cons']=context['duree_tot_depuis_prop_com']=context['duree_tot_depuis_trans_cons']=[None]*5
    transm_council=post["transm_council"]
    adopt_propos_origine=post["adopt_propos_origine"]
    adopt_conseil=post["adopt_conseil"]
    sign_pecs=post["sign_pecs"]


    #duree_adopt_trans
    context['duree_adopt_trans']=get_date_diff(transm_council, adopt_propos_origine)
    print "duree_adopt_trans:", context['duree_adopt_trans']

    #duree_proc_depuis_prop_com
    context['duree_proc_depuis_prop_com']=get_date_diff(adopt_conseil, adopt_propos_origine)
    print "duree_proc_depuis_prop_com:", context['duree_proc_depuis_prop_com']

    #duree_proc_depuis_trans_cons
    context['duree_proc_depuis_trans_cons']=get_date_diff(adopt_conseil, transm_council)
    print "duree_proc_depuis_trans_cons:", context['duree_proc_depuis_trans_cons']

    #duree_tot_depuis_prop_com
    context['duree_tot_depuis_prop_com']=get_date_diff(sign_pecs, adopt_propos_origine)
    #if no sign_pecs
    if context['duree_tot_depuis_prop_com']==None:
        context['duree_tot_depuis_prop_com']=context['duree_proc_depuis_prop_com']
    print "duree_tot_depuis_prop_com:", context['duree_tot_depuis_prop_com']

    #duree_tot_depuis_trans_cons
    context['duree_tot_depuis_trans_cons']=get_date_diff(sign_pecs, transm_council)
    #if no sign_pecs
    if context['duree_tot_depuis_trans_cons']==None:
        context['duree_tot_depuis_trans_cons']=context['duree_proc_depuis_trans_cons']
    print "duree_tot_depuis_trans_cons:", context['duree_tot_depuis_trans_cons']

    print "update_durations_fct"

    return context
    

def update_durations(request):
    """
    VIEW
    update the duration fields (duree_adopt_trans, duree_proc_depuis_prop_com, duree_proc_depuis_trans_cons, duree_tot_depuis_prop_com and duree_tot_depuis_trans_cons variables)
    TEMPLATES
    None (Ajax only)
    """
    context=update_durations_fct(request.POST)
    return HttpResponse(simplejson.dumps(context), mimetype="application/json")
