from django import forms
from act.models import Act
#change variable names (first row of the csv file)
import act.var_name_data as var_name_data


class Export(forms.Form):
	"""
	FORM
	details the Export form
	"""
	def sort_fields_qs():
		"""
		FUNCTION
		get all the field names of the Act model excluding fields not useful for the statistical analysis (primary key, validated field, etc.)
		PARAMETERS
		None
		RETURN
		qs: field names [list of strings]
		"""
		qs=[]
		qs.append(('','Select the sort field'))
		qs.append(('','--------------------------------------------------'))
		qs.append(('','EURLEX'))
		qs.append(('','--------------------------------------------------'))
		excluded_list=['id', 'actids', 'releve_annee', 'releve_mois', 'releve_mois_init', 'no_ordre', 'titre_rmc', 'council_path', 'date_doc', 'url_prelex', 'notes', 'validated']
		for field in Act._meta.get_all_field_names():
			if field not in excluded_list:
				qs.append((field, var_name_data.var_name[field]))
				if field=="type_acte":
					qs.append(('','--------------------------------------------------'))
					qs.append(('','OEIL'))
					qs.append(('','--------------------------------------------------'))
				elif field=="sign_pecs":
					qs.append(('','--------------------------------------------------'))
					qs.append(('','PRELEX'))
					qs.append(('','--------------------------------------------------'))

		return qs

	sort_fields=forms.ChoiceField(choices=sort_fields_qs())

	sort_direction=forms.ChoiceField(choices=(
	('', 'Select the sort direction'),
	('ascending', 'ascending'),
	('descending', 'descending'),
	))
