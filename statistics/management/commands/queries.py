#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand


#import specific queries
from query import acts, adopt_cs, duree, ep_amdt_vote, min_attend, modif_propos, nb_mots, no_unique_type, party_family, pers, point_b, type_acte, vote


class Command(NoArgsCommand):
    def handle(self, **options):
        #proportion d’actes avec plusieurs codes sectoriels
        #~ q1()
        #ventilation par domaines
        #~ q2()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage sur la periode 1996-2012
        #~ q3()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage sur la periode 1996-2012
        #~ q4()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q7()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q8()


        #PAR ANNEE

        #production législative
        #~ q9()
        #ventilation par domaines
        #~ q10()
        #pourcentage de propositions modifiées par la Commission
        #~ q11()
        #~ #durée moyenne d’adoption
        #~ q12()
        #pourcentage d’actes adoptés en 1e et 2e lecture
        #~ q13()
        #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q14()
        #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q15()
        #nombre moyen d’amendements déposés/adoptés
        #~ q16()
        #vote?
        #~ q17()
        #pourcentage AdoptCSContre=Y
        #~ q18("adopt_cs_contre")
        #~ #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM
        #~ q19()
        #Durée moyenne des actes soumis à un vote
        #~ q20()
        #Nombre d’actes pour lesquels on a eu au moins une discussion en points B
        #~ q21()
        #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee
        #~ q22()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage par année
        #~ q23()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage par année
        #~ q24()


        #PAR SECTEUR ET PAR ANNEE

        #% age de propositions modifiées par la Commission
        #~ q27()
        #~ #durée moyenne d’adoption
        #~ q28()
        #~ #% age d’actes adoptés en 1e et 2e lecture
        #~ q29()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q30()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q31()
        #~ #nombre moyen d’amendements déposés/adoptés
        #~ q32("EPComAmdtTabled", "com_amdt_tabled")
        #~ q32("EPComAmdtAdopt", "com_amdt_adopt")
        #~ q32("EPAmdtTabled", "amdt_tabled")
        #~ q32("EPAmdtAdopt", "amdt_adopt")
        #Vote?
        #~ q33()
        #%age de votes négatifs par Etat membre
        #~ q34()
        #% age de votes négatifs isolés, de 2 Etats, de 3 Etats
        #~ q35(1)
        #~ q35(2)
        #~ q35(3)
        #Durée moyenne des actes soumis à un vote
        #~ q36()
        #~ #Pourcentage d’actes pour lesquels on a eu au moins une discussion en points B
        #~ q37()
        #~ #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee ET par secteurs
        #~ q38()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage par année et par secteur
        #~ q39()
        #~ #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage par année et par secteur
        #~ q40()
        #~ 
        
        #période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux
        #~ q43()
        
        #~ #pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q44()
        #pourcentage 1/2/3 EM (parmi les actes AdoptCSContre=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q45(1)
        #~ q45(2)
        #~ q45(3)
        #pourcentage AdoptCSAbs=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q46()
        #~ #pourcentage 1/2/3 EM (parmi les actes AdoptCSAbs=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q47(1)
        #~ q47(2)
        #~ q47(3)
        
        #DureeTotaleDepuisTransCons moyenne pour actes avec au moins une discussion en point B par année
        #~ q48()
        #DureeTotaleDepuisTransCons moyenne pour actes avec au moins une discussion en point B par secteur
        #~ q49()
        #~ #DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par secteur et par année
        #~ q50()
       #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U par année  
        #~ q51("U")
        #~ q51("V")
        #~ #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U par secteur
        #~ q52("U")
        #~ q52("V")
        #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U, par secteur et par année
        #~ q53("U")
        #~ q53("V")
        
        #Nombre de mots moyen des textes des actes, par année
        #~ q54()
        #~ #Nombre de mots moyen des textes des actes, par secteur
        #~ q55()
        #~ #Nombre de mots moyen des textes des actes, par secteur et par année
        #~ q56()
        
        #pourcentage d'actes avec plusieurs bases juridiques dans la production législative, par année
        #~ q57()
        #~ q57("13", "Marché intérieur")
        #DureeTotaleDepuisPropCom moyenne des actes pour lesquels il y a concordance des PartyFamilyResp et GroupePolitiqueRapporteur ("Social Democracy")
        #~ q58()
        #impact du nombre de bases juridiques sur la durée de la procédure
        #~ q59("13", "Marché intérieur")
        #~ #impact du nombre de bases juridiques sur la nombre de points b
        #~ q60()
        #Nombre d'actes avec un vote public
        #~ q61()
        #~ #Pourcentages d'actes adoptés en 1ère lecture en fonction du nombre de base juridiques et du code sectoriel
        #~ q62("13", "Marché intérieur")
        
        #Nombre de mots moyen suivant le type de l'acte, par année
        #~ q63()
        #~ q63_bis()
        #~ #Nombre de mots moyen suivant le NoUniqueType, par année
        #~ q64()
        #~ q64_bis()
       
        #Nombre de points B par année
        #~ q65()
        #Nombre de points B par secteur
        #~ q66()
        #Nombre de points B par année et par secteur
        #~ q67()
        #~ #Nombre de points B pour les actes avec un vote public, par année
        #~ q68()
        #~ #Nombre de points B pour les actes avec un vote public, par secteur
        #~ q69()
        #~ #Nombre de points B pour les actes avec un vote public, par année et par secteur
        #~ q70()
        
        #pourcentages d propositions de la Commission adoptées par procédure écrite
        #~ q71()
        #pourcentage de textes adoptés en « points A » au Conseil
        #~ q72()
        #nombre de moyen de points B par texte
        #~ q73()
        #~ #pourcentage de textes adoptés en 1ère lecture au Parlement Européen
        #~ q74()
        #nombre moyen d’amendements déposés
        #~ q75()
        #% moyen de représentants permanents par acte
        #~ q76()
        #~ 
        #~ #% ages moyens de votes publics, vote contre, abstentions là où VMQ est possible
        #~ q77()
        #~ #durée moyenne par acte
        #~ q78()
        #~ #% d’actes adoptés en 2ème lecture
        #~ q79()
        #% d’actes avec au moins 1 point B
        #~ q80()
        #~ #% d’actes adoptés avec opposition de 2 ou 3 Etats ou plus par rapport au nombre total d’actes où VMQ aurait été possible
        #~ q81()

        #Liste des actes avec leur titre pour la période 1996-2012 lorsque l’un des 4 codes sectoriels comprend le code suivant
        #~ q82()
        #~ #Nb de mots x Nb d’actes par année, pour les secteurs
        #~ q83()
        #~ 
        #Pourcentage de textes lorsque PartyFamilyRapporteurPE1 DIFFERENTE de PartyFamilyRespPropos1
        #~ q84_cs()
        #~ q84_year()
        #~ q84_cs_year()

        #Nombre de CS DVE+DVE, pour certains secteurs, par année
        #~ q85()
