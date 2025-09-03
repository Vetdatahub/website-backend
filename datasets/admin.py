from django.contrib import admin

from datasets.models import Category, Dataset, DatasetRating, DatasetVersion, Specie

admin.site.register(Dataset)
admin.site.register(DatasetVersion)
admin.site.register(DatasetRating)
admin.site.register(Specie)
admin.site.register(Category)
