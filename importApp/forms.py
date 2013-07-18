from django import forms
from django.core.exceptions import ValidationError
from models import CSVUploadModel


def fileExtensionValidation(value):
	"""
	FUNCTION
	validates the extension of a file and raises an error if it is not a csv file
	"""
	if not value.name.endswith('.csv'):
		raise ValidationError(u'Incorrect format. Please choose an other file.')

class CSVUploadForm(forms.Form):
	"""
	FORM
	upload a csv file containing either prelex unique ids (disId) or acts to validate
	"""
	fileToImportChoices =(
		("","Select the import"), 
		('dosId', 'Import prelex unique ids (dosId)'), 
		('act', 'Import acts to validate')
	)
	fileToImport=forms.ChoiceField(choices=fileToImportChoices)
	
	csvFile = forms.FileField(label='Select a CSV file to upload.', help_text='size: max 1 Mo', validators=[fileExtensionValidation])
	
	class Meta:
		model = CSVUploadModel

