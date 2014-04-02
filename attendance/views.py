#-*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
#many instances of the same MinAttendForm form
from django.forms.models import modelformset_factory, formset_factory
from import_app.models import ImportMinAttend
from forms import MinAttendForm, Add, Modif
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#get the add_modif fct
from act_ids.views import add_modif_fct
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data



class MinAttendUpdate(UpdateView):
    """
    VIEW
    displays the page to validate ministers' attendance
    TEMPLATES
    min_attend/index.html
    """
    form_class=MinAttendForm
    template_name = 'attendance/index.html'
    #~ queryset = ImportMinAttend.objects.filter(validated=False)
    #~ fields = ['name']
    #~ template_name_suffix = '_update_form'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        Pass parameters to the context object for get requests
        """
        self.object = None
        context={}
        context['add'] = Add()
        context['modif'] = Modif()

        #show one unbound form
        nb=2
        #~ form_class = self.get_form_class()
        #~ context["form"]=self.get_form(form_class)
        context["formset"]=formset_factory(self.form_class, extra=nb)

        return self.render_to_response(self.get_context_data(**context))


    def get_context_data(self, **kwargs):
        """
        pass genric parameters to the context object so it can be viewed inside the template
        """
        context = super(MinAttendUpdate, self).get_context_data(**kwargs)
        context['form_template'] = 'attendance/form.html'
        context['display_name'] = var_name_ids.var_name
        context['display_name'].update(var_name_data.var_name)
        #display the length of the drop down list
        context['attendance_form']=True
        if "state" not in context:
            context['state']="display"
        return context


    def post(self, request, *args, **kwargs):
        """
        The form is posted
        """
        print "post"
        context={}
        mode, add_modif, attendances, context=add_modif_fct(request, context, Add, Modif, "min_attend")
#~ #~
        #if any of this key is present in the response dictionary -> no act display and return the errors with a json object
        #otherwise display act and return the html form of the act to validate or modif in a string format
        keys=["msg", "add_act_errors", "modif_act_errors", "update_act_errors"]
#~ #~
        #if selection of an act in the drop down list or click on the modif_act button
        if mode!=None:
            #if we are about to add or modif an act (the add or modif form is valid)
            if add_modif!=None:
                #saves the ministers' attendances
                if 'save_attendance' in request.POST:
                    #set the number of forms to the number of ministers + 3 extra form to fill if needed
                    MinAttendFormSet = modelformset_factory(self.form_class, extra=len(attendances), max_num=3)
                    formset=MinAttendFormSet(request.POST, validated=True)
                    #~ formset=MinAttendFormSet(request.POST, queryset=attendances)
                    if formset.is_valid():
                        context=self.form_valid(formset, request, context, add_modif)
                    else:
                        context=self.form_invalid(formset, request, context)
                #update status
                elif "update_status" in request.POST:
                    formset=MinAttendFormSet(request.POST)
                    if formset.is_valid():
                        for index in range(len(formset)):
                            try:
                                verbatim=Verbatim.objects.get(verbatim=formset.forms[index].cleaned_data['verbatim'])
                                status=Status.objects.get(verbatim=verbatim, country=Country.objects.get(country_code=formset.forms[index].cleaned_data['country'])).status
                                formset.forms[index].fields['status'] = status
                            except Exception, e:
                                print "The verbatim does not exist yet", e
                    else:
                        context=self.form_invalid(formset, request, context)

                if not any(key in context for key in keys) or not request.is_ajax() and context["state"]!="saved":
                    print 'act_to_validate display'
                    #get the data of the act
                    if "add_act" in POST or "modif_act" in POST:
                        formset=MinAttendFormSet(queryset=attendances)
                        if "add_act" in POST:
                            context["status"]="add"
                        else:
                            context["status"]="modif"
                    else:
                        formset=MinAttendFormSet(request.POST, queryset=attendances)

                    context['formset']=formset
                    act_ids=request.POST['act_to_validate']
                    act_ids=ActIds.objects.get(src="index", act__releve_annee=act_ids[0], act__releve_mois=act_ids[1], act__no_ordre=act_ids[2])
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


    def form_valid(formset, request, context, add_modif):
        """
        Called if all forms are valid.
        """
        #delete old objects
        act_ids=request.POST['act_to_validate']
        old_acts=ImportMinAttend.objects.filter(releve_annee=act_ids[0], releve_mois=act_ids[1], no_ordre=act_ids[2])
        for old_act in old_acts:
            print "deletion of ", old_act.pk, old_act.releve_annee, old_act.releve_mois, old_act.no_ordre
            old_act.delete()

        #save validated ministers' attendances (MinAttend model)
        instances = formset.save()

        #update dictionary (Verbatim and status models) and save attendances in MinAttend
        link_act_min_attend(act_ids)

        context["state"]="saved"
        context["msg"]="The act " + str(act) + " has been validated!"
        context["msg_class"]="success_msg"

        #save in history
        History.objects.create(action=add_modif, form="attendance", act=act, user=request.user)

        return context


    def form_invalid(formset, request, context):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        print "form_data not valid", formset.errors
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
    context["formset"]=formset_factory(MinAttendForm, extra=nb)
    return render_to_response('attendance/form.html', context, context_instance=RequestContext(request))
