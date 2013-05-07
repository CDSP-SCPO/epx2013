from django.contrib import admin
from models import DGCodeModel, DGFullNameModel
"""
administration of DgCode and DgFullName models
"""

class DGCodeAdminClass(admin.ModelAdmin):
	"""
	details the DGCode model administration
	"""
	list_display= ('acronym',)
	ordering= ('acronym',)
	search_fields = ('acronym',)

admin.site.register(DGCodeModel, DGCodeAdminClass)


class DGFullNameAdminClass(admin.ModelAdmin):
	"""
	details the DGFullName model administration
	"""
	list_display= ('dgCode', 'fullName',)
	list_filter= ('dgCode',)
	ordering= ('dgCode', 'fullName',)
	search_fields = ('dgCode', 'fullName',)

admin.site.register(DGFullNameModel, DGFullNameAdminClass)

