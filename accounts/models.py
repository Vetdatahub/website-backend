from django.db import models
from  django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    ROLES_CHOICES = [
        ('researcher', 'Researcher'),
        ('practitioner', 'Practitioner  '),
        ('student', 'Student'),
        ('policy_analyst',"Policy Analyst"),
        ('data_engineer', "Data Engineer"),
        ('other','Other')
    ]
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    affiliation = models.CharField(max_length=200, blank=True,null=True)
    location = models.CharField(max_length=100, blank=True,null=True)
    website = models.URLField(blank=True, null=True)
    orcid = models.CharField(max_length=20, blank=True,null=True)
    role = models.CharField(max_length=50, choices=ROLES_CHOICES)
    subscribe_to_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