#~ 
        #~ #Nombre de CS REG+REG, pour certains secteurs, par année
        #~ q86()
#~ 
        #~ #Nombre de CS DEC+DEC+CS DEC W/O ADD, pour certains secteurs, par année
        #~ q87()

        #1/pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=V) 2/pourcentage AdoptCSAbs=Y (parmi les actes AdoptCSRegleVote=U), par secteur, par annee, par secteur et par annee
        #~ q88()
#~ 
        #~ #Nombre de textes x Nombre de mots Pour l’année 2009 uniquement par mois
        #~ q90_mois()
        #~ q90_mois_nut()

        #Liste des RespPropos
        #~ q91()
        #Liste des Rapporteurs
        #~ q92()

        #Pourcentage des familles politiques des RespPropos
        #~ q93()
        #~ #Pourcentage des familles politiques des Rapporteurs
        #~ q94()


		#2014-10-31

		
        #Pourcentage de points B, par année, par secteur, par année et par secteur
        point_b.q95()
        #~ 
        #~ #Durée DureeTotaleDepuisTransCons moyenne 1/pour tous les actes, 2/quand VotePublic=Y ou 3/quand VotePublic= N, par année, par secteur, par année et par secteur
        duree.q96()
        #~ 
        #~ #1/Pourcentage de AdoptCSContre=Y, 2/Pourcentage de AdoptCSAbs=Y, par année, par secteur, par année et par secteur
        adopt_cs.q97()
        #~ 
        #~ #Pourcentage d’actes adoptés avec NoUniqueType=COD 1/et NbLectures=1, 2/et NbLectures=2, par année, par secteur, par année et par secteur
        no_unique_type.q98()
        #~ 
        #~ #1/Nombre d’EPComAmdtAdopt, 2/Nombre d’EPComAmdtTabled, 3/Nombre d’EPAmdtAdopt, 4/Nombre d’EPAmdtTabled, par année, par secteur, par année et par secteur
        ep_amdt_vote.q99()
        #~ 
        #1/Moyenne EPVotesFor1, 2/Moyenne EPVotesFor2, 3/Moyenne EPVotesAgst1, 4/Moyenne EPVotesAgst2, 5/MoyenneEPVotesAbs1, 6/MoyenneEPVotesAbs2, par année, par secteur, par année et par secteur
        ep_amdt_vote.q100()
