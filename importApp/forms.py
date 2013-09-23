from django import forms
from django.core.exceptions import ValidationError
from models import CSVUploadModel
from django.conf import settings
import time
#variables name
import actsIdsValidation.variablesNameForIds as vnIds
import actsInformationRetrieval.variablesNameForInformation as vnInfo


def fileExtensionValidation(value):
	"""
	FUNCTION
	validates the extension of a file and raises an error if it is not a csv file
	"""
	if not value.name.endswith('.csv'):
		raise ValidationError(u'Incorrect format. Please choose a CSV file.')

class CSVUploadForm(forms.Form):
	"""
	FORM
	upload a csv file containing either prelex unique ids (disId) or acts to validate
	"""
	fileToImportChoices =(
		("","Select the import"),
		('act', 'Import acts to validate'),
		('dosId', 'Import '+vnIds.variablesNameDic['fileDosId']),
		('configCons', 'Import '+vnInfo.variablesNameDic['prelexConfigCons']),
		('codeAgenda', 'Import '+vnInfo.variablesNameDic['eurlexCodeAgenda']),
		('respPropos', 'Import '+vnInfo.variablesNameDic['prelexRespPropos']+' and relative data'),
		('adoptPC', 'Import '+vnInfo.variablesNameDic['prelexAdoptPCAbs']+' and '+vnInfo.variablesNameDic['prelexAdoptPCContre']),
		('np', 'Import opal file (NP variables)'),
		('gvtCompo', 'Import '+vnInfo.variablesNameDic['prelexNationGvtPoliticalComposition'])
	)
	fileToImport=forms.ChoiceField(choices=fileToImportChoices)

	csvFile = forms.FileField(validators=[fileExtensionValidation])

	class Meta:
		model = CSVUploadModel
