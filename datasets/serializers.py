from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datasets.models import Dataset,DatasetRating,DatasetVersion,Specie,Category

class SpecieSerializer(ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CreateDatasetSerializer(ModelSerializer):
    file_size = serializers.IntegerField(write_only=True, required=True)
    filetype = serializers.CharField(write_only=True, required=True)
    version_number = serializers.IntegerField(write_only=True, required=True)
    changes = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Dataset
        fields = '__all__'

    def create(self, validated_data):
        file_url = validated_data.pop('file_url')
        filetype = validated_data.pop('filetype')
        version_number = validated_data.pop('version_number')
        changes = validated_data.pop('changes', None)
        filesize = validated_data.pop('filesize')

        dataset = Dataset.objects.create(**validated_data)
        DatasetVersion.objects.create(
            dataset=dataset,
            version_number=version_number,
            file_url=file_url,
            filesize=filesize,
            filetype=filetype,
            changes=changes
        )
        return dataset

class DatasetSerializer(ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = '__all__'


    def get_avg_rating(self, obj):
        ratings = obj.dataset_ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    def get_versions(self, obj):
        return DatasetVersionSerializer(obj.dataset_versions.all(), many=True).data
    
    

class DatasetRatingSerializer(ModelSerializer):
    class Meta:
        model = DatasetRating
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=DatasetRating.objects.all(),
                fields=['dataset', 'user']
            )
        ]

class DatasetVersionSerializer(ModelSerializer):
    class Meta:
        model = DatasetVersion
        fields = '__all__'


        