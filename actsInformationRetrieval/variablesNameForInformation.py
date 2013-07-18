#Acts information validation
#do the match between variables name used in the program (db) and variables name displayed
variablesNameDic={}
#name used by the program -> name displayed (to be translated in English)

#ids
variablesNameDic["releveAnnee"]="ReleveAnnee"
variablesNameDic["releveMois"]="ReleveMois"
variablesNameDic["releveMoisInitial"]="ReleveMoisInitial"
variablesNameDic["noOrdre"]="NoOrdre"

#eurlex
variablesNameDic["eurlexTitreEn"]="TitreEn"
variablesNameDic["eurlexCodeSectRep01"]="CodeSectRep01"
variablesNameDic["eurlexCodeAgenda01"]="CodeAgenda01"
variablesNameDic["eurlexCodeSectRep02"]="CodeSectRep02"
variablesNameDic["eurlexCodeAgenda02"]="CodeAgenda02"
variablesNameDic["eurlexCodeSectRep03"]="CodeSectRep03"
variablesNameDic["eurlexCodeAgenda03"]="CodeAgenda03"
variablesNameDic["eurlexCodeSectRep04"]="CodeSectRep04"
variablesNameDic["eurlexCodeAgenda04"]="CodeAgenda04"
variablesNameDic["eurlexRepEn1"]="RepEn1"
variablesNameDic["eurlexRepEn2"]="RepEn2"
variablesNameDic["eurlexRepEn3"]="RepEn3"
variablesNameDic["eurlexRepEn4"]="RepEn4"

variablesNameDic["eurlexTypeActe"]="TypeActe"
variablesNameDic["eurlexBaseJuridique"]="BaseJuridique"

#oeil
variablesNameDic["oeilCommissionPE"]="CommissionPE"
variablesNameDic["oeilEPComAndtTabled"]="EPComAndtTabled"
variablesNameDic["oeilEPComAndtAdopt"]="EPComAndtAdopt"
variablesNameDic["oeilEPAmdtTabled"]="EPAmdtTabled"
variablesNameDic["oeilEPAmdtAdopt"]="EPAmdtAdopt"
variablesNameDic["oeilEPVotesFor1"]="EPVotesFor1"
variablesNameDic["oeilEPVotesAgst1"]="EPVotesAgst1"
variablesNameDic["oeilEPVotesAbs1"]="EPVotesAbs1"
variablesNameDic["oeilEPVotesFor2"]="EPVotesFor2"
variablesNameDic["oeilEPVotesAgst2"]="EPVotesAgst2"
variablesNameDic["oeilEPVotesAbs2"]="EPVotesAbs2"
variablesNameDic["oeilGroupePolitiqueRapporteur1"]="GroupePolitiqueRapporteur1"
variablesNameDic["oeilRapporteurPE1"]="RapporteurPE1"
variablesNameDic["oeilEtatMbRapport1"]="EtatMbRapport1"
variablesNameDic["oeilGroupePolitiqueRapporteur2"]="GroupePolitiqueRapporteur2"
variablesNameDic["oeilRapporteurPE2"]="RapporteurPE2"
variablesNameDic["oeilEtatMbRapport2"]="EtatMbRapport2"
variablesNameDic["oeilGroupePolitiqueRapporteur3"]="GroupePolitiqueRapporteur3"
variablesNameDic["oeilRapporteurPE3"]="RapporteurPE3"
variablesNameDic["oeilEtatMbRapport3"]="EtatMbRapport3"
variablesNameDic["oeilGroupePolitiqueRapporteur4"]="GroupePolitiqueRapporteur4"
variablesNameDic["oeilRapporteurPE4"]="RapporteurPE4"
variablesNameDic["oeilEtatMbRapport4"]="EtatMbRapport4"
variablesNameDic["oeilGroupePolitiqueRapporteur5"]="GroupePolitiqueRapporteur5"
variablesNameDic["oeilRapporteurPE5"]="RapporteurPE5"
variablesNameDic["oeilEtatMbRapport5"]="EtatMbRapport5"
variablesNameDic["oeilModifPropos"]="ModifPropos"
variablesNameDic["oeilNombreLectures"]="NombreLectures"
variablesNameDic["oeilSignPECS"]="SignPECS"

