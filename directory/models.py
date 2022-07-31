from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# for signaling in future
# for uniqe id
from uuid import uuid4

# WARD
class Ward(models.Model):
    ward_name = models.CharField(max_length=1024)
    ward_head = models.TextField()
    # for printing in dashboard
    def __str__(self) -> str:
        return f"{self.id}-{self.ward_name}"

    # for printing in terminal
    def __repr__(self) -> str:
        return f"{self.ward_name}"


# FAMILY
class Family(AbstractBaseUser):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="family_ward")
    family_name = models.CharField(max_length=255)
    family_head_name = models.CharField(max_length=255)
    member_count = models.IntegerField(default=1)

    USERNAME_FIELD = "family_name"

    class Meta:
        unique_together = ["family_head_name", "ward"]

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
