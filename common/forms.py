"""
common functions used by forms of other modules (act, act_ids and attendance)
"""

#models
from models import ActIds
from act.models import Act
#forms
from django import forms
from django.forms.util import ErrorList
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data


def regex_propos_origine():
    #(?i): case insensitive
    return r'^(?i)COM|JAI|BCE|EM|CONS|CJEU$'


def regex_propos_chrono():
    return r'^([0-9]([0-9]?){4})(-[1-9][0-9]?)?$'


def min_value_year():
    return 1957

    
def max_value_year():
    return 2020


class AbstractModif(forms.Form):
    """
    FORM
    details the abstract Modif form (used for ActIds form, Act form and MinAttend form)
    """
    CHOICES=(
        ('releve','releve ids'),
        ('propos','propos ids')
    )
    #radio button
    ids_radio = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), initial=CHOICES[0][0])

    #releve ids input boxes for the modification
    releve_annee_modif=forms.IntegerField(label=var_name_data.var_name['releve_annee'], min_value=min_value_year(), max_value=max_value_year())
    releve_mois_modif=forms.IntegerField(label=var_name_data.var_name['releve_mois'], min_value=1, max_value=12)
    no_ordre_modif=forms.IntegerField(label=var_name_data.var_name['no_ordre'], min_value=1, max_value=99)

    #releve ids input boxes for the modification
    propos_origine_modif=forms.RegexField(label=var_name_ids.var_name['propos_origine'], regex=regex_propos_origine())
    propos_annee_modif=forms.IntegerField(label=var_name_ids.var_name['propos_annee'], min_value=min_value_year(), max_value=max_value_year())
    propos_chrono_modif=forms.RegexField(label=var_name_ids.var_name['propos_chrono'], regex=regex_propos_chrono())


    class Meta:
        #abstract form
        abstract = True
        

    #upper case for propos origine
    def clean_propos_origine_modif(self):
        return self.cleaned_data['propos_origine_modif'].upper()


    def clean(self):
        cleaned_data = super(Modif, self).clean()
        #~ cleaned_data=self.cleaned_data

        #releve ids or propos ids?
        ids = cleaned_data.get("ids_radio")
        errors=[]
        
        #we use releve ids -> do not validate propos ids
        if ids == 'releve':
            errors=['propos_origine_modif', 'propos_annee_modif', 'propos_chrono_modif']
        #we use propos ids -> do not validate releve ids
        elif ids=="propos":
            errors=['releve_annee_modif', 'releve_mois_modif', 'no_ordre_modif']

        #remove validation errors
        for error in errors:
            if error in self.errors:
                del self.errors[error]

        return cleaned_data
            
        
    #check if the searched act already exists in the db and has been validated
    def is_valid(self):
        # run the parent validation first
        valid=super(Modif, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        #if the form is valid
        ids=self.cleaned_data.get("ids_radio")

        #check releve_ids
        if ids=="releve":
            releve_annee_modif=self.cleaned_data.get("releve_annee_modif")
            releve_mois_modif=self.cleaned_data.get("releve_mois_modif")
            no_ordre_modif=self.cleaned_data.get("no_ordre_modif")
            
            try:
                act=Act.objects.get(releve_annee=releve_annee_modif, releve_mois=releve_mois_modif, no_ordre=no_ordre_modif)
                if act.validated==0:
                    self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
                    return False
            except Exception, e:
                self._errors['__all__']=ErrorList([u"The act you are looking for doesn't exist in our database!"])
                return False
                
        else:
            #check propos_ids
            propos_origine_modif=self.cleaned_data.get("propos_origine_modif")
            propos_annee_modif=self.cleaned_data.get("propos_annee_modif")
            propos_chrono_modif=self.cleaned_data.get("propos_chrono_modif")

            try:
                act=ActIds.objects.get(src="index", propos_origine=propos_origine_modif, propos_annee=propos_annee_modif, propos_chrono=propos_chrono_modif)
                if act.act.validated==0:
                    self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
                    return False
            except Exception, e:
                self._errors['__all__']=ErrorList([u"The act you are looking for doesn't exist in our database!"])
                return False
        

        # form valid -> return True
        return True
