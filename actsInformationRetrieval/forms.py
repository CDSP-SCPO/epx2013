# -*- coding: utf-8 -*-
from django import forms
from models import ActsInformationModel, RespProposModel, GvtCompoModel
from actsIdsValidation.models import ActsIdsModel
#modif form: add non field error
from django.forms.util import ErrorList

class ActsInformationForm(forms.ModelForm):
	"""
	FORM
	fields to retrieve for the statistical analysis (Acts Information retrieval)
	"""
	#eurlex
	eurlexFullCodeSectRep01=forms.RegexField(regex=r'^[0-9]{2}(.[0-9]{2}){3}$', required=False)
	eurlexFullCodeSectRep02=forms.RegexField(regex=r'^[0-9]{2}(.[0-9]{2}){3}$', required=False)
	eurlexFullCodeSectRep03=forms.RegexField(regex=r'^[0-9]{2}(.[0-9]{2}){3}$', required=False)
	eurlexFullCodeSectRep04=forms.RegexField(regex=r'^[0-9]{2}(.[0-9]{2}){3}$', required=False)

	#prelex
	prelexConfigCons=forms.RegexField(regex=r'^CAG|RE|ECOFIN|JAI|EPSCO|COMPET|TTE|AGRIFISH|AGRI-FISH|ENV|EYC$', required=False)

	#respPropos drop down list -> order nouns
	prelexRespProposId1=forms.ModelChoiceField(queryset=RespProposModel.objects.only("respPropos").order_by('respPropos').all(), empty_label="Select a RespPropos", widget=forms.Select(attrs={'onchange': 'update_respPropos(this.id, this.value)'}))
	prelexRespProposId2=forms.ModelChoiceField(queryset=RespProposModel.objects.only("respPropos").order_by('respPropos').all(), empty_label="Select a RespPropos", widget=forms.Select(attrs={'onchange': 'update_respPropos(this.id, this.value)'}))
	prelexRespProposId3=forms.ModelChoiceField(queryset=RespProposModel.objects.only("respPropos").order_by('respPropos').all(), empty_label="Select a RespPropos", widget=forms.Select(attrs={'onchange': 'update_respPropos(this.id, this.value)'}))

	class Meta:
		model = ActsInformationModel
		#fields NOT used for the validation
		exclude=('actId', 'validated', "prelexNationGvtPoliticalComposition")

	#trim trailing spaces
	def clean(self):
		cleaned_data = self.cleaned_data
		for k in self.cleaned_data:
			try:
				#only strings
				cleaned_data[k] = self.cleaned_data[k].strip()
			except:
				pass
		return cleaned_data


class ActsAddForm(forms.Form):
	"""
	FORM
	details the ActsAddForm form (fields for the add mode of Acts information retrieval)
	"""
	actsToValidate=forms.ModelChoiceField(queryset=ActsInformationModel.objects.only("releveAnnee", 'releveMois', 'noOrdre').filter(validated=0), empty_label="Select an act to validate", widget=forms.Select(attrs={'onchange': 'display_or_update_act("add_act")'}))


class ActsModifForm(forms.Form):
	"""
	FORM
	details the ActsModifForm form (fields for the modification mode of Acts information retrieval)
	"""
	#ids input boxes used for the modification
	releveAnneeModif=forms.IntegerField(label='ReleveAnnee', min_value=1957, max_value=2020)
	releveMoisModif=forms.IntegerField(label='ReleveMois', min_value=1, max_value=12)
	noOrdreModif=forms.IntegerField(label='NoOrdre', min_value=1, max_value=99)

	#check if the searched act already exists in the db and has been validated
	def is_valid(self):
		# run the parent validation first
		valid = super(ActsModifForm, self).is_valid()

		# we're done now if not valid
		if not valid:
			return valid

		#if the form is valid
		releveAnneeModif = self.cleaned_data.get("releveAnneeModif")
		releveMoisModif = self.cleaned_data.get("releveMoisModif")
		noOrdreModif = self.cleaned_data.get("noOrdreModif")

		try:
			actId=ActsIdsModel.objects.get(releveAnnee=releveAnneeModif, releveMois=releveMoisModif, noOrdre=noOrdreModif).id
			act=ActsInformationModel.objects.get(actId_id=actId, validated=1)
		except:
			print "pb find act"
			self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
			return False

		# form valid -> return True
		return True
