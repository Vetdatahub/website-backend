from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from datasets.models import Category, Dataset, DatasetRating, DatasetVersion, Specie
from datasets.permissions import IsOwnerOrReadOnly
from datasets.serializers import (
    CategorySerializer,
    CreateDatasetSerializer,
    DatasetRatingSerializer,
    DatasetSerializer,
    DatasetVersionSerializer,
    SpecieSerializer,
)


class SpecieListView(ListAPIView):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class DatasetListView(ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]


class DatasetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class DatasetCreateView(CreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = CreateDatasetSerializer
    permission_classes = [IsAuthenticated]


class DatasetRatingCreateView(CreateAPIView):
    queryset = DatasetRating.objects.all()
    serializer_class = DatasetRatingSerializer
    permission_classes = [IsAuthenticated]


class DatasetVersionCreateView(CreateAPIView):
    queryset = DatasetVersion.objects.all()
    serializer_class = DatasetVersionSerializer
    permission_classes = [IsAuthenticated]
