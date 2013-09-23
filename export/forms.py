from django import forms
from actsInformationRetrieval.models import ActsInformationModel
#change variable names (first row of the csv file)
import actsInformationRetrieval.variablesNameForInformation as vn


class ActsExportForm(forms.Form):
	"""
	FORM
	details the ActsExport form
	"""
	def sortFieldsQueryset():
		"""
		FUNCTION
		get all the field names of the ActsInformationModel model excluding fields not useful for the statistical analysis (primary key and validated field)
		PARAMETERS
		None
		RETURNS
		field names in a querySet
		"""
		querySet=[]
		querySet.append(('','Select the sort field'))
		querySet.append(('','--------------------------------------------------'))
		querySet.append(('','EURLEX'))
		querySet.append(('','--------------------------------------------------'))
		excluded_list=['actId', 'releveAnnee', 'releveMois', 'releveMoisInitial', 'noOrdre', 'validated']
		for i in ActsInformationModel._meta.get_all_field_names():
			if i not in excluded_list:
				querySet.append((i, vn.variablesNameDic[i]))
				if i=="eurlexTypeActe":
					querySet.append(('','--------------------------------------------------'))
					querySet.append(('','OEIL'))
					querySet.append(('','--------------------------------------------------'))
				elif i=="oeilSignPECS":
					querySet.append(('','--------------------------------------------------'))
					querySet.append(('','PRELEX'))
					querySet.append(('','--------------------------------------------------'))

		return querySet

	sortFields = forms.ChoiceField(choices=sortFieldsQueryset())

	sortDirection = forms.ChoiceField(choices = (
	('', 'Select the sort direction'),
	('ascending', 'ascending'),
	('descending', 'descending'),
	))
