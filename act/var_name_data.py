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

#oeil
var_name["commission"]="CommissionPE"
var_name["com_amdt_tabled"]="EPComAndtTabled"
var_name["com_amdt_adopt"]="EPComAndtAdopt"
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
for index in xrange(1,6):
    num=str(index)
    var_name["rapp_party_"+num]="GroupePolitiqueRapporteur"+num
    var_name["rapp_"+num]="RapporteurPE"+num
    var_name["rapp_country_"+num]="EtatMbRapport"+num
var_name["modif_propos"]="ModifPropos"
var_name["nb_lectures"]="NombreLectures"
var_name["sign_pecs"]="SignPECS"

#prelex
var_name["adopt_propos_origine"]="AdoptionProposOrigine"
var_name["com_proc"]="ComProc"
var_name["dg"]="DGProposition*"
var_name["dg_sigle_"]="SiglesDG"
var_name["dg_sigle"]="SiglesDG*"
var_name["dg_nb"]="ChiffresDG*"
for index in xrange(1,3):
    num=str(index)
    var_name["dg_"+num]="DGProposition"+num
    var_name["dg_sigle_"+num]="SiglesDG"+num
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
var_name["cons_b"]="ConsB"
var_name["nb_point_b"]="NbPointB"
var_name["adopt_conseil"]="AdoptionConseil"
var_name["nb_point_a"]="NbPointA"
var_name["council_a"]="CouncilA"

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

#OPAL
var_name["case_nb"]="NPCaseNumber"
var_name["np"]="NP"
var_name["act_type"]="NPActivityType"
var_name["act_date"]="NPActivityDate"

#MINISTERS' ATTENDANCE
var_name["min_attend"]="MinistersAttendance"
var_name["inc"]="Inc"
var_name["ind_status"]="IndStatus"
var_name["verbatim"]="Verbatim"
#export file
var_name["country_min_attend"]="MinAttendCountry"
var_name["ind_status_min_attend"]="MinAttendIndStatus"
var_name["verbatim_min_attend"]="MinAttendVerbatim"
