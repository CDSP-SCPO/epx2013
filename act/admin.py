from django.contrib import admin
from models import DGSigle, DG
"""
administration of DGSigle and DG models
"""

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

