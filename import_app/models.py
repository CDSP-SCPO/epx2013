from django.db import models
import act.var_name_data as var_name_data
from hashlib import md5
from django.core.validators import MaxValueValidator, MinValueValidator


def file_path(instance, file_name):
    """
    FUNCTION
    remove all spaces from the uploaded file name
    PARAMETERS
    instance: instance of the file [object]
    file_name: name of the file to process [string]
    RETURN
    new file name [string]
    """
    file_name_new=" ".join(file_name.split())
    return '/'.join(['import', file_name_new])


class CSVUpload(models.Model):
    """
    MODEL
    instances of csv files
    """
    csv_file=models.FileField(upload_to=file_path)




#TEMPORARY MODELS FOR IMPORT ONLY

class ImportDosId(models.Model):
    """
    MODEL
    temporary model: possible dos_id for each act
    """
    dos_id=models.IntegerField(max_length=7, blank=False, null=False)
    no_celex=models.CharField(max_length=15, blank=False, null=False)

    #joined primary keys
    class Meta:
        unique_together=(("dos_id", "no_celex"), )

    def __unicode__(self):
        return u"%s" % self.dos_id


class ImportNP(models.Model):
    """
    MODEL
    tempory model: np variables for each act (Opal)
    """
    case_nb=models.IntegerField(max_length=10, primary_key=True)
    no_celex=models.CharField(max_length=15, blank=False, null=False)
    #country_code
    np=models.CharField(max_length=2, blank=False, null=False)
    act_type=models.CharField(max_length=40, blank=False, null=False)
    act_date=models.DateField(max_length=10, blank=True, null=True, default=None)


class ImportAdoptPC(models.Model):
    """
    MODEL
    temporary model: adopt_pc_abs and adopt_pc_contre variables for each act
    """
    releve_annee=models.IntegerField(max_length=4, blank=False, null=False)
    releve_mois=models.IntegerField(max_length=2, blank=False, null=False)
    no_ordre=models.IntegerField(max_length=2, blank=False, null=False)
    no_celex=models.CharField(max_length=15, blank=False, null=False)
    #list of country_codes
    adopt_pc_abs=models.CharField(max_length=18, blank=True, null=True, default=None)
    #list of country_codes
    adopt_pc_contre=models.CharField(max_length=18, blank=True, null=True, default=None)

    #joined primary keys
    class Meta:
        unique_together=(("releve_annee", "releve_mois", "no_ordre"), )


class ImportMinAttend(models.Model):
    """
    MODEL
    temporary model: attendance of ministers for each act and each country
    """
    releve_annee=models.IntegerField(max_length=4)
    releve_mois=models.IntegerField(max_length=2)
    no_ordre=models.IntegerField(max_length=2)
    no_celex=models.CharField(max_length=15, blank=False, null=False)
    #country_code
    country=models.CharField(max_length=2, blank=False, null=False)
    verbatim=models.CharField(max_length=300, blank=False, null=False)
    status=models.CharField(max_length=5, blank=True, null=True, default=None)

    #joined primary keys
    class Meta:
        #use the sql command below if the joined unique index did not work (due to limitation on the length of the fields)
        #ALTER TABLE `europolix`.`import_app_importminattend` ADD INDEX (no_celex, country, verbatim(255));
        unique_together=(("no_celex", "country", "verbatim"), )


class ImportRappPartyFamily(models.Model):
    """
    MODEL
    tempory model: correspondance between parties and party families for rapporteurs
    """
    party=models.CharField(max_length=70, unique=True, blank=False, null=False)
    party_family=models.CharField(max_length=50, blank=False, null=False)


class ImportGroupVotes(models.Model):
    """
    MODEL
    tempory model: for each act (identified by its title), gives the ep group votes
    """
    title=models.CharField(max_length=2000)
    title_md5 = models.CharField(max_length=32)
    #ADLE, S&D, PPE-DE, ECR, EFD, Greens/EFA, GUE-NGL, NI
    group_name=models.CharField(max_length=15)
    col_for=models.PositiveSmallIntegerField(max_length=3)
    col_against=models.PositiveSmallIntegerField(max_length=3)
    col_abstension=models.PositiveSmallIntegerField(max_length=3)
    col_present=models.PositiveSmallIntegerField(max_length=3)
    col_absent=models.PositiveSmallIntegerField(max_length=3)
    col_non_voters=models.PositiveSmallIntegerField(max_length=3)
    col_total_members=models.PositiveSmallIntegerField(max_length=3)
    col_cohesion=models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])

    def save(self, *args, **kwargs):
        #saving title using md5 hash to use the constraint unique together on title (with the hash) and group_name
        #otherwise error django.db.utils.DatabaseError: (1071, 'Specified key was too long; max key length is 767 bytes')
        self.title_md5 = md5(self.title).hexdigest()
        super(ImportGroupVotes, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title+", "+self.group_name

    #joined primary keys
    class Meta:
        unique_together=(("title_md5", "group_name"), )
