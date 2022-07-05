from django.db import models
# for signaling in future
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
# for uniqe id
from uuid import uuid4

# WARD
class Ward(models.Model):
    wardname = models.CharField(max_length=1024)
    wardhead = models.CharField(max_length=100)
    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.wardname}"
    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.wardname}"

# FAMILY
class Family(models.Model):
    wardid = models.ForeignKey(Ward,on_delete=models.CASCADE)
    familyname = models.CharField(max_length=300)
    membercount = models.IntegerField(default=0)
    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.familyname}"
    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.familyname}"

# PEOPLE
class People(models.Model):
    familyid = models.ForeignKey(Family,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    # feilds were add according to need
    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.name}"
    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.name}"