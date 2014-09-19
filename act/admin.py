from django.contrib import admin
from models import Act, DGSigle, DG, GvtCompo
"""
administration of Act, DGSigle and DG models
"""

class ActAdmin(admin.ModelAdmin):
	"""
	details the Act model administration
	"""
	list_display=('id', 'releve_annee', 'releve_mois', 'no_ordre',)
	ordering=('id', 'releve_annee', 'releve_mois', 'no_ordre',)
	search_fields=('id', 'releve_annee', 'releve_mois', 'no_ordre',)

admin.site.register(Act, ActAdmin)


class DGSigleAdmin(admin.ModelAdmin):
	"""
	details the DGSigle model administration
	"""
	list_display=('dg_sigle',)
	ordering=('dg_sigle',)
	search_fields=('dg_sigle',)

admin.site.register(DGSigle, DGSigleAdmin)


class DGAdmin(admin.ModelAdmin):
	"""
	details the DG model administration
	"""
	list_display=('dg_sigle', 'dg',)
	list_filter=('dg_sigle',)
	ordering=('dg_sigle', 'dg',)
	search_fields=('dg_sigle', 'dg',)

admin.site.register(DG, DGAdmin)


class GvtCompoAdmin(admin.ModelAdmin):
	"""
	details the GvtCompo model administration
	"""
	list_display=('start_date', 'end_date', 'country',)
	list_filter=('start_date', 'end_date', 'country',)
	ordering=('start_date', 'end_date', 'country',)
	search_fields=('start_date', 'end_date', 'country__country_code',)

admin.site.register(GvtCompo, GvtCompoAdmin)

