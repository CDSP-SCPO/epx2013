from common.config_file import *

#Acts
#do the match between variables name used in the program (db) and variables name displayed
var_name={}
#name used by the program -> name displayed (to be translated in English)

#DO NOT CHANGE THE KEYS (left side)

#council summary (index file)
var_name["act_id"]="id"
var_name["releve_annee"]="ReleveAnnee"
var_name["releve_mois"]="ReleveMois"
var_name["releve_mois_init"]="ReleveMoisInitial"
var_name["no_ordre"]="NoOrdre"
var_name["titre_rmc"]="TitreRMC"
var_name["council_path"]="CouncilPath"
var_name["attendance_pdf"]="Attendance pdf"
var_name["notes"]="Notes"

#eurlex
var_name["titre_en"]="TitreEn"
var_name["code_sect"]="CodeSect*"
var_name["code_agenda"]="CodeAgenda*"
var_name["code_agenda_"]="CodeAgenda0"
for index in xrange(1,5):
    num=str(index)
    var_name["code_sect_"+num]="CodeSect0"+num
    var_name["code_agenda_"+num]="CodeAgenda0"+num
    var_name["rep_en_"+num]="RepEn"+num
var_name["type_acte"]="TypeActe"
var_name["base_j"]="BaseJuridique"
var_name["nb_mots"]="NombreMots"

var_name["adopt_propos_origine"]="AdoptionProposOrigine"
var_name["com_proc"]="ComProc"
var_name["dg"]="DGProposition*"
var_name["dg_sigle_"]="SigleDG"
var_name["dg_sigle"]="SigleDG*"
var_name["dg_nb"]="ChiffreDG*"
for index in xrange(1, nb_dgs+1):
    num=str(index)
    var_name["dg_"+num]="DGProposition"+num
    var_name["dg_sigle_"+num]="SigleDG"+num
var_name["resp"]="RespPropos*"
var_name["name"]=var_name["resp"]
var_name["resp_country"]="NationResp*"
var_name["resp_country_"]="NationResp"
var_name["resp_party"]="NationalPartyResp*"
var_name["resp_party_"]="NationalPartyResp"
var_name["resp_party_family"]="PartyFamilyResp*"
var_name["resp_party_family_"]="PartyFamilyResp"
for index in xrange(1,4):
    num=str(index)
    var_name["resp_"+num]="RespPropos"+num
    var_name["resp_country_"+num]="NationResp"+num
    var_name["resp_party_"+num]="NationalPartyResp"+num
    var_name["resp_party_family_"+num]="PartyFamilyResp"+num
var_name["transm_council"]="TransmissionCouncil"
var_name["nb_point_b"]="NbPointB"
var_name["date_cons_b"]="DateConsB"
var_name["cons_b"]="ConsB"
var_name["adopt_conseil"]="AdoptionConseil"
var_name["nb_point_a"]="NbPointA"
var_name["date_cons_a"]="DateConsA"
var_name["cons_a"]="CouncilA"

var_name["rejet_conseil"]="RejetConseil"
var_name["config_cons"]="ConfigCons"
var_name["chgt_base_j"]="ChgtBaseJ"
var_name["duree_adopt_trans"]="DureeAdoptionTrans"
names={"proc": "Procedure", "tot": "Totale"}
for name in names:
    var_name["duree_"+name+"_depuis_prop_com"]="Duree"+names[name]+"DepuisPropCom"
    var_name["duree_"+name+"_depuis_trans_cons"]="Duree"+names[name]+"DepuisTransCons"
var_name["adopt_cs_regle_vote"]="AdoptCSRegleVote"
var_name["vote_public"]="VotePublic"
for name in ["cs", "pc", "ap"]:
    var_name["adopt_"+name+"_contre"]="Adopt"+name.upper()+"Contre"
    var_name["adopt_"+name+"_abs"]="Adopt"+name.upper()+"Abs"
var_name["dde_em"]="DdeEM"
var_name["split_propos"]="ProposSplittee"
var_name["proc_ecrite"]="ProcedureEcrite"
var_name["suite_2e_lecture_pe"]="Suite2LecturePE"
var_name["start_date"]="StartDate"
var_name["end_date"]="EndDate"
var_name["gvt_compo"]="NationGvtPoliticalComposition"
var_name["gvt_compo_country"]="NationGvtPoliticalCompositionCountry"
var_name["gvt_compo_party"]="NationGvtPoliticalCompositionParty"
var_name["gvt_compo_party_family"]="NationGvtPoliticalCompositionPartyFamily"
var_name["country"]="Country"
var_name["party"]="Party"
var_name["party_family"]="PartyFamily"

#oeil
var_name["commission"]="CommissionPE"
var_name["com_amdt_tabled"]="EPComAmdtTabled"
var_name["com_amdt_adopt"]="EPComAmdtAdopt"
var_name["amdt_tabled"]="EPAmdtTabled"
var_name["amdt_adopt"]="EPAmdtAdopt"
for index in xrange(1,3):
    num=str(index)
    var_name["votes_for_"+num]="EPVotesFor"+num
    var_name["votes_agst_"+num]="EPVotesAgst"+num
    var_name["votes_abs_"+num]="EPVotesAbs"+num
var_name["rapp"]="Rapporteur*"
var_name["rapp_party"]="GroupePolitiqueRapporteur*"
var_name["rapp_party_"]="GroupePolitiqueRapporteur"
var_name["rapp_country"]="EtatMbRapport*"
var_name["rapp_country_"]="EtatMbRapport"
var_name["rapp_party_family_"]="PartyFamilyRapp"
for index in xrange(1,6):
    num=str(index)
    var_name["rapp_party_"+num]="GroupePolitiqueRapporteur"+num
    var_name["rapp_"+num]="RapporteurPE"+num
    var_name["rapp_country_"+num]="EtatMbRapport"+num
    var_name["rapp_party_family_"+num]="PartyFamilyRapp"+num
var_name["modif_propos"]="ModifPropos"
var_name["nb_lectures"]="NombreLectures"
var_name["sign_pecs"]="SignPECS"


#OPAL
var_name["case_nb"]="NPCaseNumber"
var_name["np"]="NP"
var_name["act_type"]="NPActivityType"
var_name["act_date"]="NPActivityDate"

#MINISTERS' ATTENDANCE
var_name["min_attend"]="MinistersAttendance"
var_name["status"]="Status"
var_name["verbatim"]="Verbatim"
#export file
var_name["country_min_attend"]="MinAttendCountry"
var_name["status_min_attend"]="MinAttendStatus"
var_name["verbatim_min_attend"]="MinAttendVerbatim"

#EPGroupsVotes
var_name["group_votes"]="EPGroupsVotes"
var_name["title"]=var_name["titre_rmc"]
var_name["group_name"]="EPGroup"
var_name["group_vote_adle"]="ALDE/ADLE"
var_name["group_vote_sd"]="S&D"
var_name["group_vote_ppe"]="EPP"
var_name["group_vote_ecr"]="ECR"
var_name["group_vote_efd"]="EFD"
var_name["group_vote_greens"]="GREENS/EFA"
var_name["group_vote_gue"]="GUE-NGL"
var_name["group_vote_ni"]="NI"
var_name["col_for"]="FOR"
var_name["col_against"]="AGAINST"
var_name["col_abstension"]="ABSTENTION"
var_name["col_present"]="PRESENT"
var_name["col_absent"]="ABSENT"
var_name["col_non_voters"]="NON VOTERS"
var_name["col_total_members"]="TOTAL MEMBERS"
var_name["col_cohesion"]="COHESION"
