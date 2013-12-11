"""
eurlex, oeil or prelex data retrieval: db access and modif
"""
from act_ids.models import ActIds
from act.models import CodeSect, Country, Person
from functions import list_reverse_enum

def get_act_ids(act):
	"""
	FUNCTION
	ge the act ids for each source ("index", "eurlex", "oeil" and "prelex") given the act in paramater
	PARAMETERS
	act: instance of the act [Act model instance]
	RETURN
	act_ids: dictionary of act ids for each source [dictionary of ActIds instances]
	"""
	act_ids={}
	#get the ids for each source
	act_ids_instances=ActIds.objects.filter(act=act)
	for act_ids_instance in act_ids_instances:
		act_ids[act_ids_instance.src]=act_ids_instance
	return act_ids


def save_fk_code_sect(instance, field):
	"""
	FUNCTION
	link the foreign key code_agenda/config_cons with code_sect (add/modif of an act)
	PARAMETERS
	instance: object to update (code_agenda/config_cons) [CodeSect model instance]
	field: field to update "code_agenda" or "config_cons" [string]
	RETURN
	None
	"""
	#if there is no value for the foreign key field, try to get a value
	if instance!=None and getattr(instance, field)==None:
		for index, item in list_reverse_enum(instance.code_sect):
			if item==".":
				code_sect_temp=instance.code_sect[:index]
				try:
					#get the new instance corresponding to the new code_sect
					new_instance=CodeSect.objects.get(code_sect=code_sect_temp)
					#if it has a code_agenda, save it to the object to update and exit
					if getattr(new_instance, field)!=None:
						setattr(instance, field, getattr(new_instance, field))
						instance.save()
						break
				except Exception, e:
					print "exception", e


def save_get_object(model, fields):
	"""
	FUNCTION
	save and get an instance object (add/modif/import of an act):
	PARAMETERS
	model: model of the field [model object]
	fields: maps names and values of each field [dictionary]
	RETURN
	instance: instance of the field variable [model instance]
	"""
	try:
		#get the object from the db if it already exists
		instance=model.objects.get(**fields)
	except:
		#~ print "does not exist in the db yet"
		#save the field in the database
		instance=model.objects.create(**fields)

	#return object
	return instance


def save_get_field_and_fk(field, fields_fk, src=""):
	"""
	FUNCTION
	save a field and its foreign keys in its table (add/modif/import of an act)
	PARAMETERS
	field: model name, field name and field value [list]
	[Person, "name", <value>]
	[Party, "party", <value>]
	[CodeSect, "code_sect", <value>]
	[DG, "dg", <value>]
	fields_fk: for each foreign key, model name, field name and field value [list of lists]
	[[Country, "country", <value>], [Party, "party", <value>]]
	[[PartyFamily, "party_family", <value>]]
	[[CodeAgenda, "code_agenda", <value>]]
	[[ConfigCons, "config_cons", <value>]]
	[[DGSigle, "dg_sigle", <value>]]
	src: "rapp" or "resp" if saving a pers (extra parameter) [string]
	RETURN
	instance: instance of the field with its foreign keys [model instance]
	exist: True if the value of the field or all its foreignkeys already exist, False otherwise [boolean]
	"""
	exist=True
	instance_fks={}
	#save and get each foreign key
	for fk in fields_fk:
		#countries -> already saved, fk[1] represents country_code and not country
		if fk[1]=="country":
			instance_fks[fk[1]]=Country.objects.get(country_code=fk[2])
		else:
			instance_fks[fk[1]]=save_get_object(fk[0], {fk[1]: fk[2]})

	try:
		#does the field already exist?
		instance=field[0].objects.get(**{field[1]: field[2]})
		#if yes does any of its foreign key is empty?
		for fk in fields_fk:
			if getattr(instance, fk[1])==None:
				exist=False
				break
	except Exception, e:
		print "save_get_field_and_fk exception", e
		instance=field[0](**{field[1]: field[2]})
		exist=False

	#if the field or one of its foreign key does not exist:
	if not exist:
		#for each foreign key
		for fk in fields_fk:
			setattr(instance, fk[1], instance_fks[fk[1]])

		#Person to be saved
		if src!="":
			instance.src=src

		#save the instance
		instance.save()

	return instance, exist


def save_get_resp_prelex(names):
	"""
	FUNCTION
	save a resp from prelex and get its instance
	PARAMETERS
	names: first name(s) and last name(s) of the responsible [string]
	RETURN
	instance: instance of the responsible [Pers model instance]
	"""
	instance=None
	try:
		#get the instance
		instance=Person.objects.get(src="resp", name=names)
		#check that there are the associated data
		print instance.country.country
	except:
		#there is an error on prelex
		#problem of case?
		names=[name.strip().upper() for name in names.split()]
		persons=Person.objects.filter(src="resp")
		for person in persons:
			person_name=person.name.upper()
			found=True
			for name in names:
				if name not in person_name:
					found=False
					break
				#~ else:
					#~ print "person_name", person_name
					#~ print "name", name
			#if a match is found, stop the program and return the instance
			if found==True and person.country!=None:
				instance=person
				break

	return instance
