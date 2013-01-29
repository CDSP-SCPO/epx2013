from django import forms
from models import ActsInformationModel

class ActsInformationForm(forms.ModelForm):
	"""
	FORM
	details the ActsInformation form (fields to retrieve for the statistical analysis)
	"""
	actsToValidate=forms.ModelChoiceField(queryset=ActsInformationModel.objects.filter(validated=0), empty_label="Select an act to validate", widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
	
	codeSectRep01=forms.RegexField(regex=r'^([1-9]{2}.){3}[1-9]{2}$')
	codeSectRep02=forms.RegexField(regex=r'^([1-9]{2}.){3}[1-9]{2}$')
	baseJuridique=forms.RegexField(regex=r'^[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[EMRLD][0-9]{3,4}(-((A|P|FR|L)[0-9]+|PT)+)?$')
	
	class Meta:
		model = ActsInformationModel
		#fields NOT used for the validation
		exclude=('actId', 'validated')