#prelex
variablesNameDic["prelexAdoptionProposOrigine"]="AdoptionProposOrigine"
variablesNameDic["prelexComProc"]="ComProc"
variablesNameDic["prelexDGProposition1"]="DGProposition1"
variablesNameDic["prelexSiglesDG1"]="SiglesDG1"
variablesNameDic["prelexDGProposition2"]="DGProposition2"
variablesNameDic["prelexSiglesDG2"]="SiglesDG2"
variablesNameDic["prelexRespPropos1"]="RespPropos1"
variablesNameDic["prelexNationResp1"]="NationResp1"
variablesNameDic["prelexNationalPartyResp1"]="NationalPartyResp1"
variablesNameDic["prelexEUGroupResp1"]="PartyFamilyResp1"
variablesNameDic["prelexRespPropos2"]="RespPropos2"
variablesNameDic["prelexNationResp2"]="NationResp2"
variablesNameDic["prelexNationalPartyResp2"]="NationalPartyResp2"
variablesNameDic["prelexEUGroupResp2"]="PartyFamilyResp2"
variablesNameDic["prelexRespPropos3"]="RespPropos3"
variablesNameDic["prelexNationResp3"]="NationResp3"
variablesNameDic["prelexNationalPartyResp3"]="NationalPartyResp3"
variablesNameDic["prelexEUGroupResp3"]="PartyFamilyResp3"
variablesNameDic["prelexTransmissionCouncil"]="TransmissionCouncil"
variablesNameDic["prelexConsB"]="ConsB"
variablesNameDic["prelexNbPointB"]="NbPointB"
variablesNameDic["prelexAdoptionConseil"]="AdoptionConseil"
variablesNameDic["prelexNbPointA"]="NbPointA"
variablesNameDic["prelexCouncilA"]="CouncilA"

variablesNameDic["prelexRejetConseil"]="RejetConseil"
variablesNameDic["prelexConfigCons"]="ConfigCons"
variablesNameDic["prelexChgtBaseJ"]="ChgtBaseJ"
variablesNameDic["prelexDureeAdoptionTrans"]="DureeAdoptionTrans"
variablesNameDic["prelexDureeProcedureDepuisPropCom"]="DureeProcedureDepuisPropCom"
variablesNameDic["prelexDureeProcedureDepuisTransCons"]="DureeProcedureDepuisTransCons"
variablesNameDic["prelexDureeTotaleDepuisPropCom"]="DureeTotaleDepuisPropCom"
variablesNameDic["prelexDureeTotaleDepuisTransCons"]="DureeTotaleDepuisTransCons"
variablesNameDic["prelexAdoptCSRegleVote"]="AdoptCSRegleVote"
variablesNameDic["prelexVotePublic"]="VotePublic"
variablesNameDic["prelexAdoptCSContre"]="AdoptCSContre"
variablesNameDic["prelexAdoptCSAbs"]="AdoptCSAbs"
variablesNameDic["prelexAdoptPCContre"]="AdoptPCContre"
variablesNameDic["prelexAdoptPCAbs"]="AdoptPCAbs"
variablesNameDic["prelexAdoptAPContre"]="AdoptAPContre"
variablesNameDic["prelexAdoptAPAbs"]="AdoptAPAbs"
variablesNameDic["prelexDdeEM"]="DdeEM"
variablesNameDic["prelexProposSplittee_Adoption_Partielle"]="ProposSplittee_Adoption_Partielle"
variablesNameDic["prelexProcedureEcrite"]="ProcedureEcrite"
variablesNameDic["prelexSuite2LecturePE"]="Suite2LecturePE"
