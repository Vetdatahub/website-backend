from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


# Create your models here.
class Specie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    species = models.ForeignKey(
        Specie, on_delete=models.CASCADE, null=True, blank=True, related_name="datasets_species"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    sampleSize = models.IntegerField(null=True, blank=True)
    fundingSource = models.CharField(max_length=255, null=True, blank=True)
    ethicsApproval = models.CharField(max_length=255, null=True, blank=True)
    methodology = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DatasetVersion(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="dataset_versions")
    version_number = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_url = models.URLField()
    filesize = models.PositiveIntegerField()
    filetype = models.CharField(max_length=100)
    changes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.dataset.title} - Version {self.version_number}"


class DatasetRating(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="dataset_ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("dataset", "user")

    def __str__(self):
        return f"{self.user.username} - {self.dataset.title} - {self.rating}"
