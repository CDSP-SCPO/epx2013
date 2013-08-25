from django.contrib import admin
from actsIdsValidation.models import ActsIdsModel
"""
actsIdsValidation model administration
"""

class ActsIdsAdminClass(admin.ModelAdmin):
	"""
	details the ActsIds model administration
	"""
	list_display= ('fileNoCelex', 'fileNoUniqueAnnee', 'fileNoUniqueChrono', 'fileNoUniqueType')
	list_filter= ('fileNoCelex', 'fileNoUniqueAnnee', 'fileNoUniqueChrono', 'fileNoUniqueType')
	ordering= ('fileNoCelex', 'fileNoUniqueAnnee', 'fileNoUniqueChrono', 'fileNoUniqueType')
	search_fields = ('fileNoCelex', 'fileNoUniqueAnnee', 'fileNoUniqueChrono', 'fileNoUniqueType')

admin.site.register(ActsIdsModel, ActsIdsAdminClass)
