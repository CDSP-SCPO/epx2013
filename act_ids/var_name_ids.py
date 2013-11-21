#ActIds
#do the match between variables name used in the program (db) and variables name displayed
var_name={}

#change a value to update the display of a variable name (useful if variables are to be translated in English)
#DO NOT CHANGE THE KEYS (left side)
var_name["url_exists"]="Url exists?"
var_name["no_celex"]="NoCelex"
for name in ["annee", "chrono", "type"]:
	var_name["no_unique_"+name]="NoUnique"+name[0].upper()+name[1:]
for name in ["annee", "chrono", "origine"]:
	var_name["propos_"+name]="Propos"+name[0].upper()+name[1:]
var_name["dos_id"]="DosId"
