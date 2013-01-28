from django.db import models

	
class ActsExportDb(models.Model):
	"""
	MODEL
	gives the ActsExportDb model (table from the database)
	"""
	title = models.CharField(max_length=20)
	year = models.IntegerField(max_length=4, blank=False)
	sector = models.CharField(max_length=50)
	
	#~ def __unicode__(self):
		#~ return self.title

