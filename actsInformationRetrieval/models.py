from django.db import models
from actsIdsValidation.models import ActsIdsModel
#min and max values for integer fields
from django.core.validators import MinValueValidator, MaxValueValidator



class GvtCompoModel(models.Model):
	"""
	MODEL
	list of start and end dates with the nationGvtPoliticalComposition variable
	"""
	startDate=models.DateField(max_length=10, blank=False, null=False)
	endDate=models.DateField(max_length=10, blank=False, null=False)
	nationGvtPoliticalComposition= models.CharField(max_length=1000, blank=False, null=False)


class ActsInformationModel(models.Model):
	"""
	MODEL
	Acts information model (fields to retrieve for the statistical analysis)
	for each act, 3 sources: eurlex, oeil, prelex
	"""
	#id of the validated act
	actId = models.OneToOneField(ActsIdsModel, primary_key=True)

	releveAnnee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
	releveMois=models.IntegerField(max_length=2, blank=True, null=True, default=None)
	releveMoisInitial=models.CharField(max_length=2, blank=True, null=True, default=None)
	noOrdre=models.IntegerField(max_length=3, blank=True, null=True, default=None)

	#fields to retrieve for the statistical analysis

	#eurlex
	eurlexTitreEn=models.CharField(max_length=500, blank=True, null=True, default=None)
	eurlexFullCodeSectRep01=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda01=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], blank=True, null=True, default=None)
	eurlexFullCodeSectRep02=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda02=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], blank=True, null=True, default=None)
	eurlexFullCodeSectRep03=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda03=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], blank=True, null=True, default=None)
	eurlexFullCodeSectRep04=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda04=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], blank=True, null=True, default=None)
	eurlexRepEn1=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepEn2=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepEn3=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepEn4=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexTypeActe=models.CharField(max_length=100, blank=True, null=True, default=None)
	eurlexBaseJuridique=models.CharField(max_length=300, blank=True, null=True, default=None)

	#oeil
	oeilCommissionPE=models.CharField(max_length=10, blank=True, null=True, default=None)
	oeilEPComAndtTabled=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPComAndtAdopt=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPAmdtTabled=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPAmdtAdopt=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesFor1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesAgst1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesAbs1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesFor2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesAgst2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilEPVotesAbs2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	oeilGroupePolitiqueRapporteur1=models.CharField(max_length=100, blank=True, null=True, default=None)
	oeilRapporteurPE1=models.CharField(max_length=50, blank=True, null=True, default=None)
	oeilEtatMbRapport1=models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilGroupePolitiqueRapporteur2=models.CharField(max_length=100, blank=True, null=True, default=None)
	oeilRapporteurPE2=models.CharField(max_length=50, blank=True, null=True, default=None)
	oeilEtatMbRapport2=models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilGroupePolitiqueRapporteur3=models.CharField(max_length=100, blank=True, null=True, default=None)
	oeilRapporteurPE3=models.CharField(max_length=50, blank=True, null=True, default=None)
	oeilEtatMbRapport3=models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilGroupePolitiqueRapporteur4=models.CharField(max_length=100, blank=True, null=True, default=None)
	oeilRapporteurPE4=models.CharField(max_length=50, blank=True, null=True, default=None)
	oeilEtatMbRapport4=models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilGroupePolitiqueRapporteur5=models.CharField(max_length=100, blank=True, null=True, default=None)
	oeilRapporteurPE5=models.CharField(max_length=50, blank=True, null=True, default=None)
	oeilEtatMbRapport5=models.CharField(max_length=5, blank=True, null=True, default=None)
	oeilModifPropos=models.BooleanField(default=False)
	oeilNombreLectures=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	oeilSignPECS=models.DateField(max_length=10, blank=True, null=True, default=None)

	#prelex
	prelexAdoptionProposOrigine=models.DateField(max_length=10, blank=True, null=True, default=None)
	prelexComProc=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexDGProposition1=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexSiglesDG1=models.CharField(max_length=7, blank=True, null=True, default=None)
	prelexDGProposition2=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexSiglesDG2=models.CharField(max_length=7, blank=True, null=True, default=None)
	prelexRespProposId1=models.ForeignKey('RespProposModel', related_name='prelexRespProposId1', blank=True, null=True, default=None)
	#~ prelexNationResp1=models.CharField(max_length=2, blank=True, null=True, default=None)
	#~ prelexNationalPartyResp1=models.CharField(max_length=50, blank=True, null=True, default=None)
	#~ prelexEUGroupResp1=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexRespProposId2=models.ForeignKey('RespProposModel', related_name='prelexRespProposId2', blank=True, null=True, default=None)
	#~ prelexNationResp2=models.CharField(max_length=2, blank=True, null=True, default=None)
	#~ prelexNationalPartyResp2=models.CharField(max_length=50, blank=True, null=True, default=None)
	#~ prelexEUGroupResp2=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexRespProposId3=models.ForeignKey('RespProposModel', related_name='prelexRespProposId3', blank=True, null=True, default=None)
	#~ prelexNationResp3=models.CharField(max_length=2, blank=True, null=True, default=None)
	#~ prelexNationalPartyResp3=models.CharField(max_length=50, blank=True, null=True, default=None)
	#~ prelexEUGroupResp3=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexTransmissionCouncil=models.DateField(max_length=10, blank=True, null=True, default=None)
	prelexConsB=models.CharField(max_length=500, blank=True, null=True, default=None)
	prelexNbPointB=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	prelexAdoptionConseil=models.DateField(max_length=10, blank=True, null=True, default=None)
	prelexNbPointA=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	prelexCouncilA=models.CharField(max_length=200, blank=True, null=True, default=None)

	prelexRejetConseil=models.BooleanField(default=False)
	prelexConfigCons=models.CharField(max_length=20, blank=True, null=True, default=None)
	prelexChgtBaseJ=models.BooleanField(default=False)
	prelexDureeAdoptionTrans=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeProcedureDepuisPropCom=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeProcedureDepuisTransCons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeTotaleDepuisPropCom=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeTotaleDepuisTransCons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexAdoptCSRegleVote=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexVotePublic=models.BooleanField(default=False)
	prelexAdoptCSContre=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexAdoptCSAbs=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexAdoptPCContre=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexAdoptPCAbs=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexAdoptAPContre=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexAdoptAPAbs=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexDdeEM=models.BooleanField(default=False)
	prelexProposSplittee_Adoption_Partielle=models.BooleanField(default=False)
	prelexProcedureEcrite=models.BooleanField(default=False)
	prelexSuite2LecturePE=models.BooleanField(default=False)
	prelexNationGvtPoliticalComposition= models.ManyToManyField(GvtCompoModel)

	#OPAL file
	#there can be many values for each field for one act (for one noCelex)-> concatenation with ";"
	opalNPCaseNumber=models.CharField(max_length=600, blank=True, null=True, default=None)
	opalNP=models.CharField(max_length=120, blank=True, null=True, default=None)
	opalNPActivityType= models.CharField(max_length=200, blank=True, null=True, default=None)
	opalNPActivityDate=models.CharField(max_length=500, blank=True, null=True, default=None)

	#GENERAL (just for the program)
	validated=models.BooleanField(default=False)


	#display in the drop down list
	def __unicode__(self):
		return u"%s" % self.actId


