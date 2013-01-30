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
	#~ baseJuridique=forms.RegexField(regex=r'^([0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[EMRLD][0-9]{3,4}(-((A|P|FR|L)[0-9]+)|-PT([0-9]|[A-Z]){0,3}(\))?)?;\s)*[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[EMRLD][0-9]{3,4}(-((A|P|FR|L)[0-9]+)|-PT([0-9]|[A-Z]){0,3}(\))?)?$')
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
	
	class Meta:
		model = ActsInformationModel
		#fields NOT used for the validation
		exclude=('actId', 'validated')
