from django.db import models


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
	titreRMC=models.CharField(max_length=1000, blank=False, null=False)
	adopCSRegleVote=models.CharField(max_length=2, blank=True, null=True)
	adopCSAbs=models.CharField(max_length=20, blank=True, null=True)
	adoptCSContre=models.CharField(max_length=20, blank=True, null=True)
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
	fileDosId = models.IntegerField(max_length=7, unique=True, blank=True, null=True, default=None)

	#EURLEX
	fileEurlexUrlExists=models.BooleanField(default=True)
	eurlexNoCelex = models.CharField(max_length=15, blank=True, null=True, default=None)
	eurlexNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	eurlexNoUniqueType = models.CharField(max_length=4, blank=True, null=True, default=None)
	eurlexNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	eurlexProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	eurlexProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	eurlexProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	eurlexDosId = models.IntegerField(max_length=7, unique=True, blank=True, null=True, default=None)
	
	#OEIL
	fileOeilUrlExists=models.BooleanField(default=True)
	oeilNoCelex = models.CharField(max_length=15, blank=True, null=True, default=None)
	oeilNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	oeilNoUniqueType = models.CharField(max_length=4, blank=True, null=True, default=None)
	oeilNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	oeilProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	oeilProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	oeilDosId = models.IntegerField(max_length=7, unique=True, blank=True, null=True, default=None)
	
	#PRELEX
	filePrelexUrlExists=models.BooleanField(default=True)
	prelexUrl=models.CharField(max_length=200,  blank=True, null=True, default=None)
	prelexNosCelex = models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexNoUniqueAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	prelexNoUniqueType = models.CharField(max_length=4,  blank=True, null=True, default=None)
	prelexNoUniqueChrono = models.CharField(max_length=5, blank=True, null=True, default=None)
	prelexProposAnnee = models.IntegerField(max_length=4, blank=True, null=True, default=None)
	prelexProposChrono = models.CharField(max_length=7, blank=True, null=True, default=None)
	prelexProposOrigine = models.CharField(max_length=4,  blank=True, null=True, default=None)
	prelexDosId = models.IntegerField(max_length=7, unique=True, blank=True, null=True, default=None)

	#INDEX FILE ("classeur")
	notes=models.CharField(max_length=2000,  blank=True, null=True)
	
	#GENERAL (just for the program)
	validated=models.BooleanField(default=False)

	
	class Meta:
		unique_together = (("releveAnnee", "releveMois", "noOrdre"), ("fileNoUniqueType", "fileNoUniqueAnnee", "fileNoUniqueChrono"), )
	
	def __unicode__(self):
		#display of the drop down list in the act validation form
		return u"releveAnne=%s, releveMois=%s, noOrdre=%s" % (self.releveAnnee, self.releveMois, self.noOrdre)
		#~ return "releveAnne="+str(self.releveAnnee)+", releveMois="+str(self.releveMois)+", noOrdre="+str(self.noOrdre)
