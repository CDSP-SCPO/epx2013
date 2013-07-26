from django.contrib import admin
from models import DGCodeModel, DGFullNameModel
"""
administration of DgCode and DgFullName models
"""

class DGCodeAdminClass(admin.ModelAdmin):
	"""
	details the DGCode model administration
	"""
	list_display= ('dgCode',)
	ordering= ('dgCode',)
	search_fields = ('dgCode',)

admin.site.register(DGCodeModel, DGCodeAdminClass)


class DGFullNameAdminClass(admin.ModelAdmin):
	"""
	details the DGFullName model administration
	"""
	list_display= ('dgCode', 'dgFullName',)
	list_filter= ('dgCode',)
	ordering= ('dgCode', 'dgFullName',)
	search_fields = ('dgCode', 'dgFullName',)

admin.site.register(DGFullNameModel, DGFullNameAdminClass)

