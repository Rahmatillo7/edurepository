from rest_framework import serializers
from .models import Resource, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Resource
        fields = ['id', 'title', 'subject_name', 'class_level', 'language', 'file', 'view_count', 'download_count']
