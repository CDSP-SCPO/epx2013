#models
from import_app.models import ImportMinAttend
from act.models import Country, Status, Verbatim, Act
#forms
from django import forms
from common.forms import AbstractModif, regex_propos_origine, regex_propos_chrono, min_value_year, max_value_year
from django.forms.util import ErrorList
#variables names
import act.var_name_data as var_name_data
#errors
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def get_choices_status():
    """
    FUNCTION
    get all the different statuses
    PARAMETERS
    None
    RETURN
    choices: list of all the possible statuses [list of tuples]
    """
    choices=[("","Select the status")]
    statuses=Status.objects.values_list('status', flat = True).distinct()
    for status in statuses:
        choices.append((status, status))
    return choices
    

class ImportMinAttendForm(forms.ModelForm):
    """
    FORM
    form to validate the ministers' attendance
    """
    country=forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select a country")
    status=forms.ChoiceField(choices=get_choices_status())
    #~ status=forms.ModelChoiceField(queryset=Status.objects.values_list('status', flat = True).distinct(), empty_label="Select a status")

    class Meta:
        model=ImportMinAttend
        #fields used for the validation and order
        fields = ('country', 'status', 'verbatim')

    def clean_country(self):
        #get the country_code instead of the country name
        country = self.cleaned_data['country'].pk
        return country

    def clean_verbatim(self):
        #remove extra blank spaces
        verbatim = ' '.join(self.cleaned_data['verbatim'].split()) 
        return verbatim


    def clean(self):
        # call the clean() method of the super class
        cleaned_data = super(ImportMinAttendForm, self).clean()
        
        #check that no other status is recorded in the db for the given country and verbatim
        if "country" in cleaned_data and "status" in cleaned_data and "verbatim" in cleaned_data:
            try:
                country=Country.objects.get(country_code=cleaned_data["country"])
                verbatim=Verbatim.objects.get(verbatim=cleaned_data["verbatim"])
                status_saved=Status.objects.get(country=country, verbatim=verbatim).status
                if status_saved!=cleaned_data["status"]:
                    raise forms.ValidationError("The country '"+ country.country + "' and the verbatim '" + verbatim.verbatim + "' are already associated to the status '"+ status_saved + "'! Please change the status from '" + cleaned_data["status"] + "' to '" + status_saved + "' before saving the form again.")
            except ObjectDoesNotExist, e:
                print "status not yet recorded", e
                
        return cleaned_data

    
    def save(self, *args, **kwargs):
        #if extra forms, add ids
        if "no_celex" in kwargs:
            self.instance.no_celex = kwargs.pop('no_celex', None)
            self.instance.releve_annee = kwargs.pop('releve_annee', None)
            self.instance.releve_mois = kwargs.pop('releve_mois', None)
            self.instance.no_ordre = kwargs.pop('no_ordre', None)
        instance = super(ImportMinAttendForm, self).save(*args, **kwargs)
        
        return instance


class Add(forms.Form):
    """
    FORM
    details the Add form (fields for the add mode of MinAttendForm)
    """
    act_to_validate=forms.ModelChoiceField(queryset=Act.objects.filter(attendance_pdf__isnull=False, validated_attendance=0).order_by("releve_annee", "releve_mois", "no_ordre"), empty_label="Select an act to validate")



class Modif(AbstractModif):
    """
    FORM
    details the Modif form (fields for the modification mode of MinAttendForm)
    """
    #condition to check in the clean method of the parent form
    def not_yet_validated(self, act):
        return act.validated_attendance==0
