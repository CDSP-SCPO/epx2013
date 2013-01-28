from django import forms
#~ from models import ActsExport


class ActsExportForm(forms.Form):
	"""
	FORM
	details the ActsExport form
	"""
	sortFields = forms.ChoiceField(choices = (
	('', 'Select the sort field'),
	('year', 'year'),
	('sector', 'sector')
	))

	sortDirection = forms.ChoiceField(choices = (
	('', 'Select the sort direction'),
    ('ascending', 'ascending'),
    ('descending', 'descending'),
	))
