# -*- coding: utf-8 -*-
#models
from models import Act, Person, CodeSect, DG, Country
#forms
from django import forms
from common.forms import AbstractModif, regex_propos_origine, regex_propos_chrono, min_value_year, max_value_year
#errors
from django.forms.util import ErrorList
#variables names
import var_name_data
#reverse list with original index
from common.functions import list_reverse_enum
from common.config_file import max_cons


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

    #prevent zero value
    nb_mots=forms.IntegerField(min_value=1)

    config_cons=forms.RegexField(regex=r'^CAG|RE|ECOFIN|JAI|EPSCO|COMPET|TTE|AGRIFISH|AGRI-FISH|ENV|EYC$', required=False)

    #dgs
    dg_1=forms.ModelChoiceField(queryset=DG.objects.order_by('dg').all(), empty_label="Select a " + var_name_data.var_name["dg"], widget=forms.Select(attrs={'id': 'dg_1_id', 'name': 'dg_1_id',}), required=False)
    dg_2=forms.ModelChoiceField(queryset=DG.objects.order_by('dg').all(), empty_label="Select a " + var_name_data.var_name["dg"], widget=forms.Select(attrs={'id': 'dg_2_id', 'name': 'dg_2_id',}), required=False)
    dg_3=forms.ModelChoiceField(queryset=DG.objects.order_by('dg').all(), empty_label="Select a " + var_name_data.var_name["dg"], widget=forms.Select(attrs={'id': 'dg_3_id', 'name': 'dg_3_id',}), required=False)

    #resp* drop down list -> order nouns
    resp_1=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_1_id', 'name': 'resp_1_id',}), required=False)
    resp_2=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_2_id', 'name': "resp_2_id",}), required=False)
    resp_3=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="resp"), empty_label="Select a " + var_name_data.var_name["resp"], widget=forms.Select(attrs={'id': 'resp_3_id', 'name': "resp_3_id",}), required=False)

    #display dgs and resps names from eurlex and oeil (hidden fields to store all the names)
    hidden_dg_eurlex_dic=forms.CharField(required=False)
    hidden_dg_oeil_dic=forms.CharField(required=False)
    hidden_resp_eurlex_dic=forms.CharField(required=False)
    hidden_resp_oeil_dic=forms.CharField(required=False)
    hidden_dg_dic=forms.CharField(required=False)
    
    #prevent zero value
    duree_proc_depuis_prop_com=forms.IntegerField(min_value=1)
    duree_proc_depuis_trans_cons=forms.IntegerField(min_value=1)
    duree_tot_depuis_prop_com=forms.IntegerField(min_value=1)
    duree_tot_depuis_trans_cons=forms.IntegerField(min_value=1)

    #create fake fields so each adopt field is called in the forloop in template
    adopt_cs_contre=forms.CharField(required=False)
    adopt_pc_contre=forms.CharField(required=False)
    adopt_cs_abs=forms.CharField(required=False)
    adopt_pc_abs=forms.CharField(required=False)

    #hidden control used to populate gentleSelect selects when ajax
    countries=forms.ModelMultipleChoiceField(queryset=Country.objects.only("country_code"), required=False)

    gvt_compo=forms.CharField(required=False)
    

    #oeil
    #rapp* drop down list -> order nouns
    rapp_1=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_1_id', 'name': 'rapp_1_id',}), required=False)
    rapp_2=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_2_id', 'name': 'rapp_2_id',}), required=False)
    rapp_3=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_3_id', 'name': 'rapp_3_id',}), required=False)
    rapp_4=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_4_id', 'name': 'rapp_4_id',}), required=False)
    rapp_5=forms.ModelChoiceField(queryset=Person.objects.order_by('name').filter(src="rapp"), empty_label="Select a " + var_name_data.var_name["rapp"], widget=forms.Select(attrs={'id': 'rapp_5_id', 'name': 'rapp_5_id',}), required=False)


    #transform textbox to textarea
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model=Act
        #fields NOT used for the validation and not displayed in the form
        exclude=('id', 'releve_annee', 'releve_mois', 'no_ordre', 'titre_rmc', 'council_path', 'attendance_pdf', 'date_doc', "validated", "validated_attendance")


    def __init__(self, *args, **kwargs):
        super(ActForm, self).__init__(*args, **kwargs)

        #15 date_cons_b / date_cons_a and cons_b / cons_a maximum
        #create date_cons_b / date_cons_a and cons_b / cons_a variables
        self.cons_a_fields=[]
        self.cons_b_fields=[]
        for character in "ab":
            for index in range(1, max_cons+1):
                suffix=character+"_"+str(index)
                date_name="date_cons_"+suffix
                cons_name="cons_"+suffix
                
                #create form fields
                self.fields[date_name] = forms.DateField(required=False)
                self.fields[date_name].max_length=10
                self.fields[cons_name] = forms.CharField(required=False)
                self.fields[cons_name].max_length=500
                
                #add form fields to a list to loop over them in template
                if character=="a":
                    self.cons_a_fields.append(self[date_name])
                    self.cons_a_fields.append(self[cons_name])
                elif character=="b":
                    self.cons_b_fields.append(self[date_name])
                    self.cons_b_fields.append(self[cons_name])
        
        #don't display the country, just its code
        self.fields["countries"].label_from_instance = lambda obj: "%s" % obj.country_code

        #dynamically create drop down lists for adopt_cs and adopt_pc fields
        names=["adopt_cs_contre_", "adopt_pc_contre_", "adopt_cs_abs_", "adopt_pc_abs_"]
        cs_contre, pc_contre, cs_abs, pc_abs=([] for i in range(4))
        lists=[cs_contre, pc_contre, cs_abs, pc_abs]
        #for each variable:
        for index in range(len(names)):
            #for each of the 8 drop down lists
            for nb in range(1,9):
                name=names[index]+str(nb)
                #add drop down list to the list of fields
                self.fields[name]=forms.ModelChoiceField(queryset=Country.objects.only("country_code"), empty_label="Select a country", required=False)
                #don't display the country, just its code
                self.fields[name].label_from_instance = lambda obj: "%s" % obj.country_code
                self.fields[name].widget.attrs.update({'class' : names[index]})
                #add fields to cs_contre, pc_contre, cs_abs and pc_abs variables
                lists[index].append(self[name])
