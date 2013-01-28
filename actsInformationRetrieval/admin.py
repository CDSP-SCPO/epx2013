from django.contrib import admin
from models import DgCodeModel, DgFullNameModel
"""
administration of DgCode and DgFullName models
"""

class DgCodeAdminClass(admin.ModelAdmin):
	"""
	details the DgCode model administration
	"""
	list_display= ('acronym',)
	ordering= ('acronym',)
	search_fields = ('acronym',)

admin.site.register(DgCodeModel, DgCodeAdminClass)


class DgFullNameAdminClass(admin.ModelAdmin):
	"""
	details the DgFullName model administration
	"""
	list_display= ('dgCode', 'fullName',)
	list_filter= ('dgCode',)
	ordering= ('dgCode', 'fullName',)
	search_fields = ('dgCode', 'fullName',)

admin.site.register(DgFullNameModel, DgFullNameAdminClass)

