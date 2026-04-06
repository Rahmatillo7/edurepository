from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ResourceSerializer
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.views import APIView
from django.db import models
from .models import Resource


class ResourceListAPIView(generics.ListAPIView):
    queryset = Resource.objects.filter(is_verified=True)
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'class_level', 'language']
    search_fields = ['title', 'description']


class ResourceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if self.request.method == 'GET':
            session_key = f'viewed_resource_{obj.pk}'
            if not self.request.session.get(session_key):
                Resource.objects.filter(pk=obj.pk).update(
                    view_count=models.F('view_count') + 1
                )
                self.request.session[session_key] = True
                self.request.session.set_expiry(86400)
                obj.refresh_from_db()
        return obj


class ResourceCreateAPIView(generics.CreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ResourceDownloadAPIView(APIView):
    def get(self, request, pk):
        resource = get_object_or_404(Resource, pk=pk)

        session_key = f'downloaded_resource_{pk}'
        if not request.session.get(session_key):
            Resource.objects.filter(pk=pk).update(
                download_count=models.F('download_count') + 1
            )
            request.session[session_key] = True
            request.session.set_expiry(86400)

        response = FileResponse(resource.file.open('rb'), as_attachment=True)
        return response