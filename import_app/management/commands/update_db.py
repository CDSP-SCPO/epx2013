"""
command to import data of the old db into the new db (only act ids)
"""
from django.core.management.base import NoArgsCommand
#new table
from act_ids.models import ActIds
from act.models import Act
#old table
from act_ids.models import ActsIdsModel


def save_adopt_cs_pc(self, instance, field, values):
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
	self.stdout.write(field+": "+ values)
	self.stdout.write('\n')
	values=values.split(',')
	for value in values:
		if value!="":
			field_instance=getattr(instance, field)
			field_instance.add(value.strip())


class Command(NoArgsCommand):
	"""
	MIGRATE ACT IDS FROM OLD DATABASE TO NEW DATABASE
	python manage.py update_db
	"""

	def handle(self, **options):
		acts=ActsIdsModel.objects.all()

		for act in acts:
			try:
				exist=Act.objects.get(releve_annee=act.releveAnnee, releve_mois=act.releveMois, no_ordre=act.noOrdre)
			except Exception, e:
				print "does not exist yet :", e, act.releveAnnee, act.releveMois, act.noOrdre

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

				save_adopt_cs_pc(self, new_act, "adopt_cs_contre", act.adoptCSContre)
				save_adopt_cs_pc(self, new_act, "adopt_cs_abs", act.adopCSAbs)
				self.stdout.write('\n')

				#ids
				for src in ["file", "eurlex", "oeil", "prelex"]:
					act_ids=ActIds()
					act_ids.act=new_act
					if src=="file":
						act_ids.src="index"
					else:
						act_ids.src=src
						act_ids.url_exists=getattr(act, "file"+src[0].upper()+src[1:]+"UrlExists")

					if src=="prelex":
						if act.prelexNosCelex!=None and act.fileNoCelex in act.prelexNosCelex:
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
#~ copy django auth.user table content

#~ delete FROM europolix.act_ids_actids;
#~ delete FROM europolix.act_act_adopt_cs_contre;
#~ delete FROM europolix.act_act_adopt_cs_abs;
#~ delete FROM europolix.act_act;
#~ ALTER TABLE europolix.act_ids_actids AUTO_INCREMENT = 1;
#~ ALTER TABLE europolix.act_act AUTO_INCREMENT = 1;
