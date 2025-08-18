from rest_framework.serializers import ModelSerializer
from datasets.models import Dataset,DatasetRating,DatasetVersion,Specie,Category

class SpecieSerializer(ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DatasetSerializer(ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class DatasetRatingSerializer(ModelSerializer):
    class Meta:
        model = DatasetRating
        fields = "__all__"

class DatasetVersionSerializer(ModelSerializer):
    class Meta:
        model = DatasetVersion
        fields = '__all__'


        