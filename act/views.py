#-*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
from act_ids.forms import ActIdsForm
from act.forms import ActForm, Add, Modif
from act.models import Act, DG, Person, NP, PartyFamily, Country, CodeSect
from history.models import History
from import_app.models import ImportNP
from common.db import get_act_ids
#get the add_modif fct
from act_ids.views import add_modif_fct
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
#retrieve url contents
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from import_app.get_ids_oeil import get_url_oeil, get_url_content_oeil
from import_app.get_ids_prelex import get_url_prelex, get_url_content_prelex
#retrieve data
from get_data_eurlex import get_data_eurlex
from get_data_oeil import get_data_oeil
from get_data_prelex import get_data_prelex, get_date_diff, save_config_cons
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

# Get an instance of a logger
logger = logging.getLogger(__name__)



def get_urls(act_ids, url_prelex, dos_id):
    """
    FUNCTION
    get the eurlex, oeil and prelex urls
    PARAMETERS
    act_ids: ids of the act [ActIds model instance]
    url_prelex: url of prelex [string]
    dos_id: validated dos_id of the act or None if does not exist
    RETURN
    urls: urls of eurlex, oeil and prelex [dictionary of strings]
    """
    urls={}
    #["data" variables url to retrieve all the variables, "ids" variables url to retrieve the directory code variables (code_sect and rep_en variables)]
    urls["url_eurlex"]=[get_url_eurlex(act_ids.no_celex), get_url_eurlex(act_ids.no_celex, "HIS")]
    urls["url_oeil"]=get_url_oeil(str(act_ids.no_unique_type), str(act_ids.no_unique_annee), str(act_ids.no_unique_chrono))
    #for ids retrieval, if split proposition (ProposChrono has a dash)-> oeil ids to construct url
    #for data retrieval, if split proposition (ProposChrono has a dash)-> dos_id to construct url
    if "-" in act_ids.propos_chrono and dos_id!=None:
        urls["url_prelex"]=get_url_prelex(dos_id)
    else:
        #url saved in the database using the oeil ids in case of a split proposition
        urls["url_prelex"]=url_prelex

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
            # if party None: the responsible does not exist in responsible file (on prelex, we have only names, no party, no country)
            if resps[index].party!=None:
                resps[index]=PartyFamily.objects.get(party=resps[index].party, country=resps[index].country).party_family
            else:
                resps[index]=None
        else:
            resps[index]=None
    return resps


def get_data(src, act_ids, url, act=None):
    """
    FUNCTION
    get data of an act from a source in parameter
    PARAMETERS
    src: source (eurlex, oeil or prelex) [string]
    act_ids: ids of the act for a given source source [ActIds model instance]
    url: link to the act page [string]
    act: data of the act for prelex only [Act model instance]
    RETURN
    fields:  dictionary which contains retrieved data for a given source [dictionary]
    dg_names: list of dg names [list of strings]
    resp_names: list of resp names [list of strings]
    """
    logger.debug('get_data')
    fields={}
    dg_names=[None]*2
    resp_names=[None]*3
    
    logger.debug("get_url_content_"+src)

    if src=="eurlex":
        url_content=[eval("get_url_content_"+src)(url[0]), eval("get_url_content_"+src)(url[1])]
        if url_content[0]!=False:
             setattr(act_ids, "url_exists", True)
             fields=eval("get_data_"+src)(url_content)
        else:
            setattr(act_ids, "url_exists", False)
            logger.debug("error while retrieving "+src+" url")
            print "error while retrieving "+src+" url"

    else:
        #oeil and eurlex
        url_content=eval("get_url_content_"+src)(url)
        #act doesn't exist, problem on page or problem with the Internet connection
        if url_content!=False:
            #set the url_exists attribute of the given source to True
            setattr(act_ids, "url_exists", True)
            #call the corresponding function to retrieve the data and pass it to an object
            fields, dg_names, resp_names=eval("get_data_"+src)(url_content, act_ids, act)
        else:
            setattr(act_ids, "url_exists", False)
            print "error while retrieving "+src+" url"
            logger.debug("error while retrieving "+src+" url")
            #retrieve fields not related to the prelex page
            if src=="prelex":
                #config_cons
                save_config_cons(act.code_sect_1_id)

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


