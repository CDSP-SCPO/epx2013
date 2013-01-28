from django.db import models

def uploadedFileName(instance, filename):
	"""
	FUNCTION
	remove all spaces from the uploaded file name 
	"""
	newFilename=" ".join(filename.split())
	return '/'.join(['import', newFilename])

class CsvUploadModel(models.Model):
	"""
	MODEL
	upload acts from a csv file
	"""
	csvFile = models.FileField(upload_to=uploadedFileName)
	#~ class Meta:
		#~ #not recorded in db  
		#~ managed = False

class DosIdModel(models.Model):
	"""
	MODEL
	dosIds of the prelex acts (unique prelex ids)
	"""
	dosId = models.IntegerField(max_length=7, primary_key=True)
	proposOrigine = models.CharField(max_length=4)
	proposAnnee = models.IntegerField(max_length=4)
	proposChrono = models.CharField(max_length=7)
	splitNumber = models.IntegerField(max_length=1, blank=True, null=True, default=None)
