"""
import data of the old db into the new db
"""
from act_ids.models import ActIds, DosIdAssoc
from act.models import Act


def save_adopt_cs_pc(instance, field, values):
	"""
	FUNCTION
	save the coutries for adopt_cs_contre, adopt_cs_abs, adopt_pc_contre or adopt_pc_abs
	PARAMETERS
	instance: instance of the act [Act model instance]
	field: name  of the field (adopt_cs_contre, adopt_cs_abs, adopt_pc_contre or adopt_pc_abs) [string]
	values: countries [list of strings]
	RETURN
	None
	"""
	values=values.split(',')
	for value in values:
		if value!="":
			field_instance=getattr(instance, field)
			field_instance.add(value.strip())


acts=ActsIdsModel.objects.using('europolix_old').all()

for act in acts:
	new_act=Act()
	new_act.releve_annee=act.releveAnnee
	new_act.releve_mois=act.releveMois
	new_act.no_ordre=act.noOrdre
	new_act.titre_rmc=act.titreRMC
	new_act.council_path=act.councilPath
	new_act.url_prelex=act.filePrelexUrl
	new_act.adopt_cs_regle_vote=act.adopCSRegleVote
	split_propos=act.proposSplittee
	suite_2e_lecture_pe=act.suite2eLecturePE
	new_act.notes=act.notes
	new_act.validated=act.validated

	#save the act
	new_act.save()

	save_adopt_cs_pc(new_act, "adopt_cs_contre", act.adoptCSContre)
	save_adopt_cs_pc(new_act, "adopt_cs_abs", act.adopCSAbs)

	#ids
	for src in ["file", "eurlex", "oeil", "prelex"]:
		act_ids=ActIds()
		act_ids.act=new_act
		if src=="file":
			act_ids.src="index"
		else:
			act_ids.src=src
			act_ids.url_exists=getattr(act, "file"+src[0].upper()+src[1:]+"UrlExists")

		if src=="prelex" and act.fileNoCelex in act.prelexNosCelex:
			act_ids.no_celex=act.fileNoCelex
		else:
			act_ids.no_celex=getattr(act, src+"NoCelex")

		act_ids.no_unique_annee=getattr(act, src+"NoUniqueAnnee")
		act_ids.no_unique_type=getattr(act, src+"NoUniqueType")
		act_ids.no_unique_chrono=getattr(act, src+"NoUniqueChrono")
		act_ids.propos_annee=getattr(act, src+"ProposAnnee")
		act_ids.propos_chrono=getattr(act, src+"ProposChrono")
		act_ids.propos_origine=getattr(act, src+"ProposOrigine")
		act_ids.dos_id=getattr(act, src+"DosId")

		act_ids.save()

#TODO
copy django auth.user table content
