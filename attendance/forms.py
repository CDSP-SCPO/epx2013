from django import forms
from import_app.models import ImportMinAttend
from act.models import Country, Status
#variables names
import act.var_name_data as var_name_data


class MinAttendForm(forms.ModelForm):
    """
    FORM
    form to validate the ministers' attendance
    """
    country=forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select the country")
    status=forms.ModelChoiceField(queryset=Status.objects.values_list('status', flat = True).distinct(), empty_label="Select the status")

    class Meta:
        model=ImportMinAttend
        #fields NOT used for the validation
        fields = ('country', 'verbatim', 'status')

    def __init__(self, *args, **kwargs):
        super(MinAttendForm, self).__init__(*args, **kwargs)
        #add class to each field to recognize them
        self.fields['country'].widget.attrs.update({'class' : 'country'})
        self.fields['verbatim'].widget.attrs.update({'class' : 'verbatim'})
        self.fields['status'].widget.attrs.update({'class' : 'status'})


def format_releve_ids(releves):
    releve_annee=var_name_data.var_name['releve_annee'] + "=" + str(releves[0])
    releve_mois=var_name_data.var_name['releve_mois'] + "=" + str(releves[1])
    no_ordre=var_name_data.var_name['no_ordre'] + "=" + str(releves[2])
    return releve_annee + ", " + releve_mois + ", " + no_ordre


class Add(forms.Form):
    """
    FORM
    details the Add form (fields for the add mode of MinAttendForm)
    """
    act_to_validate=forms.ChoiceField()

    #no duplicate in the drop down list
    def __init__(self, *args, **kwargs):
        super(Add, self).__init__(*args, **kwargs)

        #create list of different acts to validate
        acts_list=[]
        qs=ImportMinAttend.objects.filter(validated=0)
        for act in qs:
            name=[int(act.releve_annee),int(act.releve_mois),int(act.no_ordre)]
            if name not in acts_list:
                acts_list.append(name)
        #add name to be displayed in the form to have a list of tuples
        for index in range(len(acts_list)):
            acts_list[index]=(acts_list[index], format_releve_ids(acts_list[index]))

        #empty label
        acts_list=[('','Select an act to validate')] + acts_list

        #assign the choices to the drop down list
        self.fields['act_to_validate'].choices = acts_list



class Modif(forms.Form):
    """
    FORM
    details the Modif form (fields for the modification mode of MinAttendForm)
    """
    #ids input boxes used for the modification
    releve_annee_modif=forms.IntegerField(label=var_name_data.var_name['releve_annee'], min_value=1957, max_value=2020)
    releve_mois_modif=forms.IntegerField(label=var_name_data.var_name['releve_mois'], min_value=1, max_value=12)
    no_ordre_modif=forms.IntegerField(label=var_name_data.var_name['no_ordre'], min_value=1, max_value=99)

    #check if the searched act already exists in the db and has been validated
    def is_valid(self):
        # run the parent validation first
        valid=super(Modif, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        #if the form is valid
        releve_annee_modif=self.cleaned_data.get("releve_annee_modif")
        releve_mois_modif=self.cleaned_data.get("releve_mois_modif")
        no_ordre_modif=self.cleaned_data.get("no_ordre_modif")

        try:
            act=ImportMinAttend.objects.get(releve_annee=releve_annee_modif, releve_mois=releve_mois_modif, no_ordre=no_ordre_modif, validated=1)
        except:
            print "pb find act"
            self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
            return False

        # form valid -> return True
        return True
