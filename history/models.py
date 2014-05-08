from django.db import models
from django.contrib.auth.models import User
from act.models import Act


class History(models.Model):
    """
    MODEL
    history of validated acts
    """
    date=models.DateField(max_length=10, blank=False, null=False, auto_now_add=True)
    time = models.TimeField(max_length=8, blank=False, null=False, auto_now_add=True)
    #"add" or "modif"
    action=models.CharField(max_length=5, blank=False, null=False)
    #"ids" or "data" or "attendance"
    form=models.CharField(max_length=10, blank=False, null=False)
    act=models.ForeignKey(Act)
    user = models.ForeignKey(User)
