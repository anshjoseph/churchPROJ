from django.db import models
from directory.models import Family
# for signaling
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete,pre_save
# uuid
from uuid import uuid4 # // 36 chars
# sha256 for password
from hashlib import sha256



# LOGINMASTER TABLE
class LoginMaster(models.Model):
    family = models.OneToOneField(Family,on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    passwordhash = models.CharField(max_length=256,default="genrated")

# receiver for making new uuid
@receiver(post_save,sender=LoginMaster)
def passwordhash(**kargs):
    if kargs.get('created'):
        instance = kargs.get('instance')
        instance.passwordhash = sha256(str(instance.password).encode('utf-8')).hexdigest()
        instance.save()
        return
    if not kargs.get('created'):
        instance = kargs.get('instance')
        hashpass = sha256(str(instance.password).encode('utf-8')).hexdigest()
        if instance.passwordhash !=  hashpass:
            instance.passwordhash = sha256(str(instance.password).encode('utf-8')).hexdigest()
            instance.save()
        return

    

# SESSION TABLE
class Session(models.Model):
    familyid = models.ForeignKey(LoginMaster,on_delete=models.CASCADE)
    sessionid = models.CharField(max_length=64,default="new",auto_created=True,unique=True)
# receiver for making new uuid
@receiver(post_save,sender=Session)
def needSessionUuid(**kargs):
    print(kargs)
    if kargs.get('created'):
        instance = kargs.get('instance')
        instance.sessionid = str(uuid4())
        instance.save()
        return 0


class APIkey(models.Model):
    key = models.CharField(max_length=64,default="genrate",unique=True)
    def __str__(self) -> str:
        return self.key
@receiver(post_save,sender=APIkey)
def genkey(**kargs):
    if kargs.get('created'):
        instance = kargs.get('instance')
        instance.key = str(uuid4())
        instance.save()