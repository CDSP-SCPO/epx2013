"""
common functions used by views of other modules (act, act_ids and attendance)
"""

#models
from act.models import Act
from act_ids.models import ActIds
from import_app.models import ImportMinAttend

#log
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_ordered_queryset(releve_annee, releve_mois, no_ordre):
    """
    FUNCTION
    get the acts from the ids in parameter and order the queryset according to the status and country (Ministers' attendance validation page)
    PARAMETERS
    releve_mois: releve_mois variable [int]
    releve_annee: releve_annee variable [int]
    no_ordre: no_ordre variable [int]
    RETURN
    sorted queryset [Queryset object]
    """
    queryset_no_order=ImportMinAttend.objects.filter(releve_annee=releve_annee, releve_mois=releve_mois, no_ordre=no_ordre)
    #1st: rows without status, ordered by country
    queryset=queryset_no_order.filter(status=None).order_by("country")
    #must hit the database to have _result_cache working
    len(queryset)

    #2d: rows with a status, ordered by country 
    queryset_status=queryset_no_order.exclude(status=None).order_by("country")
    for query in queryset_status:
        queryset._result_cache.append(query)

    return queryset


def get_ajax_errors(form):
    """
    FUNCTION
    format the form errors so they can be read with ajax
    PARAMETERS
    form: form to process [Form object]
    RETURN
    dict: form errors stored in a dictionary [dictionary]
    """
    return dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items()])
    

def check_add_modif_forms(request, response, Add, Modif, form):
    """
    FUNCTION
    check if we are adding or modifying an act and check if the add or modif form is valid
    PARAMETERS
    request: request variable [HttpRequest object]
    response: all the different forms [dictionary]
    form: name of the form that uses the function ("act", "act_ids", "min_attend") [string]
    RETURN
    mode: "add" if selection of an act to add from the drop down list, "modif" if click on the modif_act button and None otherwise [string]
    add_modif: same than mode but return None if the add or modif form is not valid [string]
    queryset: act / ministers' attendance to validate or modify [Act or ImportMinAttend model instance(s)]
    response: all the forms being used or to use [dictionary]
    """
    print "check_add_modif_forms"
    logger.debug('check_add_modif_forms')
    #~ logger.debug('request.POST' + str(request.POST))
    add_modif=mode=queryset=None

    #adding of an act (validation of a new act)
    if request.POST["act_to_validate"]!="" and "modif_act" not in request.POST:
        logger.debug('mode=add')
        mode="add"
        add=Add(request.POST)
        if not request.is_ajax():
            response['add']=add
        #if an act has been selected in the drop down list
        if add.is_valid():
            add_modif="add"
            act_to_validate=add.cleaned_data['act_to_validate']
            #get the primary key
            act_ids=act_to_validate.pk
            queryset=Act.objects.get(id=act_ids)
            if form=="attendance_form":
                queryset=get_ordered_queryset(queryset.releve_annee, queryset.releve_mois, queryset.no_ordre)
                
        #empty selection for the drop down list
        else:
            if request.is_ajax():
                response['add_act_errors']=get_ajax_errors(add)
            print "add form not valid", add.errors
            logger.debug('add form not valid' + str(add.errors))

    #modification of an act -> display
    #"modif_act" in request.POST or request.POST["modif_button_clicked"]=="yes" -> display act to modify
    #request.POST["modif_button_clicked"]=="yes" -> with ajax
    #(request.POST["ids_radio"]=="releve" and request.POST["releve_annee_modif"]!="") or (request.POST["ids_radio"]=="propos" and request.POST["propos_annee_modif"]!="") -> update or save act to modify (or errors)
    elif "modif_act" in request.POST or request.POST["modif_button_clicked"]=="yes" or (request.POST["ids_radio"]=="releve" and request.POST["releve_annee_modif"]!="") or (request.POST["ids_radio"]=="propos" and request.POST["propos_annee_modif"]!=""):
        mode="modif"
        logger.debug('mode=modif')
        modif=Modif(request.POST)
        if not request.is_ajax():
            response['modif']=modif
        if modif.is_valid():
            #we display the act to modify it
            add_modif="modif"
                        
            #releve ids
            fields={}
            if request.POST["ids_radio"]=="releve":
                Model=Act
                fields['releve_annee']=modif.cleaned_data['releve_annee_modif']
                fields['releve_mois']=modif.cleaned_data['releve_mois_modif']
                fields['no_ordre']=modif.cleaned_data['no_ordre_modif']
            elif request.POST["ids_radio"]=="propos":
                Model=ActIds
                fields['src']='index'
                fields['propos_origine']=modif.cleaned_data['propos_origine_modif']
                fields['propos_annee']=modif.cleaned_data['propos_annee_modif']
                fields['propos_chrono']=modif.cleaned_data['propos_chrono_modif']

            #get Act object
            queryset=Model.objects.get(**fields)
            if Model!=Act:
                queryset=queryset.act

            #in attendance form, get attendances from ImportMinAttend model
            if form=="attendance_form":
                queryset=get_ordered_queryset(queryset.releve_annee, queryset.releve_mois, queryset.no_ordre)
                
        else:
            #errors on form
            if request.is_ajax():
                response['modif_act_errors']=get_ajax_errors(modif)
            print "modif form not valid", modif.errors
            logger.debug('modif form not valid' + str(modif.errors))

    return mode, add_modif, queryset, response
