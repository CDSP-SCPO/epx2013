from django.contrib import admin
from models import ActIds
"""
act_ids model administration
"""

class ActAdmin(admin.ModelAdmin):
	"""
	details the Act model administration
	"""
	list_display=('no_celex', 'no_unique_annee', 'no_unique_chrono', 'no_unique_type')
	list_filter=('no_celex', 'no_unique_annee', 'no_unique_chrono', 'no_unique_type')
	ordering=('no_celex', 'no_unique_annee', 'no_unique_chrono', 'no_unique_type')
	search_fields=('no_celex', 'no_unique_annee', 'no_unique_chrono', 'no_unique_type')

admin.site.register(ActIds, ActAdmin)
