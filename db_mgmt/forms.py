# -*- coding: utf-8 -*-
#models
from act.models import Person, Country, Party, PartyFamily, DG, DGSigle
from django import forms
#variables names
import act.var_name_data as var_name_data


class AddDG(forms.ModelForm):
    """
    FORM
    details the Add dg form
    """
    dg=forms.CharField(label=var_name_data.var_name['dg'], required=True)
    dg_sigle=forms.ModelChoiceField(label=var_name_data.var_name["dg_sigle"], queryset=DGSigle.objects.order_by('dg_sigle').all(), empty_label="Select a " + var_name_data.var_name["dg_sigle"], required=True)

    class Meta:
        model=DG
        exclude=('id', 'dg_nb')


class AddRapp(forms.ModelForm):
    """
    FORM
    details the Add rapporteur form
    """
    name=forms.CharField(label=var_name_data.var_name['rapp'],  widget=forms.TextInput(attrs={'placeholder': 'format: NAME(S) Lastname(s)'}), required=True)
    country=forms.ModelChoiceField(label=var_name_data.var_name["rapp_country"], queryset=Country.objects.order_by('country').all(), empty_label="Select a " + var_name_data.var_name["rapp_country"], required=True)
    party=forms.ModelChoiceField(label=var_name_data.var_name["rapp_party"], queryset=Party.objects.order_by('party').filter(person__src="rapp").distinct(), empty_label="Select a " + var_name_data.var_name["rapp_party"], required=True)

    class Meta:
        model=Person
        exclude=('id', 'src')


class AddResp(forms.ModelForm):
    """
    FORM
    details the Add responsible form
    """
    name=forms.CharField(label=var_name_data.var_name['resp'],  widget=forms.TextInput(attrs={'placeholder': 'format: NAME(S) Lastname(s)'}), required=True)
    country=forms.ModelChoiceField(label=var_name_data.var_name["resp_country"], queryset=Country.objects.order_by('country').all(), empty_label="Select a " + var_name_data.var_name["resp_country"], required=True)
    party=forms.ModelChoiceField(label=var_name_data.var_name["resp_party"], queryset=Party.objects.order_by('party').filter(person__src="resp").distinct(), empty_label="Select a " + var_name_data.var_name["resp_party"], required=True)
    party_family=forms.ChoiceField(label=var_name_data.var_name["resp_party_family"], choices=PartyFamily.objects.none(), required=True)

    #distinct values for party_family
    def __init__(self, *args, **kwargs):
        super(AddResp, self).__init__(*args, **kwargs)
        choices=[("", "Select a " + var_name_data.var_name["resp_party_family"])]
        choices=choices+[(pf, pf) for pf in PartyFamily.objects.values_list("party_family", flat=True).distinct()]
        self.fields['party_family'].choices = choices

    class Meta:
        model=Person
        exclude=('id', 'src')
