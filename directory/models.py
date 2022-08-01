from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# for signaling in future
# for uniqe id
from uuid import uuid4

# WARD


class FamilyManager(BaseUserManager):
    def create_user(
        self, ward_id, family_name, family_head_name, member_count, password=None
    ):
        if not ward_id:
            raise ValueError("Ward ID is required")
        if not family_name:
            raise ValueError("Family Name is required")
        if not family_head_name:
            raise ValueError("Family Head Name is required")
        family = self.model(
            ward_id=ward_id,
            family_name=family_name,
            family_head_name=family_head_name,
            member_count=member_count,
        )
        family.set_password(password)
        family.save(using=self._db)
        return family

    def create_superuser(self, family_name, password):

        family = self.create_user(
            ward_id=3564563213543132,
            family_name=family_name,
            family_head_name=f"{family_name}-head",
            member_count=1,
            password=password,
        )
        family.is_staff = True
        family.is_superuser = True
        family.is_admin = True

        family.save(using=self._db)
        return family


class Ward(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    ward_name = models.CharField(max_length=255)
    ward_head = models.TextField()
    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.ward_name}"

    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.ward_name}"


# FAMILY
class Family(AbstractBaseUser, PermissionsMixin):
    ward_id = models.BigIntegerField(default=0)
    family_name = models.CharField(max_length=255)
    family_head_name = models.CharField(max_length=255)
    member_count = models.IntegerField(default=1)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "family_name"

    class Meta:
        unique_together = ["family_head_name", "ward_id"]

    objects = FamilyManager()

    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.family_name}"

    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.family_name}"


# PEOPLE
class People(models.Model):
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="people_family"
    )
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(default=1)
    date_of_birth = models.DateField(null=False)

    def __str__(self) -> str:
        return f"{self.first_name}-{self.last_name}"

    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.last_name}"
