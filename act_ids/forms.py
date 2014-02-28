from django import forms
from models import ActIds
from act.models import Act
from  import_app.models import ImportDosId
#modif form: add non field error
from django.forms.util import ErrorList
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
#concatain querysets
from itertools import chain


class ActIdsForm(forms.ModelForm):
    """
    FORM
    details the ActIds form (ids validation only -> fields from index file only)
    """

    #EURLEX
    no_celex=forms.RegexField(regex=r'^[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])([dflryDFLRY]|PC)[0-9]{4}(\(0[1-9]\)|R\(0[1-9]\))?$')
    #~ act
    #Ne peut etre=000L (sauf pour l'acte de NoSaisie 329)
    #Chaque acte a un numero Celex et ce numero est unique (sauf exception : acte de releve_annee='2004', ReleveMois='4' et NoOrdre='52', OrdreSaisie='329')


    #OEIL
    no_unique_type=forms.RegexField(regex=r'^COD|SYN|CNS|ACC|AVC|CS|CNB|ACI$', required=False)
    #~ no_unique_type
    #^(COD|SYN|CNS|ACC|AVC|CS|CNB|ACI)$"
    #~ Valeur du champ indiquee sur la fiche Prelex, oeil et Celex si NoUniqueType=COD ou SYN ou CNS ou AVC
    #~ ou ACI, uniquement sur les fiches Prelex et Celex si NoUniqueType=ACC
    #~ Codes COD, SYN, CNS, ACC, AVC, CNB et ACI attribues par l'UE ; en cas de divergences entre la fiche Prelex
    #~ et la fiche oeil, on prend le numero qui permet de retrouver la fiche via Oeil
    #~ Code CS recode lors de la constitution de la base pour les procedures n'impliquant que le Conseil

    no_unique_annee=forms.IntegerField(min_value=1957, max_value=2020, required=False)
    #~ no_unique_annee
    #~ 1957 a l'annee courante.
    #~ Valeur du champ indiquee sur la fiche Prelex, oeil et Celex si NoUnique Type=COD ou SYN ou CNS ou AVC
    #~ ou ACI, uniquement sur les fiches Prelex et Celex si NoUniqueType=ACC
    #~ Valeur 000L si NumUniqueType=CS

    no_unique_chrono=forms.RegexField(regex=r'^([1-9]([0-9]?){3})([a-zA-Z])?$', required=False)
    #~ no_unique_chrono
    #4 digits or 4 digits + 1 letter (if splitted proposition)
    #De 1 a 999
    #Valeur du champ indiquee sur la fiche Prelex, oeil et Celex si NoUniqueType=COD ou SYN ou CNS ou AVC ou ACI, uniquement sur les fiches Prelex et Celex si NoUniqueType=ACC
    #Valeur 000L si NumUniqueType=CS


    #PRELEX
    #normal case
    propos_origine=forms.RegexField(regex=r'^COM|JAI|BCE|EM|CONS|CJEU$', required=False)
    #~ Ne peut etre=000L. Une valeur parmi :COM, JAI, BCE, EM, CONS
    #~ Valeurs COM et JAI indiquees sur la fiche Prelex, Celex (et oeIL si le PE intervient dans la procedure)
    #~ Valeurs BCE indiquees sur la fiche Celex (il n'y a pas toujours de fiche Prelex)
    #~ Valeurs EM et CONS recodees lors de la constitution de la base
    #~ Ce champ est issu d'une saisie manuelle

    propos_annee=forms.IntegerField(min_value=1957, max_value=2020, required=False)
    #~ Valeurs possibles : Ne peut etre=000L
    #~ de 1957 a annee courante.
    #~ Lorsque ProposOrigine=COM ou JAI ou BCE, la valeur est celle qui figure dans le "code" du projet a l'origine de l'acte du Conseil, attribue par l'UE et indique sur les fiches Celex et Prelex (en cas de BCE, il n'existe pas toujours de fiche Prelex)
    #~ Lorsque ProposOrigine=CONS, la valeur est l'annee du document le plus ancien que nous puissions trouver
    #~ dans le registre du Conseil
    #~ Lorsque ProposOrigine=EM et que la date de la demande de l'Etat membre figure sur l'acte publie au JO, la
    #~ valeur est l'annee de cette date
    #~ Lorsque ProposOrigine=EM et que la date de la demande de l'Etat membre ne figure pas sur l'acte publie au
    #~ JO, la valeur est l'annee du document le plus ancien que nous puissions trouver dans le registre du Conseil

    propos_chrono=forms.RegexField(regex=r'^([0-9]([0-9]?){4})(-[1-9][0-9]?)?$', required=False)
    #one to 5 digits (+ one hyphen and digit if splitted proposition)
    #~ Valeurs possibles : Peut etre=000L
    #~ De 1 a 99999
    #~ Origine :
    #~ 1) Fiche Celex et Prelex
    #~ 2) Registre du Conseil (saisie manuelle)
    #~ 3) et 4) Fiche Celex ou registre du Conseil (saisie manuelle)

    #dos_id
    dos_id=forms.IntegerField(min_value=1, max_value=9999999, required=False)
    #between 1 and 9999999

    #display all the possible dos_id variables in the index row
    dos_id_choices=forms.ChoiceField(required=False)


    class Meta:
        model=ActIds
        #fields excluded from the validation
        exclude=('src', 'url_exists', 'act', 'dos_id_choices',)


    #dynamically populate dos_id_choices (list of possible dos_id variables for the act)
    def __init__(self, *args, **kwargs):
        super(ActIdsForm, self).__init__(*args, **kwargs)
        if self.fields['dos_id_choices']:
            #get dos_ids from the ImportDosId model
            qs=ImportDosId.objects.only("dos_id").filter(no_celex=self.instance.no_celex)
            dos_ids=[(row.dos_id, row.dos_id) for row in qs]
            #check if there is already a validated dos_id
            try:
                dos_id=ActIds.objects.only("dos_id").get(src="index", act=self.instance.act)
                #if it's not a possible dos_id yet, add it to the list
                if dos_id.dos_id!=None and dos_id.dos_id not in [dos_id_temp[0] for dos_id_temp in dos_ids]:
                    dos_ids.append((dos_id.dos_id, dos_id.dos_id))
            except Exception, e:
                #~ print "no validated dos_id for this act", e
                pass

            #assign the choices to the drop down list
            self.fields['dos_id_choices'].choices = dos_ids
            #no_celex not editable
            self.fields["no_celex"].widget.attrs['readonly'] = True


    def clean(self):
        super(ActIdsForm, self).clean() #if necessary
        cleaned_data=self.cleaned_data
        #do not validate dos_id_choices -> if an error comes from this field, remove it
        if 'dos_id_choices' in self._errors:
            del self._errors['dos_id_choices']

        #trim trailing spaces
        for k in self.cleaned_data:
            try:
                #only strings
                cleaned_data[k]=self.cleaned_data[k].strip()
            except:
                pass
        return cleaned_data

    #no_celex from index file must be unique
    def is_valid(self):
        # run the parent validation first
        valid=super(ActIdsForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        #if the form is valid
        no_celex=self.cleaned_data["no_celex"]
        try:
            act_ids=ActIds.objects.get(no_celex=no_celex, src="index")
            #if another act has the same no_celex already
            if act_ids!=self.instance:
                #if it exists already, raise error
                self._errors['no_celex']=ErrorList([var_name_ids.var_name['no_celex']+u" already exists!"])
                return False
        except:
            pass

        # form valid -> return True
        return True


class ActForm(forms.ModelForm):
    """
    FORM
    details the ActForm form (notes field)
    """
    #transform textbox to textarea
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model=Act
        #fields used for the validation
        field=('notes',)


class Add(forms.Form):
    """
    FORM
    details the Add form (fields for the add mode of ActIdsForm)
    """
    act_to_validate=forms.ModelChoiceField(queryset=Act.objects.only("releve_annee", "releve_mois", "no_ordre").filter(validated=0), empty_label="Select an act to validate")


class Modif(forms.Form):
    """
    FORM
    details the Modif form (fields for the modification mode of ActIdsForm)
    """
    #ids input boxes used for the modification
    releve_annee_modif=forms.IntegerField(label=var_name_data.var_name['releve_annee'], min_value=1957, max_value=2020)
    releve_mois_modif=forms.IntegerField(label=var_name_data.var_name['releve_mois'], min_value=1, max_value=12)
    no_ordre_modif=forms.IntegerField(label=var_name_data.var_name['no_ordre'], min_value=1, max_value=99)

    #check if the searched act already exists in the db and has been validated
    def is_valid(self):
        # run the parent validation first
        valid=super(Modif, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        #if the form is valid
        releve_annee_modif=self.cleaned_data.get("releve_annee_modif")
        releve_mois_modif=self.cleaned_data.get("releve_mois_modif")
        no_ordre_modif=self.cleaned_data.get("no_ordre_modif")

        try:
            act=Act.objects.get(releve_annee=releve_annee_modif, releve_mois=releve_mois_modif, no_ordre=no_ordre_modif, validated__gt=0)
        except:
            self._errors['__all__']=ErrorList([u"The act you are looking for has not been validated yet!"])
            return False

        # form valid -> return True
        return True


#~ il arrive que l'acte soit sur 1 fiche (Celex, par 32003D0277) ou 2 fiches (Celex et Prelex, par ex 32003D0065) ou 3 fiches (Celex, Prelex et OEIL, par ex 32003L0015).

#~ from celex, check if there is an oeil page:
#~ sur le document Celex il n'y a pas non plus de NumUnique, mais il s'agit parfois d'un oubli, donc il vaut mieux verifier avec le contenu de l'acte qui se trouve aussi dans le document Celex : il faut que l'acte soit adopte uniquement par le Conseil et qu'il n'y ait PAS au debut de l'acte 'Having regard to the opinion of the European Parliament'.

#~ il faudrait que lorsqu'on les rentre manuellement dans la base ou sur une interface (je ne sais pas si j'utilise le bon mot!), on puisse savoir immediatement s'il y a un probleme 1) pour construire l'url et trouver la page/fiche correspondante 2) d'incoherences entre les identifiants sur les differentes pages (si par ex il y a une fiche prelex et oeil, il faut que le NoUnique soit le meme sur les deux fiches)
