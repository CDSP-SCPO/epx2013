from django.db import models
#min and max values for integer fields
from django.core.validators import MinValueValidator, MaxValueValidator
import var_name_data


class Country(models.Model):
	"""
	MODEL
	instances of country (country code) variables
	"""
	country_code=models.CharField(max_length=2, primary_key=True)
	country=models.CharField(max_length=20, unique=True)


class Party(models.Model):
	"""
	MODEL
	instances of party variables
	"""
	party=models.CharField(max_length=70, unique=True)
	#if party_family None: party comes from rapp (oeil); otherwise comes from resp (prelex) or gvt_compo
	#~ country=models.ManyToManyField(Country, through='PartyFamily')


class PartyFamily(models.Model):
	"""
	MODEL
	instances of party_family determined by a party and a country (association model)
	"""
	party = models.ForeignKey(Party)
	country = models.ForeignKey(Country)
	party_family = models.CharField(max_length=50)

	class Meta:
		unique_together=(("party", "country"), )


class Person(models.Model):
	"""
	MODEL
	instances of person (rapporteurs from oeil or responsibles from prelex) variables
	"""
	#src="rapp" or "resp"
	src=models.CharField(max_length=4, db_index=True)
	name=models.CharField(max_length=50, unique=True)
	country=models.ForeignKey(Country, blank=True, null=True, default=None)
	party=models.ForeignKey(Party, blank=True, null=True, default=None)

	def __unicode__(self):
		return u"%s" % self.name


class GvtCompo(models.Model):
	"""
	MODEL
	instances of gvt_compo variables
	"""
	start_date=models.DateField(max_length=10, blank=False, null=False)
	end_date=models.DateField(max_length=10, blank=False, null=False)
	country=models.ForeignKey(Country, blank=False, null=False)
	party=models.ManyToManyField(Party)

	class Meta:
		unique_together=(("start_date", "end_date"), )


class DGSigle(models.Model):
	"""
	MODEL
	instances of dg_sigle variables
	"""
	dg_sigle=models.CharField(max_length=10, unique=True)


class DGNb(models.Model):
	"""
	MODEL
	instances of dg_nb variables
	"""
	dg_nb=models.CharField(max_length=4, unique=True)


class DG(models.Model):
	"""
	MODEL
	instances of dg variables
	"""
	dg=models.CharField(max_length=100, unique=True)
	dg_sigle=models.ForeignKey(DGSigle)
	#link between DG with nb and real name
	dg_nb=models.ManyToManyField(DGNb)

	def __unicode__(self):
		#display of the drop down list in the act data form
		return self.dg


class ConfigCons(models.Model):
	"""
	MODEL
	instances of config_cons variables
	"""
	config_cons=models.CharField(max_length=20, unique=True)


class CodeAgenda(models.Model):
	"""
	MODEL
	instances of code_agenda variables
	"""
	code_agenda=models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(9999)], unique=True)


class CodeSect(models.Model):
	"""
	MODEL
	instances of code_sect variables
	"""
	code_sect=models.CharField(max_length=11, unique=True)
	config_cons=models.ForeignKey(ConfigCons, blank=True, null=True, default=None)
	code_agenda=models.ForeignKey(CodeAgenda, blank=True, null=True, default=None)

	def __unicode__(self):
		#display of the drop down list in the act data form
		return self.code_sect


