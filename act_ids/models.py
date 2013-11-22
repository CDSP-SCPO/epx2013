from django.db import models
from act.models import Act
from django.core.exceptions import ValidationError


class ActIds(models.Model):
	"""
	MODEL
	instances of acts ids
	for each act, several sources: index file (monthly council summary), eurlex, oeil, prelex
	"""
	#when importing an index file, acts are inserted into the db except if:
	#a no_celex has been added while importing a dos_id or opal file

	#src="index", "eurlex", "oeil" or "prelex"
	src=models.CharField(max_length=6, default="index", db_index=True)
	url_exists=models.BooleanField(default=True)
	#no_celex for index file must be unique
	no_celex=models.CharField(max_length=15, blank=True, null=True, default=None)
	no_unique_annee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
	no_unique_type=models.CharField(max_length=4, blank=True, null=True, default=None)
	no_unique_chrono=models.CharField(max_length=5, blank=True, null=True, default=None)
	propos_annee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
	propos_chrono=models.CharField(max_length=7, blank=True, null=True, default=None)
	propos_origine=models.CharField(max_length=4, blank=True, null=True, default=None)
	dos_id=models.IntegerField(max_length=7, blank=True, null=True, default=None)
	act=models.ForeignKey(Act)

	#joined primary keys
	class Meta:
		unique_together=(("act", "src"), )

	#no_celex from index file must be unique
	def clean(self, *args, **kwargs):
		#~ super(ActIds, self).clean(*args, **kwargs)
		print "clean"
		if self.src=="index":
			no_celex=self.no_celex
			try:
				act_ids=ActIds.objects.get(no_celex=no_celex, src="index")
				print "clean ActIds: act_ids pk:", act_ids.pk
				#if another act has the same no_celex already
				if act_ids!=self:
					#if it exists already, raise error
					raise ValidationError('%s NoCelex must be unique')
			except Exception, e:
				print "the no_celex does not exist in the db yet", e

		return self


class ActsIdsModel(models.Model):
	"""
	MODEL
	ActsIds model (ids of the acts only)
	for each id, 5 sources: csv file, prelex dosId file, eurlex, oeil, prelex
	"""
	#INDEX FILE ("classeur")
	releveAnnee = models.IntegerField(max_length=4, blank=False, null=False)
	releveMois=models.IntegerField(max_length=2, blank=False, null=False)
	noOrdre=models.IntegerField(max_length=2, blank=False, null=False)
	titreRMC=models.CharField(max_length=2000, blank=False, null=False)
	adopCSRegleVote=models.CharField(max_length=2, blank=True, null=True)
	adopCSAbs=models.CharField(max_length=90, blank=True, null=True)
	adoptCSContre=models.CharField(max_length=90, blank=True, null=True)
	proposSplittee=models.BooleanField(default=False)
	suite2eLecturePE=models.BooleanField(default=False)
	councilPath=models.CharField(max_length=200, blank=True, null=True, default=None)
	fileNoCelex = models.CharField(max_length=15, unique=True, blank=False, null=False)
	fileNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	fileNoUniqueType = models.CharField(max_length=4, blank=True, null=True, default=None)
	fileNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	fileProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	fileProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	fileProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	fileDosId = models.IntegerField(max_length=7, blank=True, null=True, default=None)

	#EURLEX
	fileEurlexUrlExists=models.BooleanField(default=True)
	eurlexNoCelex = models.CharField(max_length=15, blank=True, null=True, default=None)
	eurlexNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	eurlexNoUniqueType = models.CharField(max_length=4, blank=True, null=True, default=None)
	eurlexNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	eurlexProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	eurlexProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	eurlexProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	eurlexDosId = models.IntegerField(max_length=7, blank=True, null=True, default=None)

	#OEIL
	fileOeilUrlExists=models.BooleanField(default=True)
	oeilNoCelex = models.CharField(max_length=15, blank=True, null=True, default=None)
	oeilNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	oeilNoUniqueType = models.CharField(max_length=4, blank=True, null=True, default=None)
	oeilNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	oeilProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	oeilProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	oeilDosId = models.IntegerField(max_length=7, blank=True, null=True, default=None)

	#PRELEX
	filePrelexUrlExists=models.BooleanField(default=True)
	filePrelexUrl=models.CharField(max_length=200,  blank=True, null=True, default=None)
	prelexNosCelex = models.CharField(max_length=200, blank=True, null=True, default=None)
	prelexNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	prelexNoUniqueType = models.CharField(max_length=4,  blank=True, null=True, default=None)
	prelexNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	prelexProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	prelexProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	prelexProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	prelexDosId = models.IntegerField(max_length=7, blank=True, null=True, default=None)

	#INDEX FILE ("classeur")
	notes=models.CharField(max_length=2000,  blank=True, null=True)

	#GENERAL (just for the program)
	validated=models.BooleanField(default=False)