class DGCodeModel(models.Model):
	"""
	MODEL
	list of dgCodes for the dgProposition field(s)
	"""
	dgCode = models.CharField(max_length=10, unique=True)

	#display in the drop down list (administration form)
	def __unicode__(self):
		return u"%s" % self.dgCode


class DGFullNameModel(models.Model):
	"""
	MODEL
	list of dg full names corresponding to the dg codes
	"""
	dgFullName = models.CharField(max_length=100, unique=True)
	dgCode=models.ForeignKey('DgCodeModel')


class ConfigConsModel(models.Model):
	"""
	MODEL
	list of configCons
	"""
	configCons = models.CharField(max_length=20, unique=True)


class CodeAgendaModel(models.Model):
	"""
	MODEL
	list of codeAgenda
	"""
	codeAgenda=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], unique=True)


class CodeSectRepModel(models.Model):
	"""
	MODEL
	list configCons names associated to configCons
	"""
	codeSectRep = models.CharField(max_length=11, unique=True)
	configCons = models.ForeignKey('ConfigConsModel', blank=True, null=True, default=None)
	codeAgenda = models.ForeignKey('CodeAgendaModel', blank=True, null=True, default=None)


class NationRespModel(models.Model):
	"""
	MODEL
	list of nationResp (country code)
	"""
	nationResp=models.CharField(max_length=2, unique=True)


class NationalPartyRespModel(models.Model):
	"""
	MODEL
	list of nationalPartyResp names
	"""
	nationalPartyResp=models.CharField(max_length=50, unique=True)


class EUGroupRespModel(models.Model):
	"""
	MODEL
	list of euGroupResp names
	"""
	euGroupResp=models.CharField(max_length=50, unique=True)


class RespProposModel(models.Model):
	"""
	MODEL
	list of respPropos (full names)
	"""
	respPropos=models.CharField(max_length=50, unique=True)
	nationResp = models.ForeignKey('NationRespModel', blank=True, null=True, default=None)
	nationalPartyResp = models.ForeignKey('NationalPartyRespModel', blank=True, null=True, default=None)
	euGroupResp = models.ForeignKey('EUGroupRespModel', blank=True, null=True, default=None)

	def __unicode__(self):
		return u"%s" % self.respPropos

class AdoptPCModel(models.Model):
	"""
	MODEL
	list of act ids with adoptPCAbs and adoptPCContre variables
	"""
	releveAnnee = models.IntegerField(max_length=4, blank=False, null=False)
	releveMois=models.IntegerField(max_length=2, blank=False, null=False)
	noOrdre=models.IntegerField(max_length=2, blank=False, null=False)
	adoptPCAbs=models.CharField(max_length=50, blank=True, null=True, default=None)
	adoptPCContre=models.CharField(max_length=50, blank=True, null=True, default=None)

	#joined primary keys
	class Meta:
		unique_together = (("releveAnnee", "releveMois", "noOrdre"), )


class NPModel(models.Model):
	"""
	MODEL
	list of act ids with NP and NPActivityType variables
	"""
	npCaseNumber=models.IntegerField(primary_key=True, max_length=10)
	noCelex = models.CharField(max_length=15, blank=False, null=False)
	np=models.CharField(max_length=55, blank=False, null=False)
	npActivityType= models.CharField(max_length=106, blank=False, null=False)
	npActivityDate=models.DateField(max_length=10, blank=True, null=True, default=None)
