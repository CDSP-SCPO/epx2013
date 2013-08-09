# -*- coding: utf-8 -*-
from django import forms
from models import ActsInformationModel, RespProposModel, GvtCompoModel
from actsIdsValidation.models import ActsIdsModel

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

	#~ eurlexBaseJuridique=forms.RegexField(regex=r'^([0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[EMRLD][0-9]{3,4}(-((A|P|FR|L)[0-9]+)|-PT([0-9]|[A-Z]){0,3}(\))?)?;\s)*[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[EMRLD][0-9]{3,4}(-((A|P|FR|L)[0-9]+)|-PT([0-9]|[A-Z]){0,3}(\))?)?$')
	#TODO: make the regex work
	#~ 11997E080
	#~ 21997M0801
	#~ 31997R080-P2)
	#~ 42002L062-PT2)B)II)
	#~ 12002M031 -P1PTE)
	#~ 31997D063-L1PT1B)
	#~ 22002E062-PT2
	#~ 42002E062-P2PTB)II)
	#~ 42002E062-P2PTB)II); 22002E062-PT2
	#~ 42002E062-P2PTB)II); 22002E062-PT2; 11997E080
	#~ 12006E152 -A152P4PTB)

	class Meta:
		model = ActsInformationModel
		#fields NOT used for the validation
		exclude=('actId', 'validated', "prelexNationGvtPoliticalComposition")


class ActsAddForm(forms.Form):
	"""
	FORM
	details the ActsAddForm form (fields for the add mode of Acts information retrieval)
	"""
	actsToValidate=forms.ModelChoiceField(queryset=ActsInformationModel.objects.filter(validated=0), empty_label="Select an act to validate", widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))


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
	def clean(self):
		cleaned_data = super(ActsModifForm, self).clean()
		releveAnneeModif = cleaned_data.get("releveAnneeModif")
		releveMoisModif = cleaned_data.get("releveMoisModif")
		noOrdreModif = cleaned_data.get("noOrdreModif")
		#~ print "releveAnneeModif",releveAnneeModif
		#~ print "releveMoisModif",releveMoisModif
		#~ print "noOrdreModif", noOrdreModif

		try:
			actId=ActsIdsModel.objects.get(releveAnnee=releveAnneeModif, releveMois=releveMoisModif, noOrdre=noOrdreModif).id
			act=ActsInformationModel.objects.get(actId_id=actId, validated=1)
		except:
			raise forms.ValidationError("The act you're looking for hasn't been validated yet!")

		 # Always return the full collection of cleaned data.
		return cleaned_data
