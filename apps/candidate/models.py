from django.db import models
from .constants import GENDER_CHOICES
from django.contrib.postgres.indexes import GinIndex


class Candidate(models.Model):

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True, help_text="Candidate's email address (must be unique)")
    phone_number = models.CharField(max_length=20, unique=True, help_text="Candidate's phone number (must be unique)")


    class Meta:
        app_label = 'candidate'
        ordering = ['name']
        indexes = [
            GinIndex(
                fields=['name'],
                name='candidate_name_gin_trgm_idx',
                opclasses=['gin_trgm_ops']
            ),
        ]

    def __str__(self):
        return self.name