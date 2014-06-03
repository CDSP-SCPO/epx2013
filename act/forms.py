# -*- coding: utf-8 -*-
from django import forms
from models import Act, Person, CodeSect, DG
#modif form: add non field error
from django.forms.util import ErrorList
from django.core.exceptions import ValidationError
#variables names
import var_name_data
#reverse list with original index
from common.functions import list_reverse_enum


def check_order_fields(fields):
    """
    FUNCTION
    check if the fields are filled in order
    PARAMETERS
    fields: pers to check [list of strings]
    RETURN
    True if the order is respected or index of the first None field otherwise
    """
    for index, item in list_reverse_enum(fields):
        if item!=None:
            #check if all the previous fields are filled
            for num in xrange(len(fields[:index])):
                if fields[num]==None:
                    return str(num+1)
            #exit function
            return True
    return True


def check_duplicates(fields):
    """
    FUNCTION
    check if the fields are all different
    PARAMETERS
    fields: list of fields to check [list of strings]
    RETURN
    True if there are duplicates and None otherwise [boolean]
    """
    seen = set()
    for x in fields:
        if x!=None and x in seen:
            return True
        seen.add(x)
    return False


def check_fields(fields, name):
    """
    FUNCTION
    check if a group of fields are filled in order (from 1 to max) and are not equal (for code_sect_*, dg_*, rapp_*, resp_*)
    PARAMETERS
    fields: list of fields [list of strings]
    name: name of the field [string]
    RETURN
    msg: list of errors [list of strings]
    """
    msg=[]
    #check that all the rapp or resp are filled in order
    index=check_order_fields(fields)
    if index!=True:
        msg.append("Please select a "+var_name_data.var_name[name+"_"+index]+" first.")
    #check that all the rapp or resp are different
    if check_duplicates(fields):
        msg.append(var_name_data.var_name[name]+" must be different.")
    return msg


class ActForm(forms.ModelForm):
    """
    FORM
    fields to retrieve for the statistical analysis (Acts Information retrieval)
    """
    releve_mois_init=forms.RegexField(regex=r'^([1-9]|1[0-2]|AD|ad)$')
    #~ #eurlex
    #code_sect drop down list
    code_sect_1=forms.ModelChoiceField(queryset=CodeSect.objects.order_by('code_sect').all(), empty_label="Select a " + var_name_data.var_name["code_sect"], widget=forms.Select(attrs={'id': 'code_sect_1_id', 'name': 'code_sect_1_id',}), required=False)
    code_sect_2=forms.ModelChoiceField(queryset=CodeSect.objects.order_by('code_sect').all(), empty_label="Select a " + var_name_data.var_name["code_sect"], widget=forms.Select(attrs={'id': 'code_sect_2_id', 'name': 'code_sect_2_id',}), required=False)
    code_sect_3=forms.ModelChoiceField(queryset=CodeSect.objects.order_by('code_sect').all(), empty_label="Select a " + var_name_data.var_name["code_sect"], widget=forms.Select(attrs={'id': 'code_sect_3_id', 'name': 'code_sect_3_id',}), required=False)
    code_sect_4=forms.ModelChoiceField(queryset=CodeSect.objects.order_by('code_sect').all(), empty_label="Select a " + var_name_data.var_name["code_sect"], widget=forms.Select(attrs={'id': 'code_sect_4_id', 'name': 'code_sect_4_id',}), required=False)

    #oeil
    #rapp* drop down list -> order nouns
    rapp_1=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_1_id', 'name': 'rapp_1_id',}), required=False)
    rapp_2=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_2_id', 'name': 'rapp_2_id',}), required=False)
    rapp_3=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_3_id', 'name': 'rapp_3_id',}), required=False)
    rapp_4=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_4_id', 'name': 'rapp_4_id',}), required=False)
    rapp_5=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_5_id', 'name': 'rapp_5_id',}), required=False)

    #prelex
    config_cons=forms.RegexField(regex=r'^CAG|RE|ECOFIN|JAI|EPSCO|COMPET|TTE|AGRIFISH|AGRI-FISH|ENV|EYC$', required=False)

    #dgs
    dg_1=forms.ModelChoiceField(queryset=DG.objects.order_by('dg').all(), empty_label="Select a " + var_name_data.var_name["dg"], widget=forms.Select(attrs={'id': 'dg_1_id', 'name': 'dg_1_id',}), required=False)
    dg_2=forms.ModelChoiceField(queryset=DG.objects.order_by('dg').all(), empty_label="Select a " + var_name_data.var_name["dg"], widget=forms.Select(attrs={'id': 'dg_2_id', 'name': 'dg_2_id',}), required=False)

    #resp* drop down list -> order nouns
    resp_1=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_1_id', 'name': 'resp_1_id',}), required=False)
    resp_2=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_2_id', 'name': "resp_2_id",}), required=False)
    resp_3=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_3_id', 'name': "resp_3_id",}), required=False)

    adopt_cs_contre=forms.CharField(required=False)
    adopt_pc_contre=forms.CharField(required=False)
    adopt_cs_abs=forms.CharField(required=False)
    adopt_pc_abs=forms.CharField(required=False)
    gvt_compo=forms.CharField(required=False)

    #transform textbox to textarea
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model=Act
        #fields NOT used for the validation
        exclude=('id', 'releve_annee', 'releve_mois', 'no_ordre', 'titre_rmc', 'council_path', 'attendance_pdf', 'date_doc', 'url_prelex', "validated")

    #trim trailing spaces
    def clean(self):
        cleaned_data=super(ActForm, self).clean()
        for k in cleaned_data:
            try:
                #only strings
                cleaned_data[k]=cleaned_data[k].strip()
            except:
                pass


        #drop down lists validation: check code_sects, rapps, dgs, resps
        fields={"code_sect": 5, "rapp": 6, "dg": 3, "resp": 4}
        msg=[]
        for field in fields:
            fields_to_check=[]
            for index in xrange(1, fields[field]):
                fields_to_check.append(cleaned_data.get(field+"_"+ str(index)))
            msg.extend(check_fields(fields_to_check, field))

        #assignate all the errors to the non field errors
        if msg:
            self._errors['__all__']=ErrorList(msg)

        # Always return the full collection of cleaned data.
        return cleaned_data


class Add(forms.Form):
    """
    FORM
    details the Add form (fields for the add mode of ActForm)
    """
    act_to_validate=forms.ModelChoiceField(queryset=Act.objects.filter(validated=1).order_by("releve_annee", "releve_mois", "no_ordre"), empty_label="Select an act to validate")


class Modif(forms.Form):
    """
    FORM
    details the Modif form (fields for the modification mode of ActForm)
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
            act=Act.objects.get(releve_annee=releve_annee_modif, releve_mois=releve_mois_modif, no_ordre=no_ordre_modif, validated=2)
        except:
            print "pb find act"
            self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
            return False

        # form valid -> return True
        return True