class Act(models.Model):
	"""
	MODEL
	instances of acts data (index file fields if not ids + data of the acts)
	"""
	#when importing an index file, acts are inserted into the db except if:
	#releve_* have been inserted while importing AdoptPC* file

	#GENERAL (index file)
	releve_annee=models.IntegerField(max_length=4, blank=False, null=False)
	releve_mois=models.IntegerField(max_length=2, blank=False, null=False)
	releve_mois_init=models.CharField(max_length=2, blank=True, null=True, default=None)
	no_ordre=models.IntegerField(max_length=2, blank=False, null=False)
	titre_rmc=models.CharField(max_length=2000, blank=False, null=False)
	council_path=models.CharField(max_length=200, blank=True, null=True, default=None)

	#EURLEX
	titre_en=models.CharField(max_length=500, blank=True, null=True, default=None)
	code_sect_1=models.ForeignKey(CodeSect, related_name='code_sect_1', blank=True, null=True, default=None)
	code_sect_2=models.ForeignKey(CodeSect, related_name='code_sect_2', blank=True, null=True, default=None)
	code_sect_3=models.ForeignKey(CodeSect, related_name='code_sect_3', blank=True, null=True, default=None)
	code_sect_4=models.ForeignKey(CodeSect, related_name='code_sect_4', blank=True, null=True, default=None)
	rep_en_1=models.CharField(max_length=200, blank=True, null=True, default=None)
	rep_en_2=models.CharField(max_length=200, blank=True, null=True, default=None)
	rep_en_3=models.CharField(max_length=200, blank=True, null=True, default=None)
	rep_en_4=models.CharField(max_length=200, blank=True, null=True, default=None)
	type_acte=models.CharField(max_length=100, blank=True, null=True, default=None)
	base_j=models.CharField(max_length=300, blank=True, null=True, default=None)

	#OEIL
	commission=models.CharField(max_length=10, blank=True, null=True, default=None)
	com_amdt_tabled=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	com_amdt_adopt=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	amdt_tabled=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	amdt_adopt=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_for_1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_agst_1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_abs_1=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_for_2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_agst_2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	votes_abs_2=models.IntegerField(max_length=3, blank=True, null=True, default=None)
	rapp_1=models.ForeignKey(Person, related_name='rapp_1', blank=True, null=True, default=None)
	rapp_2=models.ForeignKey(Person, related_name='rapp_2', blank=True, null=True, default=None)
	rapp_3=models.ForeignKey(Person, related_name='rapp_3', blank=True, null=True, default=None)
	rapp_4=models.ForeignKey(Person, related_name='rapp_4', blank=True, null=True, default=None)
	rapp_5=models.ForeignKey(Person, related_name='rapp_5', blank=True, null=True, default=None)
	modif_propos=models.BooleanField(default=False)
	nb_lectures=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	sign_pecs=models.DateField(max_length=10, blank=True, null=True, default=None)

	#PRELEX
	url_prelex=models.CharField(max_length=200, blank=True, null=True, default=None)
	#data
	adopt_propos_origine=models.DateField(max_length=10, blank=True, null=True, default=None)
	com_proc=models.CharField(max_length=100, blank=True, null=True, default=None)
	dg_1=models.ForeignKey(DG, related_name='dg_1', blank=True, null=True, default=None)
	dg_2=models.ForeignKey(DG, related_name='dg_2', blank=True, null=True, default=None)
	resp_1=models.ForeignKey(Person, related_name='resp_1', blank=True, null=True, default=None)
	resp_2=models.ForeignKey(Person, related_name='resp_2', blank=True, null=True, default=None)
	resp_3=models.ForeignKey(Person, related_name='resp_3', blank=True, null=True, default=None)
	transm_council=models.DateField(max_length=10, blank=True, null=True, default=None)
	cons_b=models.CharField(max_length=500, blank=True, null=True, default=None)
	nb_point_b=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	adopt_conseil=models.DateField(max_length=10, blank=True, null=True, default=None)
	nb_point_a=models.IntegerField(max_length=1, blank=True, null=True, default=None)
	council_a=models.CharField(max_length=200, blank=True, null=True, default=None)

	rejet_conseil=models.BooleanField(default=False)
	chgt_base_j=models.BooleanField(default=False)
	duree_adopt_trans=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	duree_proc_depuis_prop_com=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	duree_proc_depuis_trans_cons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	duree_tot_depuis_prop_com=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	duree_tot_depuis_trans_cons=models.IntegerField(max_length=5, blank=True, null=True, default=None)
	vote_public=models.BooleanField(default=False)
	adopt_cs_regle_vote=models.CharField(max_length=2, blank=True, null=True, default=None)
	adopt_cs_contre=models.ManyToManyField(Country, related_name='adopt_cs_contre')
	adopt_cs_abs=models.ManyToManyField(Country, related_name='adopt_cs_abs')
	adopt_pc_contre=models.ManyToManyField(Country, related_name='adopt_pc_contre')
	adopt_pc_abs=models.ManyToManyField(Country, related_name='adopt_pc_abs')
	adopt_ap_contre=models.CharField(max_length=50, blank=True, null=True, default=None)
	adopt_ap_abs=models.CharField(max_length=50, blank=True, null=True, default=None)
	dde_em=models.BooleanField(default=False)
	split_propos=models.BooleanField(default=False)
	proc_ecrite=models.BooleanField(default=False)
	suite_2e_lecture_pe=models.BooleanField(default=False)
	gvt_compo=models.ManyToManyField(GvtCompo)

	#GENERAL
	notes=models.CharField(max_length=2000,  blank=True, null=True, default=None)
	#validated=0 if the act hasn't been validated yet
	#validated=1 if the ids of the act have been validated but not its data
	#validated=2 if the ids AND data of the act have been validated
	validated=models.IntegerField(max_length=1, default=0, db_index=True)

	#joined primary keys
	class Meta:
		unique_together=(("releve_annee", "releve_mois", "no_ordre"), )

	def __unicode__(self):
		#display of the drop down list in the act data form
		releve_annee=var_name_data.var_name['releve_annee'] + "=" + str(self.releve_annee)
		releve_mois=var_name_data.var_name['releve_mois'] + "=" + str(self.releve_mois)
		no_ordre=var_name_data.var_name['no_ordre'] + "=" + str(self.no_ordre)
		#~ return u"releve_annee=%s, releve_mois=%s, no_ordre=%s" % (self.releve_annee, self.releve_mois, self.no_ordre)
		return releve_annee + ", " + releve_mois + ", " + no_ordre


class NP(models.Model):
	"""
	MODEL
	instances of opal variables (NP*)
	"""
	case_nb=models.IntegerField(max_length=10, primary_key=True)
	np=models.ForeignKey(Country, blank=False, null=False)
	act_type=models.CharField(max_length=106, blank=False, null=False)
	act_date=models.DateField(max_length=10, blank=True, null=True, default=None)
	act=models.ForeignKey(Act)