#~ 
        #~ #update the adopt variables of the form with the above variables
        self.cs_contre=cs_contre
        self.pc_contre=pc_contre
        self.cs_abs=cs_abs
        self.pc_abs=pc_abs

        #nb_mots not editable
        self.fields["nb_mots"].widget.attrs['readonly'] = True


    def clean(self):
        cleaned_data=super(ActForm, self).clean()

        #trim trailing spaces
        for field in cleaned_data:
            try:
                #only strings
                cleaned_data[field]=cleaned_data[field].strip()
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

        #~ #check errors adopt drop down lists
        names=["adopt_cs_contre", "adopt_pc_contre", "adopt_cs_abs", "adopt_pc_abs"]
        #for each variable:
        for name in names:
            adopts=[]
            #for each of the country drop down lists
            for index in range(8):
                adopt=cleaned_data.get(name+"_"+str(index+1))
                #print adopt
                if adopt!=None:
                    #~ #if the same country has been selected twice: error
                    if adopt in adopts:
                        self._errors[name]=ErrorList(["You have selected the country " + adopt.country + " more than once!"])
                    else:
                        adopts.append(adopt)

        #error message when adopt_cs_contre and adopt_cs_regle_vote="U"
        adopt_cs_contre=cleaned_data.get("adopt_cs_contre_1")
        adopt_cs_regle_vote=cleaned_data.get("adopt_cs_regle_vote")
        if adopt_cs_contre is not None and adopt_cs_regle_vote=="U":
            self._errors['adopt_cs_contre']=ErrorList([var_name_data.var_name["adopt_cs_regle_vote"] + "=U. You can't have countries for " + var_name_data.var_name["adopt_cs_contre"] + "."])
            #~ msg.append(var_name_data.var_name["adopt_cs_regle_vote"] + "=U. You can't have countries for " + var_name_data.var_name["adopt_cs_contre"] + ".")

        #assignate all the errors to the non field errors
        if msg:
            self._errors['__all__']=ErrorList(msg)

        return cleaned_data



class Add(forms.Form):
    """
    FORM
    details the Add form (fields for the add mode of ActForm)
    """
    act_to_validate=forms.ModelChoiceField(queryset=Act.objects.filter(validated=1).order_by("releve_annee", "releve_mois", "no_ordre"), empty_label="Select an act to validate")


class Modif(AbstractModif):
    """
    FORM
    details the Modif form (fields for the modification mode of ActForm)
    """
    #condition to check in the clean method of the parent form
    def not_yet_validated(self, act):
        return act.validated<2
