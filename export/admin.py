from django.contrib import admin
from export.models import ActsExportDb
"""
ActsExport model administration
"""

class ActsExportAdminClass(admin.ModelAdmin):
	"""
	details the ActsExport model administration
	"""
	list_display= ('title', 'year', 'sector')
	list_filter= ('title', 'year', 'sector')
	ordering= ('year', 'sector', 'title', )
	search_fields = ('title', 'year', 'sector')

admin.site.register(ActsExportDb, ActsExportAdminClass)
