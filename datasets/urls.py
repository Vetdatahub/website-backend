from django.urls import path
from datasets.views import (
    SpecieListView,
    CategoryListView,
    DatasetListView,
    DatasetDetailView,
    DatasetCreateView,
    DatasetRatingCreateView,
    DatasetVersionCreateView,
)

urlpatterns = [
    path('species/', SpecieListView.as_view(), name='specie-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', DatasetListView.as_view(), name='dataset-list'),
    path('<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('create/', DatasetCreateView.as_view(), name='dataset-create'),
    path('ratings/', DatasetRatingCreateView.as_view(), name='dataset-rating-create'),
    path('versions/', DatasetVersionCreateView.as_view(), name='dataset-version-create'),
]