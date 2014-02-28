from django.db import models
from act.models import Act
from django.core.exceptions import ValidationError


class ActIds(models.Model):
    """
    MODEL
    instances of acts ids
    for each act, several sources: index file (monthly council summary), eurlex, oeil, prelex
    """
    #when importing an index file, acts are inserted into the db except if:
    #a no_celex has been added while importing a dos_id or opal file

    #src="index", "eurlex", "oeil" or "prelex"
    src=models.CharField(max_length=6, default="index", db_index=True)
    url_exists=models.BooleanField(default=True)
    #no_celex for index file must be unique
    no_celex=models.CharField(max_length=15, blank=True, null=True, default=None)
    no_unique_type=models.CharField(max_length=4, blank=True, null=True, default=None)
    no_unique_annee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
    no_unique_chrono=models.CharField(max_length=5, blank=True, null=True, default=None)
    propos_origine=models.CharField(max_length=4, blank=True, null=True, default=None)
    propos_annee=models.IntegerField(max_length=4, blank=True, null=True, default=None)
    propos_chrono=models.CharField(max_length=7, blank=True, null=True, default=None)
    dos_id=models.IntegerField(max_length=7, blank=True, null=True, default=None)
    act=models.ForeignKey(Act)

    #joined primary keys
    class Meta:
        unique_together=(("act", "src"), )

    #no_celex from index file must be unique
    def clean(self, *args, **kwargs):
        #~ super(ActIds, self).clean(*args, **kwargs)
        if self.src=="index":
            no_celex=self.no_celex
            try:
                act_ids=ActIds.objects.get(no_celex=no_celex, src="index")
                #if another act has the same no_celex already
                if act_ids!=self:
                    #if it exists already, raise error
                    raise ValidationError('%s NoCelex must be unique')
            except Exception, e:
                #~ print "the no_celex does not exist in the db yet", e
                pass

        return self
