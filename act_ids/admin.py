from django.contrib import admin
from models import ActIds
"""
act_ids model administration
"""

class ActAdmin(admin.ModelAdmin):
    """
    details the Act model administration
    """
    list_display=('src', 'no_celex', 'act', 'no_unique_annee', 'no_unique_chrono', 'no_unique_type')
    list_filter=('src', 'no_celex')
    ordering=('src', 'no_celex')
    search_fields=('src', 'no_celex')

admin.site.register(ActIds, ActAdmin)
