from django.db import models


def file_path(instance, file_name):
	"""
	FUNCTION
	remove all spaces from the uploaded file name
	PARAMETERS
	instance: instance of the file [object]
	file_name: name of the file to process [string]
	RETURN
	new file name [string]
	"""
	file_name_new=" ".join(file_name.split())
	return '/'.join(['import', file_name_new])


class CSVUpload(models.Model):
	"""
	MODEL
	instances of csv files
	"""
	csv_file=models.FileField(upload_to=file_path)




#TEMPORARY MODELS FOR IMPORT ONLY

class ImportDosId(models.Model):
	"""
	MODEL
	temporary model: possible dos_id for each act
	"""
	dos_id=models.IntegerField(max_length=7, blank=False, null=False)
	no_celex=models.CharField(max_length=15, blank=False, null=False)

	#joined primary keys
	class Meta:
		unique_together=(("dos_id", "no_celex"), )

	def __unicode__(self):
		return u"%s" % self.dos_id


class ImportNP(models.Model):
	"""
	MODEL
	tempory model: np variables for each act (Opal)
	"""
	case_nb=models.IntegerField(max_length=10, primary_key=True)
	no_celex=models.CharField(max_length=15, blank=False, null=False)
	#country_code
	np=models.CharField(max_length=2, blank=False, null=False)
	act_type=models.CharField(max_length=40, blank=False, null=False)
	act_date=models.DateField(max_length=10, blank=True, null=True, default=None)


class ImportAdoptPC(models.Model):
	"""
	MODEL
	temporary model: adopt_pc_abs and adopt_pc_contre variables for each act
	"""
	releve_annee=models.IntegerField(max_length=4, blank=False, null=False)
	releve_mois=models.IntegerField(max_length=2, blank=False, null=False)
	no_ordre=models.IntegerField(max_length=2, blank=False, null=False)
	#list of country_codes
	adopt_pc_abs=models.CharField(max_length=18, blank=True, null=True, default=None)
	#list of country_codes
	adopt_pc_contre=models.CharField(max_length=18, blank=True, null=True, default=None)

	#joined primary keys
	class Meta:
		unique_together=(("releve_annee", "releve_mois", "no_ordre"), )