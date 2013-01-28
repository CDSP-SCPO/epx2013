from django.db import models
from actsIdsValidation.models import ActsIdsModel


class ActsInformationModel(models.Model):
	"""
	MODEL
	Acts information model (fields to retrieve for the statistical analysis)
	for each act, 3 sources: eurlex, oeil, prelex
	"""
	#id of the validated act
	actId = models.OneToOneField(ActsIdsModel, primary_key=True)
	
	#fields to retrieve for the statistical analysis 
	
	#prelex
	adoptionProposOrigine=models.DateField(max_length=10, blank=True, null=True, default=None)
	comProc=models.CharField(max_length=100,  blank=True, null=True, default=None)
	dgProposition=models.CharField(max_length=100,  blank=True, null=True, default=None)
	dgProposition2=models.CharField(max_length=100,  blank=True, null=True, default=None)
	respPropos1=models.CharField(max_length=100, blank=True, null=True, default=None)
	respPropos2=models.CharField(max_length=100, blank=True, null=True, default=None)
	respPropos3=models.CharField(max_length=100, blank=True, null=True, default=None)
	transmissionCouncil=models.DateField(max_length=10, blank=True, null=True, default=None)
	nbPointB=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	consB=models.CharField(max_length=500,  blank=True, null=True, default=None)
	adoptionConseil=models.DateField(max_length=10, blank=True, null=True, default=None)
	nbPointA=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	councilA=models.CharField(max_length=100,  blank=True, null=True, default=None)
	nbLectures=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	
	#GENERAL (just for the program)
	validated=models.BooleanField(default=False)
	
	#display in the drop down list
	def __unicode__(self):
		return u"%s" % self.actId


class DgCodeModel(models.Model):
	"""
	MODEL
	list of dgCodes for the dgProposition field(s)
	"""
	acronym = models.CharField(max_length=10, unique=True)
	
	#display in the drop down list (administration form)
	def __unicode__(self):
		return u"%s" % self.acronym


class DgFullNameModel(models.Model):
	"""
	MODEL
	list of dg full names corresponding to the dg codes
	"""
	fullName = models.CharField(max_length=100)
	dgCode=models.ForeignKey('DgCodeModel')