def store_dg_resp(act, oeil_list, prelex_list, field):
    """
    FUNCTION
    store dg or resp names from oeil and prelex in a dictionary and store dgs or resps from oeil in the act object if there is none on prelex
    PARAMETERS
    act: instance of the data of the act [Act model instance]
    oeil_list: list of dg or resp names from oeil [list of strings]
    prelex_list: list of dg or resp names from prelex [list of strings]
s   field: name of the field ("dg" or "resp") [string]
    RETURN
    act: instance of the data of the act (with updated dgs or resps if any) [Act model instance]
    oeil_dic: list of dg or resp names from oeil [dictionary of strings]
    prelex_dic: list of dg or resp names from prelex [dictionary of strings]
    """
    print "oeil_list", oeil_list
    oeil_dic={}
    for index, field in enumerate(oeil_list):
        index=str(index+1)
        oeil_dic[index]=field
    prelex_dic={}
    for index, field in enumerate(prelex_list):
        num=str(index+1)
        prelex_dic[num]=field
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

    return act, oeil_dic, prelex_dic


def get_data_all(context, add_modif, act, POST):
    """
    FUNCTION
    get all data of an act (from eurlex, oeil and prelex)
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

    #"compute" the url of the eurlex, oeil and prelex page
    urls=get_urls(act_ids["index"], act.url_prelex, act_ids["index"].dos_id)
    
    #default state: display the act
    if "state" not in "display":
        context["state"]="display"

    #an act has been selected in the drop down list -> the related data is displayed
    #if state different of modif, save and ongoing and if the act is not being modified
    if context["state"]=="display" and add_modif=="add":
        print "data retrieval"
        logger.debug('data retrieval')
        #retrieve all the data from all the sources
        #COMMENT FOR TESTS ONLY
        logger.debug('eurlex to be processed')
        print "eurlex to be processed"
        act.__dict__.update(get_data("eurlex", act_ids["eurlex"], urls["url_eurlex"], act)[0])
        logger.debug('oeil to be processed')
        print "oeil to be processed"
        fields, dg_names_oeil, resp_names_oeil=get_data("oeil", act_ids["oeil"], urls["url_oeil"], act)
        logger.debug('prelex to be processed')
        print "prelex to be processed"
        act.__dict__.update(fields)
        nb_lectures=act.nb_lectures
        #~ #prelex config_cons needs eurlex, gvt_compo needs oeil
        fields, dg_names_prelex, resp_names_prelex=get_data("prelex", act_ids["prelex"], urls["url_prelex"], act)
        act.__dict__.update(fields)
        #nb_lectures already retrieved from oeil
        act.nb_lectures=nb_lectures
#~
        #~ #store dg/resp from oeil and prelex to be displayed as text in the template
        logger.debug('dg and resp to be processed')
        act, context["dg_names_oeil"], context["dg_names_prelex"]=store_dg_resp(act, dg_names_oeil, dg_names_prelex, "dg")
        act, context["resp_names_oeil"], context["resp_names_prelex"]=store_dg_resp(act, resp_names_oeil, resp_names_prelex, "resp")
#~
        #~ #check multiple values for dgs with numbers
        context["dg"], act=check_multiple_dgs(act)

    if "add_act" in POST or "modif_act" in POST:
        if "add_act" in POST:
            form_data=ActForm(instance=act, initial={"releve_mois_init": act.releve_mois})
            context["status"]="add"
        else:
            form_data=ActForm(instance=act)
            context["status"]="modif"

    else:
        form_data=ActForm(POST, instance=act)

    context["urls"]=urls
    context['act']=act
    #COMMENT FOR TESTS ONLY
    temp=get_data_others(act_ids["index"], act)
    context['opals']=temp["opal"]
    context['min_attends']=temp["min_attend"]
    context["party_family"]=get_party_family({"1": act.resp_1_id, "2": act.resp_2_id, "3": act.resp_3_id})
    context['act_ids']=act_ids
    context['form_data']=form_data

    return context



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
    #one table (used to display one source) displays a subset of variables of the Act model only -> create list to loop over each subset
    #-> one table for eurlex, one for oeil and two for prelex
    context["vars_eurlex"]=["titre_en", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "rep_en_1", "rep_en_2", "rep_en_3", "rep_en_4", "type_acte", "base_j"]
    context["vars_oeil"]=["commission", "com_amdt_tabled", "com_amdt_adopt", "amdt_tabled", "amdt_adopt", "votes_for_1", "votes_agst_1", "votes_abs_1", "votes_for_2", "votes_agst_2", "votes_abs_2", "rapp_1", "rapp_2", "rapp_3", "rapp_4", "rapp_5", "modif_propos", "nb_lectures", "sign_pecs"]
    context["vars_prelex_1"]=["adopt_propos_origine", "com_proc", "dg_1", "dg_2", "resp_1", "resp_2", "resp_3", "transm_council", "cons_b", "nb_point_b", "adopt_conseil", "nb_point_a", "council_a"]
    context["vars_prelex_2"]=["rejet_conseil", "chgt_base_j", "duree_adopt_trans", "duree_proc_depuis_prop_com", "duree_proc_depuis_trans_cons", "duree_tot_depuis_prop_com", "duree_tot_depuis_trans_cons", "vote_public", "adopt_cs_regle_vote", "adopt_cs_contre", "adopt_cs_abs", "adopt_pc_contre", "adopt_pc_abs", "adopt_ap_contre", "adopt_ap_abs", "dde_em", "split_propos", "proc_ecrite", "suite_2e_lecture_pe", "gvt_compo"]
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
        
        #~ print request.GET.get('act_to_validate')
        #~ if request.GET.get('act_to_validate') not in [None, ""]:
            #~ History.objects.create(action="test", form="data", act=Act.objects.get(pk=1), user=User.objects.get(username="romain.lalande"))
        
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
        mode, add_modif, act, context=add_modif_fct(request, context, Add, Modif, "act")
        
        print "ACT", act
        print "ACTION",  add_modif
        print "USER", request.user.username
        print ""
        
        logger.debug("act: "+ str(act))
        logger.debug('mode: ' + mode)
        logger.debug("add_modif: "+ str(add_modif))
        logger.debug("user: "+ request.user.username)

        #if any of this key is present in the context dictionary -> no act display and return the errors with a json object
        #otherwise display act and return the html form of the act to validate or modif in a string format
        keys=["msg", "add_act_errors", "modif_act_errors"]
    
        #if selection of an act in the drop down list or click on the modif_act button
        if mode !=None:
            #if we are about to add or modif an act (the add or modif form is valid)
            if add_modif!=None:
                form_data=ActForm(request.POST, instance=act)

                #saves the act
                if 'save_act' in request.POST:
                    if form_data.is_valid():
                        context=self.form_valid(act, context, add_modif)
                    else:
                        context=self.form_invalid(form_data, context)
                        
                #displays the retrieved data of the act to validate / modify
                #(selection of an act in the add / modif form  with no form error)
                #or errors when saving the form if ajax deactivated
                if not any(key in context for key in keys) or not self.request.is_ajax() and context["state"]!="saved":
                    logger.debug("act_to_validate display")
                    print 'act_to_validate display'
                    #get the data of the act
                    context=get_data_all(context, add_modif, act, self.request.POST)

                context['mode']=mode
            
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


    def form_valid(self, act, context, add_modif):
        """
        Called if all forms are valid.
        """
        print "form_valid"
    
        #if use form_data m2m are deleted!
        act.validated=2
        act.notes=self.request.POST['notes']
        act.save()
        context["state"]="saved"
        context["msg"]="The act " + str(act) + " has been validated!"
        context["msg_class"]="success_msg"
        
        #save in history
        History.objects.create(action=add_modif, form="data", act=act, user=self.request.user)

        #empty forms
        #~ if not self.request.is_ajax():
            #~ context['form_data'] = ActForm()
            #~ context['add'] = Add()
            #~ context['modif'] = Modif()

        return context


    def form_invalid(self, form_data, context):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        print "form_data not valid", form_data.errors
        if self.request.is_ajax():
            context['save_act_errors']= dict([(k, form_data.error_class.as_text(v)) for k, v in form_data.errors.items()])
        else:
            context['form_data']=form_data
        context["msg"]="The form contains errors! Please correct them before submitting again."
        context["msg_class"]="error_msg"
        state="ongoing"

        return context


@login_required
def alternate_data_retrieval(request):
    """
    VIEW
    reset the act form (except add and modif)
    TEMPLATES
    act/form2.html
    """
    print 'alternate view'
    context={}
    context=init_context(context)
    context['form_template']='act/form2.html'
    
    #get act
    act_id=request.POST["act_to_validate"]
    act=Act.objects.get(pk=act_id)
        
    #retrieve the act ids for each source
    act_ids=get_act_ids(act)

    #"compute" the url of the eurlex, oeil and prelex page
    urls=get_urls(act_ids["index"], act.url_prelex, act_ids["index"].dos_id)

    #get data on eurlex, oeil and prelex
    act.__dict__.update(get_data("eurlex", act_ids["eurlex"], urls["url_eurlex"], act)[0])
    fields, dg_names_oeil, resp_names_oeil=get_data("oeil", act_ids["oeil"], urls["url_oeil"], act)
    act.__dict__.update(fields)
    nb_lectures=act.nb_lectures
    #~ #prelex config_cons needs eurlex, gvt_compo needs oeil
    fields, dg_names_prelex, resp_names_prelex=get_data("prelex", act_ids["prelex"], urls["url_prelex"], act)
    act.__dict__.update(fields)
    #nb_lectures already retrieved from oeil
    act.nb_lectures=nb_lectures
#~
    #~ #store dg/resp from oeil and prelex to be displayed as text in the template
    act, context["dg_names_oeil"], context["dg_names_prelex"]=store_dg_resp(act, dg_names_oeil, dg_names_prelex, "dg")
    act, context["resp_names_oeil"], context["resp_names_prelex"]=store_dg_resp(act, resp_names_oeil, resp_names_prelex, "resp")
#~
    #~ #check multiple values for dgs with numbers
    context["dg"], act=check_multiple_dgs(act)

    form_data=ActForm(instance=act, initial={"releve_mois_init": act.releve_mois})
    context["status"]="add"
    context["urls"]=urls
    context['act']=act
    #COMMENT FOR TESTS ONLY
    temp=get_data_others(act_ids["index"], act)
    context['opals']=temp["opal"]
    context['min_attends']=temp["min_attend"]
    context["party_family"]=get_party_family({"1": act.resp_1_id, "2": act.resp_2_id, "3": act.resp_3_id})
    context['act_ids']=act_ids
    context['form_data']=form_data
    
    #display fields in template
    return HttpResponse(render_to_string(context['form_template'], context, RequestContext(request)))
   


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
    update the rapp (oeil) or resp (prelex) variables when a different person is selected from the drop down list
    TEMPLATES
    None (Ajax only)
    """
    context={}
    if request.POST["person_id"]!="":
        instance=Person.objects.get(pk=request.POST["person_id"])
        context["country"]=instance.country.pk
        party=instance.party
        context["party"]=party.party
        if request.POST["src"]=="resp":
            context["party_family"]=PartyFamily.objects.only("party_family").get(party=party, country=context["country"]).party_family
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



