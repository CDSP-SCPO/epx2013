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

	releveAnnee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
	releveMois=models.IntegerField(max_length=2, blank=True, null=True, default=None)
	releveMoisInitial=models.CharField(max_length=2, blank=True, null=True, default=None)
	noOrdre=models.IntegerField(max_length=3, blank=True, null=True, default=None)

	#fields to retrieve for the statistical analysis

	#eurlex
	eurlexTitreEn=models.CharField(max_length=500, blank=True, null=True, default=None)
	eurlexCodeSectRep01=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda01=models.IntegerField(max_length=8, blank=True, null=True, default=None)
	eurlexCodeSectRep02=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda02=models.IntegerField(max_length=8, blank=True, null=True, default=None)
	eurlexCodeSectRep03=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda03=models.IntegerField(max_length=8, blank=True, null=True, default=None)
	eurlexCodeSectRep04=models.CharField(max_length=11, blank=True, null=True, default=None)
	eurlexCodeAgenda04=models.IntegerField(max_length=8, blank=True, null=True, default=None)
	eurlexRepEn1=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepAgenda01=models.TextField(max_length=10000, blank=True, null=True, default=None)
	eurlexRepEn2=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepAgenda02=models.TextField(max_length=10000, blank=True, null=True, default=None)
	eurlexRepEn3=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepAgenda03=models.TextField(max_length=10000, blank=True, null=True, default=None)
	eurlexRepEn4=models.CharField(max_length=200, blank=True, null=True, default=None)
	eurlexRepAgenda04=models.TextField(max_length=10000, blank=True, null=True, default=None)
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
	prelexRespPropos1=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexNationResp1=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexNationalPartyResp1=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexEUGroupResp1=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexRespPropos2=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexNationResp2=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexNationalPartyResp2=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexEUGroupResp2=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexRespPropos3=models.CharField(max_length=100, blank=True, null=True, default=None)
	prelexNationResp3=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexNationalPartyResp3=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexEUGroupResp3=models.CharField(max_length=50, blank=True, null=True, default=None)
	prelexTransmissionCouncil=models.DateField(max_length=10, blank=True, null=True, default=None)
	prelexConsB=models.CharField(max_length=500, blank=True, null=True, default=None)
	prelexNbPointB=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	prelexAdoptionConseil=models.DateField(max_length=10, blank=True, null=True, default=None)
	prelexNbPointA=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	prelexCouncilA=models.CharField(max_length=200, blank=True, null=True, default=None)

	prelexRejetConseil=models.BooleanField(default=False)
	prelexConfigCons=models.CharField(max_length=10, blank=True, null=True, default=None)
	prelexChgtBaseJ=models.BooleanField(default=False)
	prelexDureeAdoptionTrans=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeProcedureDepuisPropCom=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeProcedureDepuisTransCons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeTotaleDepuisPropCom=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexDureeTotaleDepuisTransCons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	prelexAdoptCSRegleVote=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexVotePublic=models.BooleanField(default=False)
	prelexAdoptCSContre=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexAdoptCSAbs=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexAdoptPCContre=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexAdoptPCAbs=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexAdoptAPContre=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexAdoptAPAbs=models.CharField(max_length=2, blank=True, null=True, default=None)
	prelexDdeEM=models.BooleanField(default=False)
	prelexProposSplittee_Adoption_Partielle=models.BooleanField(default=False)
	prelexProcedureEcrite=models.BooleanField(default=False)
	prelexSuite2LecturePE=models.BooleanField(default=False)

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
	acronym = models.CharField(max_length=10, unique=True)

	#display in the drop down list (administration form)
	def __unicode__(self):
		return u"%s" % self.acronym


class DGFullNameModel(models.Model):
	"""
	MODEL
	list of dg full names corresponding to the dg codes
	"""
	fullName = models.CharField(max_length=100)
	dgCode=models.ForeignKey('DgCodeModel')
