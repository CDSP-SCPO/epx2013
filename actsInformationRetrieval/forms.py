from django import forms
from models import ActsInformationModel

class ActsInformationForm(forms.ModelForm):
	"""
	FORM
	details the ActsInformation form (fields to retrieve for the statistical analysis)
	"""
	actsToValidate=forms.ModelChoiceField(queryset=ActsInformationModel.objects.filter(validated=0), empty_label="Select an act to validate", widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
	
	class Meta:
		model = ActsInformationModel
		#fields NOT used for the validation
		exclude=('actId', 'validated')
