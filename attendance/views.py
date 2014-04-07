#-*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
#many instances of the same ImportMinAttendForm form
from django.forms.models import modelformset_factory, formset_factory
from import_app.models import ImportMinAttend
from act.models import Country, Verbatim, Status
from act_ids.models import ActIds
from history.models import History
from forms import ImportMinAttendForm, Add, Modif
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#get the add_modif fct
from act_ids.views import add_modif_fct
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
from act.get_data_others import link_act_min_attend


class MinAttendUpdate(UpdateView):
    """
    VIEW
    displays the page to validate ministers' attendance
    TEMPLATES
    min_attend/index.html
    """
    model = ImportMinAttend
    fields = ['country', 'verbatim', 'status']
    form_class=ImportMinAttendForm
    template_name = 'attendance/index.html'
    object=None
    nb_extra_forms=3

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        Pass parameters to the context object for get requests
        """
        print "get"
        return self.render_to_response(self.get_context_data())


    def get_context_data(self, **kwargs):
        """
        pass generic parameters to the context object so it can be viewed inside the template
        """
        print "get_context_data"
        context = super(MinAttendUpdate, self).get_context_data(**kwargs)
        if "add" not in context:
            context['add'] = Add()
        if "modif" not in context:
            context['modif'] = Modif()
        if "formset" not in context:
            context["formset"]=formset_factory(self.form_class, extra=self.nb_extra_forms)
        context['form_template'] = 'attendance/form.html'
        context['display_name'] = var_name_ids.var_name
        context['display_name'].update(var_name_data.var_name)
        #display the length of the drop down list
        context['attendance_form']=True
        if "state" not in context:
            context['state']="display"
        return context


    def get_act_ids(self, post, add_modif):
        """
        FUNCTION
        return an act_ids instance from the Add or Modif form
        PARAMETERS
        post: request.POST object [dictionary]
        add_modif: "add" or "modif" [string]
        RETURN
        act_ids: act_ids instance [ActIds model instance]
        """
        #if adding ministers's attendance for an act
        if add_modif=="add":
            act_ids=post['act_to_validate'].split(",")
        else:
            act_ids=[post['releve_annee_modif'], post['releve_mois_modif'], post['no_ordre_modif']]
        act_ids=ActIds.objects.get(src="index", act__releve_annee=act_ids[0], act__releve_mois=act_ids[1], act__no_ordre=act_ids[2])
        return act_ids

    def post(self, request, *args, **kwargs):
        """
        The form is posted
        """
        print "post"
        context={}
        mode, add_modif, attendances, context=add_modif_fct(request, context, Add, Modif, "min_attend")
        #~ print "context beginning post", context
#~ #~
        #if any of this key is present in the response dictionary -> no act display and return the errors with a json object
        #otherwise display act and return the html form of the act to validate or modif in a string format
        keys=["msg", "add_act_errors", "modif_act_errors", "update_act_errors"]
#~ #~
        #if click on OK or MODIF but no act selected or no releve* entered
        if mode==None:
            context=self.get_context_data(**context)
        #if selection of an act in the drop down list (and click on Ok) or input releves* and click on MODIF
        else:
            #if we are about to add or modif an act (the add or modif form is valid)
            if add_modif!=None:
                #get act_ids instance
                act_ids=self.get_act_ids(request.POST, add_modif)

                #set the number of forms to the number of ministers + 3 extra form to fill if needed
                MinAttendFormSet = modelformset_factory(self.model, form=self.form_class, fields=self.fields, extra=len(attendances), max_num=len(attendances)+self.nb_extra_forms)
                formset = MinAttendFormSet(request.POST, queryset=attendances)

                #saves the ministers' attendances
                if 'save_attendance' in request.POST:
                    if formset.is_valid():
                        context=self.form_valid(formset, request, context, add_modif, act_ids)
                    else:
                        context=self.form_invalid(formset, request, context)
                #update status
                elif "update_status" in request.POST:
                    #we are going to update the status if possible
                    post_values = request.POST.copy()
                    for index in range(len(formset)):
                        try:
                            #remove extra blank spaces verbatim
                            post_values["form-"+str(index)+"-verbatim"] = ' '.join(post_values["form-"+str(index)+"-verbatim"].split())
                            verbatim=Verbatim.objects.get(verbatim=post_values["form-"+str(index)+"-verbatim"])
                            status=Status.objects.get(verbatim=verbatim, country=Country.objects.get(country_code=post_values["form-"+str(index)+"-country"])).status
                            post_values["form-"+str(index)+"-status"] = status
                        except Exception, e:
                            print "The verbatim does not exist yet", e
                    #update status
                    formset=MinAttendFormSet(post_values)


                if not any(key in context for key in keys) or not request.is_ajax() and context["state"]!="saved":
                    print 'act_to_validate display'
                    #get the data of the act
                    if "add_act" in request.POST or "modif_act" in request.POST:
                        formset=MinAttendFormSet(queryset=attendances)
                        if "add_act" in request.POST:
                            context["status"]="add"
                        else:
                            context["status"]="modif"

                    context['formset']=formset
                    context['no_celex']=act_ids.no_celex
                    context['attendance_pdf']=act_ids.act.attendance_pdf

                context['mode']=mode

            if request.is_ajax():
                #save act (with or without errors) or act display and modif (with errors)
                if any(key in context for key in keys):
                    return HttpResponse(simplejson.dumps(context), mimetype="application/json")
                else:
                    #act display or modif (without errors)
                    return HttpResponse(render_to_string(context['form_template'], context, RequestContext(request)))

        if request.is_ajax():
            #no act has been selected-> do nothing
            return HttpResponse(simplejson.dumps(""), mimetype="application/json")


        return self.render_to_response(self.get_context_data(**context))


    def form_valid(self, formset, request, context, add_modif, act_ids):
        """
        Called if all forms are valid.
        """
        print "form_valid"
        #save validated ministers' attendances (MinAttend model)
        #~ instances = formset.save()
        for form in formset.forms:
            #if the form has been changed
            if form.has_changed():
                #update status in ImportMinAttend with same verbatim and empty status
                for instance in ImportMinAttend.objects.filter(verbatim=form.cleaned_data["verbatim"], status=None):
                    print "instance ImportMinAttend", instance.pk
                    instance.status=form.cleaned_data["status"]
                    instance.save()

                #add releve_ids and no_celex for extra forms not already in ImportMinAttend and save extra forms
                if form.empty_permitted:
                    form.save(no_celex=act_ids.no_celex, releve_annee=act_ids.act.releve_annee, releve_mois=act_ids.act.releve_mois, no_ordre=act_ids.act.no_ordre)

            #save all the "normal" forms, even unchanged
            if not form.empty_permitted:
                form.save()

        #update dictionary (Verbatim and status models) and save attendances in MinAttend
        link_act_min_attend(act_ids)

        context["state"]="saved"
        context["msg"]="The act " + str(act_ids.act) + " has been validated!"
        context["msg_class"]="success_msg"

        #save in history
        History.objects.create(action=add_modif, form="attendance", act=act_ids.act, user=request.user)

        #empty forms
        context['add'] = Add()
        context['modif'] = Modif()

        return context


    def form_invalid(self, formset, request, context):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        print "form_invalid", formset.errors
        if request.is_ajax():
            context['save_act_errors']= dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items() for form in formset])
        else:
            context['formset']=formset
        context["msg"]="The form contains errors! Please correct them before submitting again."
        context["msg_class"]="error_msg"
        context["state"]="ongoing"

        return context


def reset_form_attendance(request):
    """
    VIEW
    reset the act form (except add and modif)
    TEMPLATES
    act/form.html
    """
    context={}
    context['display_name']=var_name_ids.var_name
    context['display_name'].update(var_name_data.var_name)
    #number of blank forms to display
    nb=2
    context["formset"]=formset_factory(ImportMinAttendForm, extra=nb)
    return render_to_response('attendance/form.html', context, context_instance=RequestContext(request))