def update_durations(request):
    """
    VIEW
    update the duration fields (DureeAdoptionTrans, DureeProcedureDepuisPropCom, DureeProcedureDepuisTransCons, DureeTotaleDepuisPropCom and DureeTotaleDepuisTransCons)
    TEMPLATES
    None (Ajax only)
    """
    context={}
    context['duree_adopt_trans']=context['duree_proc_depuis_prop_com']=context['duree_proc_depuis_trans_cons']=context['duree_tot_depuis_prop_com']=context['duree_tot_depuis_trans_cons']=[None]*5
    duree_adopt_trans=request.POST["duree_adopt_trans"]
    duree_proc_depuis_prop_com=request.POST["duree_proc_depuis_prop_com"]
    duree_proc_depuis_trans_cons=request.POST["duree_proc_depuis_trans_cons"]
    duree_tot_depuis_prop_com=request.POST["duree_tot_depuis_prop_com"]
    duree_tot_depuis_trans_cons=request.POST["duree_tot_depuis_trans_cons"]
    transm_council=request.POST["transm_council"]
    adopt_propos_origine=request.POST["adopt_propos_origine"]
    adopt_conseil=request.POST["adopt_conseil"]
    sign_pecs=request.POST["sign_pecs"]


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

    return HttpResponse(simplejson.dumps(context), mimetype="application/json")
